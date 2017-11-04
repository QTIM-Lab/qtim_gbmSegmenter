
import os

from subprocess import call

def docker_segmentation(gpu_num=0, interactive=False, **kwargs):

    path_codes = ['T2', 'T1', 'T1POST', 'FLAIR', 'output']
    mounted_dir = os.path.abspath(os.path.dirname(os.path.commonprefix([kwargs[code] for code in path_codes])))
    for code in path_codes:
        print kwargs[code]
        kwargs[code] = os.path.abspath(kwargs[code]).split(mounted_dir,1)[1][1:]
        print kwargs[code]

    if gpu_num is None:
        gpu_num = '0'

    if interactive:
        docker_command = ['nvidia-docker', 'run', '-it', '-v', mounted_dir + ':/INPUT_DATA', 'qtim_gbmsegmenter', 'bash']

    else:
        docker_command = ['nvidia-docker', 'run', '--rm', '-v', mounted_dir + ':/INPUT_DATA', 'qtim_gbmsegmenter', 'segment', 'docker_pipeline']

        docker_command += ['-gpu_num', str(gpu_num)]

        if kwargs is not None:
            for key, value in kwargs.iteritems():
                if value == True:
                    docker_command += ['-' + str(key)]
                else:
                    docker_command += ['-' + str(key) + ' ' + value]

    print ' '.join(docker_command)
    call(' '.join(docker_command), shell=True)

def queue_dockers(commands, gpu):

    for command in commands:
        docker_segmentation(T2=command['T2'], T1=command['T1'], T1POST=command['T1POST'], FLAIR=command['FLAIR'], output=command['final_output_folder'], gpu_num=gpu, niftis=True, preprocessed=True, keep_outputs=True)

    return

if __name__ == '__main__':

    pass