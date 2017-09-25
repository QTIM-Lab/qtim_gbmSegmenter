import os
import fnmatch

from subprocess import call

from qtim_gbmSegmenter.Config_Library.step import PipelineStep
from qtim_gbmSegmenter.DeepLearningLibrary.models import skull_strip_models, evaluate_model, segmentation_models, load_old_model

def segment_deepneuro(input_volumes, output_filenames, output_wholetumor_name, output_enhancing_name):

    model_dict = segmentation_models()
    wholetumor_input_filenames, enhancingtumor_input_filenames = [], []
    return_filenames = input_volumes

    for modality_code in ['FLAIR', 'T2', 'T1POST', 'T1']:
        wholetumor_input_filenames += [input_volumes[modality_code]]
    for modality_code in ['FLAIR', 'T2', 'T1', 'T1POST']:
        enhancingtumor_input_filenames += [input_volumes[modality_code]]

    output_wholetumor = os.path.join(os.path.dirname(output_filenames['T2']), output_wholetumor_name + '-label.nii.gz')
    output_enhancing = os.path.join(os.path.dirname(output_filenames['T2']), output_enhancing_name + '-label.nii.gz')

    # try:

    evaluate_model(load_old_model(model_dict['wholetumor']), wholetumor_input_filenames, os.path.abspath(output_wholetumor), patch_shape=(32,32,32))
    return_filenames['wholetumor'] = output_wholetumor

    evaluate_model(load_old_model(model_dict['enhancingtumor']), enhancingtumor_input_filenames + [output_wholetumor], os.path.abspath(output_enhancing), patch_shape=(32,32,32))
    return_filenames['enhancingtumor'] = output_enhancing

    return return_filenames

    # except:
    #     print 'DeepNeuro skull-stripping failed for file ' + input_filename
    #     return []

def execute(input_volumes, output_filenames, specific_function, params):

    if specific_function == 'deepneuro_segment':
        segment_deepneuro(*[input_volumes, output_filenames] + params)
    else:
        print 'There is no segmentation method associated with this keyword: ' + specific_function + '. Skipping volumes located at...' + input_volumes

def run_test():
    return

if __name__ == '__main__':
    run_test()