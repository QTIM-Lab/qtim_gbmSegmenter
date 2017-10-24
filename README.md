![Alt text](./package_resources/logos/qtim_gbmSegmenter.PNG?raw=true "qtim_gbmSegmenter")

# qtim_gbmSegmenter
This Github repository contains a nvidia-Docker container and full code/resources for pre-processing and segmenting medical imaging data for the case of glioblastoma (GBM). It takes as input four volumes (T2, T1 pre-contrast, T1 post-contrast, and FLAIR), and outputs segmentations for peritumoral edema and contrast-enhancing tumor. These segmentations are created from models trained by deep neural networks on hundreds of public and private datasets of pre-operative high- and low-grade GBMs. It also pre-processed the input data by performing bias correction, resampling to isotropic resolution, and coregistration. This repository was developed at the Quantitative Tumor Imaging Lab at the Martinos Center (MGH, MIT/Harvard HST).

## Table of Contents
- [Installation](#installation) 
- [Docker Usage](#docker-usage)
- [Python Wrapper Usage](#python-wrapper-usage)
- [Contact](#contact)

## Installation

1. Pull the qtim_gbmSegmenter Docker container from https://hub.docker.com/r/qtimlab/qtim_gbmsegmenter/.

2. Install the Docker Engine Utility for NVIDIA GPUs, AKA nvidia-docker. You can find installation instructions at their Github page, here: https://github.com/NVIDIA/nvidia-docker

3. If you want to inspect the code, or run your Docker container with an easy-to-use python wrapper, clone this repository ("git clone https://github.com/QTIM-Lab/qtim_gbmSegmenter").

## Docker Usage

Each qtim_gbmSegmenter command will take the same basic format:

```
nvidia-docker run --rm -v [MOUNTED_DIRECTORY]:/INPUT_DATA qtimlab/qtim-gbmsegmenter segment docker_pipeline <T2> <T1pre> <T1post> <FLAIR> <output_folder> [-gpu_num <int> -niftis -nobias -preprocessed -keep_outputs]
```

All input folders (T2_Folder, Output_Folder, etc.) are presumed to be located in MOUNTED_DIRECTORY. Note that the filepaths you provide in the parameters for this function have to be specifally formatted to be launched from nvidia-docker -- see more details in the Example section below.

An brief explanation of parameters after docker_pipeline follows.

* T2, T1pre, T1post, FLAIR: Filepaths to DICOM folders. Can be filepaths to niftis if the -niftis flag is set.
* output_folder: A filepath to your output folder. This folder will be created if it does not already exist.
* -gpu_num: Which CUDA GPU ID # to use.
* -niftis: Input nifti files instead of DIOCM folders.
* -nobias: Skip the bias correction step.
* -preprocessed: Skip bias correction, resampling, and registration.
* -keep_outputs: Do not delete files generated from intermediary steps.

### Example

Let's say you stored some DICOM data on your computer at the path /home/my_user/Data/, and wanted to segment data located at /home/my_user/Data/Patient_1. The nvidia-docker command would look like this:

```
nvidia-docker run --rm -v /home/my_user/Data:/INPUT_DATA qtimlab/qtim-gbmsegmenter segment pipeline Patient_1/T2 Patient_1/T1pre Patient_1/T1post Patient_1/FLAIR Patient_1/Output_Folder
```

First, note that the "/INPUT_DATA" designation on the right-hand side of the "-v" option will never change. "INPUT_DATA" is a folder within the Docker container that will not change between runs.

Second, note that you will need to make sure that the left-hand side of the "-v" option is an absolute, rather than relative, path. For example "../Data/" and "~/Data/" will not work (relative path), but "/home/my_user/Data/" will work (absolute path, starting from the root directory).

Third, note that the folders you provide as arguments to the "segment pipeline" command should be relative paths. This is because you are mounting, and thus renaming, a folder on your system to the "/INPUT_DATA" folder inside the Docker system. For example, if you were mounting the directory "/home/my_user/Data/" to "/INPUT_DATA", you should not provide the path "/home/my_user/Data/Patient_1/T2" as a parameter. Rather, you should provide the path "Patient_1/T2", as those parts of the path are within the scope of your mounted directory.

## Python Wrapper Usage

Given the filepath rules above, you may want to avoid using nvidia-docker directly. I've also created a python utility that wraps around the nvidia-docker command above, and is slightly easier to use. In order to use this utlity, you will need to clone this repository. ("git clone https://github.com/QTIM-Lab/qtim_gbmSegmenter"), and install it ("python setup.py install", in the directory you cloned the repository).

Once you have installed the repository, you can use the following command on the command-line:

```
segment pipeline <T2> <T1pre> <T1post> <FLAIR> <output_folder> [-gpu_num <int> -niftis -nobias -preprocessed -keep_outputs]
```

Here are some details about what each of those parameters mean.

* T2, T1pre, T1post, FLAIR: Filepaths to DICOM folders. Can be filepaths to niftis if the -niftis flag is set.
* output_folder: A filepath to your output folder. This folder will be created if it does not already exist.
* -gpu_num: Which CUDA GPU ID # to use.
* -niftis: Input nifti files instead of DICOM folders.
* -nobias: Skip the bias correction step.
* -preprocessed: Skip bias correction, resampling, and registration.
* -keep_outputs: Do not delete files generated from intermediary steps.

## Contact

This docker container is under active development, and you may run into errors or desire additional features. Send any questions or requests for methods to abeers@mgh.harvard.edu. You can also submit a Github "issue" if you run into a bug. Otherwise, happy segmenting!
