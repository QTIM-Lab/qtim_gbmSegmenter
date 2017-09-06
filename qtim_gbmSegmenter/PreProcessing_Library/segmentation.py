import os
import fnmatch

from subprocess import call

from qtim_gbmSegmenter.Config_Library.step import PipelineStep
from qtim_gbmSegmenter.DeepLearningLibrary.models import skull_strip_models, evaluate_model

def segmentation_deepneuro(input_folder, output_filename, output_each_label=False):

    model_dict = skull_strip_models()

    target_modality = None
    for modality in modality_codes.keys():
        if fnmatch.fnmatch(os.path.basename(input_filename), modality_codes[modality]):
            target_modality = modality

    if target_modality is None:
        print 'No modality matched for skull-stripping file: ', input_filename
        return

    no_path = os.path.basename(os.path.normpath(output_filename))
    file_prefix = str.split(no_path, '.nii')
    output_mask_filename = os.path.join(os.path.dirname(output_filename), file_prefix[0] + output_mask_suffix + '.nii.gz')
    
    input_filename = os.path.abspath(input_filename)
    print model_dict[target_modality], input_filename
    print input_filename, output_mask_filename

    evaluate_model(model_dict[target_modality], os.path.abspath(input_filename), os.path.abspath(output_mask_filename), patch_shape=(32,32,32))

    pass  

def execute(input_volume, output_filename, specific_function, params):

    if specific_function == 'fsl_skull_stripping':
        skull_strip_fsl(*[input_volume, output_filename] + params)
    elif specific_function == 'deepneuro_skull_stripping':
        skull_strip_deepneuro(*[input_volume, output_filename] + params)
    else:
        print 'There is no skull-stripping method associated with this keyword: ' + specific_function + '. Skipping volume located at...' + input_volume

def run_test():
    return

if __name__ == '__main__':
    run_test()