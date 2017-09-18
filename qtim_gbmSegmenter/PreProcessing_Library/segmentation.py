import os
import fnmatch

from subprocess import call

from qtim_gbmSegmenter.Config_Library.step import PipelineStep
from qtim_gbmSegmenter.DeepLearningLibrary.models import skull_strip_models, evaluate_model

def segment_deepneuro(input_filename, output_filename, modality_dict):

    model_dict = skull_strip_models()

    target_file = None
    for model_filename, modality_code in [[T2_input_modality, model_dict['T2']], [FLAIR_input_modality, model_dict['FLAIR']]]:
        if fnmatch.fnmatch(os.path.basename(input_filename), modality_code):
            target_file = input_filename
            target_model = model_filename

    if target_modality is None:
        print 'No modality matched for skull-stripping file: ', input_filename
        return
    
    input_filename = os.path.abspath(input_filename)

    try: 
        evaluate_model(load_old_model(target_model), os.path.abspath(input_filename), os.path.abspath(output_filename), patch_shape=(32,32,32))
        return output_filename
    except:
        print 'DeepNeuro skull-stripping failed for file ' + input_filename
        return []

def execute(input_volume, output_filename, specific_function, params):

    if specific_function == 'deepneuro_segment':
        segment_deepneuro(*[input_volume, output_filename] + params)
    else:
        print 'There is no segmentation method associated with this keyword: ' + specific_function + '. Skipping volume located at...' + input_volume

def run_test():
    return

if __name__ == '__main__':
    run_test()