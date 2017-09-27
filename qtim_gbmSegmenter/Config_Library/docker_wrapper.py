
import os

from subprocess import call

def docker_segmentation(T2_folder, T1_folder, T1POST_folder, FLAIR_folder, final_output_folder, gpu_num=0, interactive=False, **kwargs):

    paths = [T2_folder, T1_folder, T1POST_folder, FLAIR_folder, final_output_folder]
    mounted_dir = os.path.abspath(os.path.dirname(os.path.commonprefix(paths)))

    if interactive:
        docker_command = ['nvidia-docker', 'run', '-it', '-v', mounted_dir + ':/INPUT_DATA', 'qtim_gbmsegmenter', 'bash']

    else:
        docker_command = ['nvidia-docker', 'run', '--rm', '-v', mounted_dir + ':/INPUT_DATA', 'qtim_gbmsegmenter', 'segment', 'docker_pipeline']

        for path in paths:
            docker_command += [os.path.abspath(path).split(mounted_dir,1)[1][1:]]

        docker_command += ['-gpu_num', str(gpu_num)]

        if kwargs is not None:
            for key, value in kwargs.iteritems():
                if value:
                    docker_command += ['-' + str(key)]

    print ' '.join(docker_command)
    call(' '.join(docker_command), shell=True)

def queue_dockers(commands, gpu_list):

    return

if __name__ == '__main__':

    pass