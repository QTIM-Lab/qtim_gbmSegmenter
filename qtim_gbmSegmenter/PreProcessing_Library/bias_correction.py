from subprocess import call

def N4_Bias_Correct(input_volumes, output_filenames):
    
    # Note - include head radius and center options in the future.

    return_filenames = {}

    for key, input_volume in input_volumes.iteritems():

        n4bias_base_command = ['N4BiasFieldCorrection']

        n4bias_specific_command = n4bias_base_command + ['-i', input_volume, '-o', output_filenames[key]]

        try:
            print 'Using ANTs\' N4BiasCorrection to correct intensity inhomgeneities from ' + input_volume + ' to output volume ' + output_filenames[idx] + '...'
            call(' '.join(n4bias_specific_command), shell=True)
            return_filenames[key] = output_filenames[key]
        except:
            print 'ANTs N4BiasCorrection failed for file ' + input_volume

        return return_filenames

def execute(input_volumes, output_filenames, specific_function, params):

    if specific_function == 'ants_n4_bias':
        return N4_Bias_Correct(*[input_volumes, output_filenames] + params)
    else:
        print 'There is no bias correction program associated with this keyword: '  + specific_function +  '. Skipping volume located at...' + input_volumes
        return None

def run_test():
    return

if __name__ == '__main__':
    run_test()