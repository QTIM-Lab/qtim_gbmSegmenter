import numpy as np
import nibabel as nib
import os

from keras import backend as K
from keras.models import load_model

import qtim_gbmSegmenter.PreProcessing_Library.common as common

def skull_strip_models():

    model_dict = {}
    for modality in ['FLAIR', 'T2']:
        model_dict[modality] = os.path.join(os.path.dirname(__file__),'model_data', modality + '_ss.h5')

    return model_dict

def segmentation_models():

    model_dict = {}
    for tissue in ['wholetumor', 'enhancingtumor']:
        model_dict[tissue] = os.path.join(os.path.dirname(__file__),'model_data', tissue + '.h5')

    return model_dict

    return

def evaluate_model(model, input_filenames, output_filename, patch_shape):

    input_data, input_affine = read_image_files(input_filenames, return_affine=True)
    input_data = np.expand_dims(input_data, 0)
    if input_data.ndim < 5:
        input_data = np.expand_dims(input_data, 0)

    output_shape = list(input_data.shape)
    output_shape[1] = 1
    output_shape = tuple(output_shape)

    output_data = predict_patches_one_image(input_data, patch_shape, model, output_shape, repetitions=8, model_batch_size=100)

    save_prediction(output_data, output_filename, input_affine=input_affine)

def predict_patches_one_image(input_data, patch_shape, model, output_shape, repetitions=1, model_batch_size=1):

    output_data = np.zeros(output_shape)

    repetition_offsets = [np.linspace(0, patch_shape[x], repetitions, dtype=int) for x in xrange(len(patch_shape))]

    for rep_idx in xrange(repetitions):

        print 'PREDICTION PATCH GRID REPETITION # ..', rep_idx

        offset_slice = [slice(min(repetition_offsets[axis][rep_idx], input_data.shape[axis+2]-patch_shape[axis]), None, 1) for axis in xrange(len(patch_shape))]
        offset_slice = [slice(None)]*2 + offset_slice
        repatched_image = np.zeros_like(output_data[offset_slice])
        corners_list = patchify_image(input_data[offset_slice], [input_data[offset_slice].shape[1]] + list(patch_shape))

        for corner_list_idx in xrange(0, len(corners_list), model_batch_size):

            corner_batch = corners_list[corner_list_idx:corner_list_idx+model_batch_size]
            input_patches = grab_patch(input_data[offset_slice], corners_list[corner_list_idx:corner_list_idx+model_batch_size], patch_shape)
            prediction = model.predict(input_patches)

            for corner_idx, corner in enumerate(corner_batch):
                insert_patch(repatched_image, prediction[corner_idx, ...], corner)

        if rep_idx == 0:
            output_data = np.copy(repatched_image)
        else:
            # Running Average
            output_data[offset_slice] = output_data[offset_slice] + (1.0 / (rep_idx)) * (repatched_image - output_data[offset_slice])

    return output_data

def patchify_image(input_data, patch_shape, offset=(0,0,0,0), batch_dim=True, return_patches=False, mask_value = 0):

    corner = [0] * len(input_data.shape[1:])

    if return_patches:
        patch = grab_patch(input_data, corner, patch_shape)
        patch_list = [[corner[:], patch[:]]]
    else:
        patch_list = [corner[:]]

    finished = False

    while not finished:

        # Wonky, fix in grab patch.
        patch = grab_patch(input_data, [corner], tuple(patch_shape[1:]))
        if np.sum(patch != 0):
            if return_patches:
                patch_list += [[corner[:], patch[:]]]
            else:
                patch_list += [corner[:]]

        for idx, corner_dim in enumerate(corner):

            # Advance corner stride
            if idx == 0:
                corner[idx] += patch_shape[idx]

            # Finish patchification
            if idx == len(corner) - 1 and corner[idx] == input_data.shape[-1]:
                finished = True
                continue

            # Push down a dimension.
            if corner[idx] == input_data.shape[idx+1]:
                corner[idx] = 0
                corner[idx+1] += patch_shape[idx+1]

            elif corner[idx] > input_data.shape[idx+1] - patch_shape[idx]:
                corner[idx] = input_data.shape[idx+1] - patch_shape[idx]

    return patch_list

def grab_patch(input_data, corner_list, patch_shape, mask_value=0):

    """ Given a corner coordinate, a patch_shape, and some input_data, returns a patch or array of patches.
    """

    output_patches = np.zeros(((len(corner_list),input_data.shape[1]) + patch_shape))

    for corner_idx, corner in enumerate(corner_list):
        output_slice = [slice(None)]*2 + [slice(corner_dim, corner_dim+patch_shape[idx], 1) for idx, corner_dim in enumerate(corner[1:])]
        output_patches[corner_idx, ...] = input_data[output_slice]

    return output_patches

def insert_patch(input_data, patch, corner):

    patch_shape = patch.shape[1:]

    patch_slice = [slice(None)]*2 + [slice(corner_dim, corner_dim+patch_shape[idx], 1) for idx, corner_dim in enumerate(corner[1:])]
    
    input_data[patch_slice] = patch

    return

def save_prediction(input_data, output_filepath, input_affine, binarize_probability=.5, stack_outputs=True):


    output_shape = input_data.shape
    input_data = np.squeeze(input_data)

    # If output modalities is one, just save the output.
    if output_shape[1] == 1:
        binarized_output_data = threshold_binarize(threshold=binarize_probability, input_data=input_data)
        print 'SUM OF ALL PREDICTION VOXELS', np.sum(binarized_output_data)
        common.save_numpy_2_nifti(binarized_output_data, reference_affine=input_affine, output_path=output_filepath)

    return

def threshold_binarize(input_data, threshold):

    return (input_data > threshold).astype(float)

def read_image_files(image_files, return_affine=False):

    if isinstance(image_files, basestring):
        output_data = np.expand_dims(common.nifti_2_numpy(image_files), 0)
        output_affine = nib.load(image_files).affine
    else:
        image_list = []
        for i, image_file in enumerate(image_files):
            image_list.append(common.nifti_2_numpy(image_file))
        output_data = np.stack([image for image in image_list])
        output_affine = nib.load(image_files[0]).affine

    # This is a little clunky.
    if return_affine:
        # This assumes all images share an affine matrix.
        return output_data, output_affine
    else:
        return output_data

def msq(y_true, y_pred):
    return K.sum(K.pow(y_true - y_pred, 2), axis=None)

def msq_loss(y_true, y_pred):
    return msq(y_true, y_pred)

def dice_coef(y_true, y_pred, smooth=1.):
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)
    return (2. * intersection + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth)

def dice_coef_loss(y_true, y_pred):
    return (1 - dice_coef(y_true, y_pred))

def load_old_model(model_file):

    custom_objects = {'dice_coef_loss': dice_coef_loss, 'dice_coef': dice_coef, 'msq': msq, 'msq_loss': msq_loss}

    return load_model(model_file, custom_objects=custom_objects)

if __name__ == '__main__':
    pass