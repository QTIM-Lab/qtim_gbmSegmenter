
import numpy as np
import os
import glob
import re
import fnmatch
import shutil

import qtim_gbmSegmenter.PreProcessing_Library.normalize as normalize
import qtim_gbmSegmenter.PreProcessing_Library.import_dicom as import_dicom
import qtim_gbmSegmenter.PreProcessing_Library.crop as crop
import qtim_gbmSegmenter.PreProcessing_Library.bias_correction as bias_correction
import qtim_gbmSegmenter.PreProcessing_Library.resample as resample
import qtim_gbmSegmenter.PreProcessing_Library.skull_strip as skull_strip
import qtim_gbmSegmenter.PreProcessing_Library.registration as registration
import qtim_gbmSegmenter.PreProcessing_Library.segmentation as segmentation

preprocessing_dictionary = {
    'dicom_convert': import_dicom,
    'resample': resample,
    'bias_correct': bias_correction,
    'crop': crop,
    'register': registration,
    'skull_strip': skull_strip,
    'normalize': normalize,
    'segment': segmentation
}

def grab_files(location_list, file_regex='*', exclusion_regex=''):

    if isinstance(location_list, basestring):
        location_list = [location_list]
    
    output_volumes = []
    for input_volume_item in location_list:
        if os.path.isdir(input_volume_item):
            output_volumes += glob.glob(os.path.join(input_volume_item, file_regex))
        else:
            output_volumes += [input_volume_item]

    if exclusion_regex != '':
        output_volumes = [filepath for filepath in output_volumes if exclusion_regex not in os.path.basename(os.path.normpath(filepath))]

    return output_volumes

def grab_folders_recursive(input_folders, file_regex, exclusion_regex):

    if isinstance(input_folders, basestring):
        input_folders = [input_folders]

    output_folders = []

    for input_folder in input_folders:
        
        lowest_dirs = []

        for root,dirs,files in os.walk(input_folder):
            if files and not dirs:
                end_root = os.path.basename(os.path.normpath(root))
                if fnmatch.fnmatch(end_root, file_regex) and (exclusion_regex not in end_root or exclusion_regex == ''):
                    lowest_dirs.append(root)

        output_folders += lowest_dirs

    return output_folders

def grab_output_filepath(input_volume, output_folder, output_suffix = '', make_dir = True):
    
    if output_folder == '':
        output_folder = os.path.dirname(input_volumes)
    elif not os.path.exists(output_folder) and make_dir:
        os.makedirs(output_folder)

    no_path = os.path.basename(os.path.normpath(input_volume))
    file_prefix = str.split(no_path, '.nii')

    output_filename = os.path.join(output_folder, file_prefix[0] + output_suffix + '.nii' + file_prefix[-1])

    return output_filename

def grab_output_filepath_folder(input_volume, output_folder, output_suffix = '', make_dir = True):
    
    if output_folder == '':
        output_folder = os.path.dirname(input_volume)
    elif not os.path.exists(output_folder) and make_dir:
        os.makedirs(output_folder)

    no_path = os.path.basename(os.path.normpath(input_volume))

    output_filename = os.path.join(output_folder, no_path + output_suffix + '.nii.gz')

    return output_filename

def clear_directories(input_directories):

    if isinstance(input_directories, basestring):
        input_directories = [input_directories]

    for directory in input_directories:
        if os.path.isdir(directory):
            shutil.rmtree(directory)

def move_files_recursive(input_filepaths, file_regex='*', exclusion_regex='', output_folder='', output_suffix='', make_dir = True):

    file_list = grab_files(input_filepaths, file_regex, exclusion_regex)

    for move_file in file_list:
        
        output_filepath = grab_output_filepath(move_file, output_folder, output_suffix, make_dir)

        os.rename(move_file, output_filepath)

def move_files_unique_folder(input_filepaths, output_base_directory, file_regex='*', exclusion_regex='', output_suffix='', separator='_', prefix_segments=1, make_dir = True):
    
    file_list = grab_files(input_filepaths, file_regex, exclusion_regex)

    for move_file in file_list:

        if not os.path.isdir(move_file):

            output_folder = os.path.join(output_base_directory, separator.join(str.split(os.path.basename(os.path.normpath(move_file)), separator)[0:prefix_segments]))
            
            output_filepath = grab_output_filepath(move_file, output_folder, output_suffix, make_dir)

            os.rename(move_file, output_filepath)

def execute(preprocess_step, input_files, input_search_phrase, input_exclusion_phrase, output_folder, output_suffix, method, params):

    output_filenames = {}

    if preprocess_step in ['dicom_convert']:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        output_filenames = output_folder
    else:
        for key in input_files:
            output_filenames[key] = os.path.abspath(grab_output_filepath(input_files[key], output_folder, output_suffix, make_dir=True))
            input_files[key] = os.path.abspath(input_files[key])

    return_filenames = preprocessing_dictionary[preprocess_step].execute(input_files, output_filenames, method, params)

    return return_filenames

def run_test():
    return

if __name__ == '__main__':
    run_test()