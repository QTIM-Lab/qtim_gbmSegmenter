from qtim_gbmSegmenter.Config_Library.docker_wrapper import docker_segmentation

T2 = '/home/user/input_folder/T2'
T1 = '/home/user/input_folder/T1'
T1POST = '/home/user/input_folder/T1POST'
FLAIR = '/home/user/input_folder/FLAIR'
OUTPUT = '/home/user/output_folder'

docker_segmentation(T2, T1, T1POST, FLAIR, OUTPUT)