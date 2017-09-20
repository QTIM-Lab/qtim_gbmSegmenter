import os
import glob

from subprocess import call

def resample_slicer(input_volumes, output_filenames, dimensions=[1,1,1], interpolation_mode = 'linear'):

    return_filenames = []

    for idx, input_volume in enumerate(input_volumes):

        ResampleVolume_base_command = ['Slicer', '--launch', 'ResampleScalarVolume', '-i', interpolation_mode]

        ResampleVolume_base_command += ['-s', str(dimensions).strip('[]').replace(' ', '')]

        ResampleVolume_specific_command = ResampleVolume_base_command + [input_volume, output_filenames[idx]]
        
        print ' '.join(ResampleVolume_specific_command)

        try:
            print '\n'
            print 'Using 3DSlicer\'s ResampleVolume to resample ' + input_volume + ' to ' + str(dimensions) + '...'
            call(' '.join(ResampleVolume_specific_command), shell=True)
            return_filenames += [output_filenames[idx]]
        except:
            print '3DSlicer\'s resample volume failed for file ' + input_volume

    return return_filenames

def execute(input_volumes, output_filenames, specific_function, params):

    if specific_function == 'slicer_resample':
        return resample_slicer(*[input_volumes, output_filenames] + params)
    else:
        print 'There is no resampling method associated with this keyword: ' + specific_function + '. Skipping volume located at...' + input_volumes
        return None

def run_test():
    return

if __name__ == '__main__':
    run_test()