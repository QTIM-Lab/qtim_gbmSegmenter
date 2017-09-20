from subprocess import call

import glob
import os
import numpy as np
import fnmatch

from qtim_tools.qtim_utilities.format_util import convert_input_2_numpy
from qtim_tools.qtim_utilities.nifti_util import save_numpy_2_nifti

def normalize_zeromean_unitvariance(input_volumes, output_filenames, label_volume='', label_volume_search_phrase=''):

    print label_volume_search_phrase

    if label_volume == '' and label_volume_search_phrase != '':
        label_volume_results = fnmatch.filter(input_volumes, label_volume_search_phrase)
        if len(label_volume_results) == 1:
            label_volume = label_volume_results[0]
        else:
            print 'Error! Search phrase for normalization mask returned multiple results. Cancelling normalization, results printed below...'
            print label_volume_results
            return

    print label_volume

    input_volumes = [input_volume for input_volume in input_volumes if not fnmatch.fnmatch(input_volume, label_volume_search_phrase)]
    output_filenames = [input_volume for input_volume in output_filenames if not fnmatch.fnmatch(input_volume, label_volume_search_phrase)]

    print input_volumes

    return_filenames = []

    for idx, input_volume in enumerate(input_volumes):

        try:
            print 'Using python\'s Nibabel and Numpy packages to normalize intensities within a region of interest to zero mean and unit variance on volume ' + input_volume + ' to output volume ' + output_filenames[idx] + '...'

            normalize_numpy = convert_input_2_numpy(input_volume)

            if label_volume == '':
                vol_mean = np.mean(normalize_numpy)
                vol_std = np.std(normalize_numpy)
                normalize_numpy = (normalize_numpy - vol_mean) / vol_std           
            else:
                ROI_numpy = convert_input_2_numpy(label_volume)
                vol_mean = np.mean(normalize_numpy[ROI_numpy > 0])
                vol_std = np.std(normalize_numpy[ROI_numpy > 0])
                normalize_numpy = (normalize_numpy - vol_mean) / vol_std
                normalize_numpy[ROI_numpy == 0] = 0

            save_numpy_2_nifti(normalize_numpy, input_volume, output_filenames[idx])

            return_filenames += output_filenames[idx]

        except:
            print 'Zero mean and unit variance normalization failed for file ' + input_volume

    return return_filenames

def execute(input_volumes, output_filenames, specific_function, params):

    if specific_function == 'zeromean_normalize':
        return normalize_zeromean_unitvariance(*[input_volumes, output_filenames] + params)
    else:
        print 'There is no normalization method associated with this keyword: '  + specific_function +  '. Skipping volumes located at...' + input_volumes


def run_test():
    return

if __name__ == '__main__':
    run_test()