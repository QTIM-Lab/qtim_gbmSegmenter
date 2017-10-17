import os
import fnmatch

from subprocess import call
from qtim_tools.qtim_utilities.file_util import replace_suffix
from qtim_tools.qtim_utilities.format_util import convert_input_2_numpy
from qtim_tools.qtim_preprocessing.image import fill_in_convex_outline
from qtim_tools.qtim_utilities.nifti_util import save_numpy_2_nifti
from scipy import misc, ndimage

from qtim_gbmSegmenter.DeepLearningLibrary.models import skull_strip_models, evaluate_model, load_old_model

def skull_strip_fsl(input_volumes, output_filenames, output_mask_suffix='_mask', skull_strip_threshold=.5, skull_strip_vertical_gradient=0):
    
    # Note - include head radius and center options in the future.

    bet_volume = input_volumes['T2']

    bet_base_command = ['bet2', bet_volume, output_filenames['T2'], '-f', str(skull_strip_threshold), '-g', str(skull_strip_vertical_gradient), '-m']

    try:
        print ' '.join(bet_base_command)
        print 'Using FSL\'s BET2 (Brain Extraction Tool) to skull-strip ' + bet_volume + ' to output volume ' + output_filenames['T2'] + '...'
        call(' '.join(bet_base_command), shell=True)

        output_mask = os.path.join(os.path.dirname(bet_volume), os.path.basename(replace_suffix(bet_volume, '', output_mask_suffix)))
        os.rename(output_filenames['T2'] + '_mask.nii.gz', output_mask)

    except:
        print 'BET2 skull-stripping failed for file ' + bet_volume

    return_filenames = {}
    return_filenames['mask'] = output_mask

    for key, input_volume in input_volumes.iteritems():

        label_data = convert_input_2_numpy(output_mask)
        crop_data = convert_input_2_numpy(input_volume)
        crop_data[label_data == 0] = 0
        save_numpy_2_nifti(crop_data, input_volume, output_filenames[key])

        return_filenames[key] = output_filenames[key]

    return return_filenames

def skull_strip_deepneuro(input_volumes, output_filenames, output_mask_suffix='_mask'):

    model_dict = skull_strip_models()

    target_model = model_dict['FLAIR']
    target_file = input_volumes['FLAIR']

    output_mask = os.path.join(os.path.dirname(target_file), os.path.basename(replace_suffix(target_file, '', output_mask_suffix)))
    
    evaluate_model(load_old_model(target_model), target_file, output_mask, patch_shape=(32,32,32))
    fill_in_convex_outline(output_mask, output_mask, output_mask)

    return_filenames = {}
    return_filenames['mask'] = output_mask

    for key, input_volume in input_volumes.iteritems():

        label_data = convert_input_2_numpy(output_mask)
        crop_data = convert_input_2_numpy(input_volume)
        crop_data[label_data == 0] = 0
        save_numpy_2_nifti(crop_data, input_volume, output_filenames[key])

        return_filenames[key] = output_filenames[key]

    return return_filenames

def execute(input_volumes, output_filenames, specific_function, params):

    if specific_function == 'fsl_skull_stripping':
        return skull_strip_fsl(*[input_volumes, output_filenames] + params)
    elif specific_function == 'deepneuro_skull_stripping':
        return skull_strip_deepneuro(*[input_volumes, output_filenames] + params)
    else:
        print 'There is no skull-stripping method associated with this keyword: ' + specific_function + '. Skipping volumes located at...' + input_volumes

def run_test():
    return

if __name__ == '__main__':
    run_test()
