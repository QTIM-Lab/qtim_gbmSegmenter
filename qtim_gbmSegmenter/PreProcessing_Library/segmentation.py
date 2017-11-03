import os
import fnmatch

from subprocess import call

from qtim_gbmSegmenter.DeepLearningLibrary.models import skull_strip_models, evaluate_model, segmentation_models, load_old_model

def segment_deepneuro(input_volumes, output_filenames, output_segmentation_name, model_name):

    model_dict = segmentation_models()
    segmentation_input_filenames = []
    return_filenames = input_volumes

    if model_name == 'wholetumor_downsample':
        for modality_code in ['FLAIR', 'T2', 'T1', 'T1POST']:
            segmentation_input_filenames += [input_volumes[modality_code]]

    if model_name == 'upsample_wholetumor':
        for modality_code in ['FLAIR', 'T2', 'T1', 'T1POST', 'wholetumor_downsample']:
            segmentation_input_filenames += [input_volumes[modality_code]]

    if model_name == 'enhancingtumor':
        for modality_code in ['FLAIR', 'T2', 'T1', 'T1POST', 'upsample_wholetumor']:
            segmentation_input_filenames += [input_volumes[modality_code]]

    output_segmentation = os.path.join(os.path.dirname(output_filenames['T2']), output_segmentation_name + '-label.nii.gz')

    # try:

    return_filenames[model_name] = evaluate_model(load_old_model(model_dict[model_name]), segmentation_input_filenames, os.path.abspath(output_segmentation), patch_shape=(32,32,32))

    return return_filenames

    # except:
        # print 'DeepNeuro segmentation failed for model ' + model_name
        # return []

def execute(input_volumes, output_filenames, specific_function, params):

    if specific_function == 'deepneuro_segment':
        return segment_deepneuro(*[input_volumes, output_filenames] + params)
    else:
        print 'There is no segmentation method associated with this keyword: ' + specific_function + '. Skipping volumes located at...' + input_volumes

def run_test():
    return

if __name__ == '__main__':
    run_test()
