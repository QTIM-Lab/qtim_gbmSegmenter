from subprocess import call

import glob
import os
import numpy as np
import fnmatch

from qtim_tools.qtim_utilities.format_util import convert_input_2_numpy
from qtim_tools.qtim_utilities.nifti_util import save_numpy_2_nifti

def normalize_zeromean_unitvariance(input_volumes, output_filenames):

    return_filenames = {}

    if 'mask' in input_volumes.keys():
        label_volume = input_volumes['mask']
    else:
        label_volume = None

    for key, input_volume in input_volumes.iteritems():

        if key == 'mask':
            continue

        # try:
        print 'Using python\'s Nibabel and Numpy packages to normalize intensities within a region of interest to zero mean and unit variance on volume ' + input_volume + ' to output volume ' + output_filenames[key] + '...'

        normalize_numpy = convert_input_2_numpy(input_volume)

        if label_volume is not None:
            ROI_numpy = convert_input_2_numpy(label_volume)
            vol_mean = np.mean(normalize_numpy[ROI_numpy > 0])
            vol_std = np.std(normalize_numpy[ROI_numpy > 0])
            normalize_numpy = (normalize_numpy - vol_mean) / vol_std
            normalize_numpy[ROI_numpy == 0] = 0
        else:
            vol_mean = np.mean(normalize_numpy)
            vol_std = np.std(normalize_numpy)
            normalize_numpy = (normalize_numpy - vol_mean) / vol_std        

        save_numpy_2_nifti(normalize_numpy, input_volume, output_filenames[key])

        return_filenames[key] = output_filenames[key]

        # except:
            # print 'Zero mean and unit variance normalization failed for file ' + input_volume

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