# qtim_gbmSegmenter
This Github repository contains a nvidia-Docker container and full code/resources for pre-processing and segmenting medical imaging data for the case of glioblastoma (GBM). It takes as input four volumes (T2, T1 pre-contrast, T1 post-contrast, and FLAIR), and outputs segmentations for peritumoral edema and contrast-enhancing tumor. These segmentations are created from models trained by deep neural networks on hundreds of public and private datasets of pre-operative high- and low-grade GBMs. It also pre-processed the input data by performing bias correction, resampling to isotropic resolution, and coregistration. This repository was developed at the Quantitative Tumor Imaging Lab at the Martinos Center (MGH, MIT/Harvard HST).

# Usage

1. Pull the qtim_gbmSegmenter Docker container from https://hub.docker.com/r/qtimlab/qtim_gbmsegmenter/.

2. Install the Docker Engine Utility for NVIDIA GPUs, AKA nvidia-docker. You can find installation instructions at their Github page, here: https://github.com/NVIDIA/nvidia-docker

3. Inspect the usage data below.

Each qtim_gbmSegmenter command will take the same basic format:

```
nvidia-docker run --rm -v [MOUNTED_DIRECTORY]:/INPUT_DATA qtimlab/qtim-gbmsegmenter segment pipeline [T2_Folder] [T1pre_Folder] [T1post_Folder] [FLAIR_Folder] [Output_Folder]
```

This command will preprocess DICOM directories located at T2_Folder, T1pre_Folder, T1post_Folder, and FLAIR_folder, and output them and their segmentations to the folder located at Output_Folder.

For example, let's say you stored some DICOM data on your computer at the path /home/my_user/Data/, and wanted to segment data located at /home/my_user/Data/Patient_1. The nvidia-docker command would look like this:

```
nvidia-docker run --rm -v /home/my_user/Data:/INPUT_DATA qtimlab/qtim-gbmsegmenter segment pipeline Patient_1/T2 Patient_1/T1pre Patient_1/T1post Patient_1/FLAIR Patient_1/Output_Folder
```

Note that the "/INPUT_DATA" designation on the right-hand side of the "-v" option will never change. You will need to make sure that the left-hand side of the "-v" option is an absolute, rather than relative, path. For example "../Data/DICOMs" and "~/Data/DICOMs" will not work (relative path), but "/home/my_user/Data/DICOMs" will work (absolute path, starting from the root directory).

Unlike the mounted directory, the folders you provide as arguments to the "segment pipeline" command should be relative paths. This is because you are mounting a folder to "/INPUT_DATA" inside the Docker, and will not be able to reference that folder's original full path. For example, if you were mounting the directory "/home/my_user/Data/DICOMs/" to "/INPUT_DATA", you should not provide the path "/home/my_user/Data/DICOMs/Patient_1/T2" as a parameter. Rather, you should provide the path "Patient_1/T2", as those parts of the path are within the scope of your mounted directory. 

Send any questions or requests for methods to abeers@mgh.harvard.edu. Happy pre-processing!




