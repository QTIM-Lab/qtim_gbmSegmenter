""" This is a wrapper script for BRAINSFit registration by 3D Slicer. In the future, there could be an all-Python
    implementation of registration in this function. In the meantime, one will need 3D Slicer (or a Docker container
    with 3DSlicer inside).
"""

import glob
import os
import fnmatch

from subprocess import call
from shutil import copyfile

def BRAINSFit_register(input_volumes, output_filenames, fixed_volume, transform_type='Rigid,ScaleVersor3D,ScaleSkewVersor3D,Affine', transform_mode = 'useMomentsAlign', interpolation_mode = 'Linear', sampling_percentage = .06):

    return_filenames = {}

    fixed_volume = input_volumes['T2']

    for key, moving_volume in input_volumes.iteritems():

        if fixed_volume == moving_volume:
            print 'Cannot register a volume to itself! Copying over and skipping this volume...'
            copyfile(fixed_volume, output_filenames[key])
            return_filenames[key] = output_filenames[key]

        BRAINSFit_base_command = ['Slicer', '--launch', 'BRAINSFit', '--fixedVolume', '"' + fixed_volume + '"', '--transformType', transform_type, '--initializeTransformMode', transform_mode, '--interpolationMode', interpolation_mode, '--samplingPercentage', str(sampling_percentage)]

        BRAINSFit_specific_command = BRAINSFit_base_command + ['--movingVolume',moving_volume,'--outputVolume',output_filenames[key]]

        try:
            print '\n'
            print 'Using 3DSlicer\'s BRAINSFit to register ' + moving_volume + ' to ' + fixed_volume + '...'
            call(' '.join(BRAINSFit_specific_command), shell=True)
            return_filenames[key] = output_filenames[key]
        except:
            print 'BRAINSFit failed for file ' + moving_volume

    return return_filenames

def execute(input_volumes, output_filenames, specific_function, params):

    if specific_function == 'slicer_registration':
        return BRAINSFit_register(*[input_volumes, output_filenames] + params)
    else:
        print 'There is no registration method associated with this keyword: ' + specific_function + '. Skipping volume located at...' + input_volume

# def run_test():

#     Slicer_Path = '"C:/Users/azb22/Documents/Software/SlicerNightly/Slicer 4.6.0/Slicer.exe"'
#     fixed_volume = 'C:/Users/azb22/Documents/Scripting/Tata_Hospital/Drawn_ROI_TestFiles/7_Ax_T2_PROPELLER.nii.gz'
#     moving_folder = 'C:/Users/azb22/Documents/Scripting/Tata_Hospital/Drawn_ROI_TestFiles/'
#     output_folder = 'C:/Users/azb22/Documents/Scripting/Tata_Hospital/Drawn_ROI_TestFiles/Registered_Volumes/'

#     register_to_one(fixed_volume, Slicer_Path, moving_folder, '_r_T2',output_folder)

#     return

if __name__ == "__main__":
    run_test()
