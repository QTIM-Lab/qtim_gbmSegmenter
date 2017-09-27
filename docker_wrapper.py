
import os

from subprocess import call

def segmentation_docker(T2_folder, T1_folder, T1POST_folder, FLAIR_folder, final_output_folder, gpu_num=0, interactive=False, **kwargs):

    paths = [T2_folder, T1_folder, T1POST_folder, FLAIR_folder, final_output_folder]
    mounted_dir = os.path.abspath(os.path.dirname(os.path.commonprefix(paths)))

    if interactive:
        docker_command = ['nvidia-docker', 'run', '-it', '-v', mounted_dir + ':/INPUT_DATA', 'qtim_gbmsegmenter', 'bash']

    else:
        docker_command = ['nvidia-docker', 'run', '--rm', '-v', mounted_dir + ':/INPUT_DATA', 'qtim_gbmsegmenter', 'segment', 'pipeline']

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

    T2 = '/home/administrator/test_data/TMZ/T2'
    T1 = '/home/administrator/test_data/TMZ/T1'
    T1POST = '/home/administrator/test_data/TMZ/T1POST'
    FLAIR = '/home/administrator/test_data/TMZ/FLAIR'
    OUTPUT = '/home/administrator/test_data/TATA'

    T2 = '/home/administrator/test_data/TATA/T2SPACE_nobias_isotropic_reg.nii.gz'
    T1 = '/home/administrator/test_data/TATA/T1AxialPremosaicwithSAT_nobias_isotropic_reg.nii.gz'
    T1POST = '/home/administrator/test_data/TATA/T1AxialPostmosaic_nobias_isotropic_reg.nii.gz'
    FLAIR = '/home/administrator/test_data/TATA/FLAIRmosaic_nobias_isotropic_reg.nii.gz'
    OUTPUT = '/home/administrator/test_data/TATA'

    T2 = '/home/administrator/test_data/TATA/TATA_T2.nii.gz'
    T1 = '/home/administrator/test_data/TATA/TATA_T1.nii.gz'
    T1POST = '/home/administrator/test_data/TATA/TATA_T1C.nii.gz'
    FLAIR = '/home/administrator/test_data/TATA/TATA_FLAIR.nii.gz'
    OUTPUT = '/home/administrator/test_data/TATA'

    T2 = '/home/administrator/test_data/TATA/TATA_T2_nobias_isotropic_reg.nii.gz'
    T1 = '/home/administrator/test_data/TATA/TATA_T1_nobias_isotropic_reg.nii.gz'
    T1POST = '/home/administrator/test_data/TATA/TATA_T1C_nobias_isotropic_reg.nii.gz'
    FLAIR = '/home/administrator/test_data/TATA/TATA_FLAIR_nobias_isotropic_reg.nii.gz'
    OUTPUT = '/home/administrator/test_data/TATA'

    T2 = '/home/administrator/test_data/NORMALIZED_NIFTI/TATA_T2_nobias_isotropic_reg_ss_normalized.nii.gz'
    T1 = '/home/administrator/test_data/NORMALIZED_NIFTI/TATA_T1_nobias_isotropic_reg_ss_normalized.nii.gz'
    T1POST = '/home/administrator/test_data/NORMALIZED_NIFTI/TATA_T1C_nobias_isotropic_reg_ss_normalized.nii.gz'
    FLAIR = '/home/administrator/test_data/NORMALIZED_NIFTI/TATA_FLAIR_nobias_isotropic_reg_ss_normalized.nii.gz'
    OUTPUT = '/home/administrator/test_data/TATA'

    segmentation_docker(T2, T1, T1POST, FLAIR, OUTPUT, interactive=True, niftis=True, preprocessed=True, no_ss=True)

    TATA/TATA_T2_nobias_isotropic_reg.nii.gz TATA/TATA_T1_nobias_isotropic_reg.nii.gz TATA/TATA_T1C_nobias_isotropic_reg.nii.gz TATA/TATA_FLAIR_nobias_isotropic_reg.nii.gz bratstest -niftis -preprocessed