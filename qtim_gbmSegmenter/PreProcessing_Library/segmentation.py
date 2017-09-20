import os
import fnmatch

from subprocess import call

from qtim_gbmSegmenter.Config_Library.step import PipelineStep
from qtim_gbmSegmenter.DeepLearningLibrary.models import skull_strip_models, evaluate_model, segmentation_models, load_old_model

def segment_deepneuro(input_volumes, output_filenames, modality_dict, output_segmentation_name):

    model_dict = segmentation_models()
    input_filenames = []

    for modality_code in ['FLAIR', 'T2', 'T1POST', 'T1PRE']:
        matches = fnmatch.filter(input_volumes, modality_dict[modality_code])
        if len(matches) == 1:
            input_filenames += [os.path.abspath(matches[0])]

    output_filename = os.path.join(os.path.dirname(output_filenames[0]), output_segmentation_name + '.nii.gz')

    print input_filenames

# try: 
    evaluate_model(load_old_model(model_dict['wholetumor']), input_filenames, os.path.abspath(output_filename), patch_shape=(32,32,32))
    return output_filename
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