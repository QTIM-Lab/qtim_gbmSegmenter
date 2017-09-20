#--------------------------------------------------------------------#
# Global settings
num_processes = 1
gpu_num = 0
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
# Never change this portion, required for functioning in Docker container.
import sys
import os
import glob
sys.path.append("..")
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_num)
import qtim_gbmSegmenter.Config_Library.pipeline as pipeline
#--------------------------------------------------------------------#

output = None

#--------------------------------------------------------------------#
# DICOM Conversion Step
# Available methods: 'python_convert'

# input_files = ['./INPUT_DATA/TCGA-02-0054']

# output_folder = './INPUT_DATA/RAW_NIFTI'

# method = 'python_convert'

# output_suffix = ''
# chosen_sequences = []
# extra_parameters = [output_suffix]

# output = pipeline.execute('dicom_convert', input_files, None, None, output_folder, output_suffix, method, extra_parameters)

# # #--------------------------------------------------------------------#

# # # #--------------------------------------------------------------------#
# # Bias Correction Step
# # Available methods: 'ants_n4_bias'

# # output_folder = './INPUT_DATA/BIAS_CORRECTED_NIFTI'
# # output_suffix = '_nobias'

# # method = 'ants_n4_bias'

# # extra_parameters = []

# # output = pipeline.execute('bias_correct', output, input_contains=None, input_does_not_contain=None, output_folder, output_suffix, method, extra_parameters)

# # # #--------------------------------------------------------------------#

# # # #--------------------------------------------------------------------#
# # Resampling Step
# # Available methods: 'slicer_resample'

# if output is None:
#     output = glob.glob(os.path.join('./INPUT_DATA/BIAS_CORRECTED_NIFTI','*'))

# output_folder = './INPUT_DATA/ISOTROPIC_NIFTI'
# output_suffix = '_isotropic'

# method = 'slicer_resample'

# dimensions = [1,1,1]
# interpolation_mode = 'linear'
# extra_parameters = [dimensions, interpolation_mode]

# output = pipeline.execute('resample', output, None, None, output_folder, output_suffix, method, extra_parameters)

# # #--------------------------------------------------------------------#

# # #--------------------------------------------------------------------#
# # # Registration Step
# # # Available methods: 'slicer_registration'

# if output is None:
#     output = glob.glob(os.path.join('./INPUT_DATA/ISOTROPIC_NIFTI','*'))

# output_folder = './INPUT_DATA/REGISTERED_NIFTI'
# output_suffix = '_reg'

# method = 'slicer_registration'

# fixed_volume = ''
# fixed_volume_contains = '*T2*'
# transform_type = 'Rigid,ScaleVersor3D,ScaleSkewVersor3D,Affine'
# transform_mode = 'useMomentsAlign'
# interpolation_mode = 'Linear'
# sampling_percentage = .06
# extra_parameters = [fixed_volume, fixed_volume_contains, transform_type, transform_mode, interpolation_mode, sampling_percentage]

# output = pipeline.execute('register', output, None, None, output_folder, output_suffix, method, extra_parameters)

# # # #--------------------------------------------------------------------#

# # # #--------------------------------------------------------------------#
# # # Skull-Stripping Step
# # # Available methods: 'deepneuro_skull_stripping'

# if output is None:
#     output = glob.glob(os.path.join('./INPUT_DATA/REGISTERED_NIFTI','*'))

# output_folder = './INPUT_DATA/SKULLSTRIP_NIFTI'
# output_suffix = '_ss'

# method = 'deepneuro_skull_stripping'

# T2_input_modality = '*T2*'
# FLAIR_input_modality = '*FLAIR*' # Will prefer T2 unless unavailable.
# output_mask_suffix = '_mask'
# extra_parameters = [T2_input_modality, FLAIR_input_modality, output_mask_suffix]

# output = pipeline.execute('skull_strip', output, None, None, output_folder, output_suffix, method, extra_parameters)

# # # # #--------------------------------------------------------------------#

# # # #--------------------------------------------------------------------#
# # # Normalizing Step
# # # Available methods: 'zeromean_normalize'

# if output is None:
#     output = glob.glob(os.path.join('./INPUT_DATA/SKULLSTRIP_NIFTI','*'))

# output_folder = './INPUT_DATA/NORMALIZED_NIFTI'
# output_suffix = '_normalized'

# method = 'zeromean_normalize'

# label_volume = ''
# label_volume_contains = '*_mask*'
# extra_parameters = [label_volume, label_volume_contains]

# output = pipeline.execute('normalize', output, None, None, output_folder, output_suffix, method, extra_parameters)

# # #--------------------------------------------------------------------#

# # #--------------------------------------------------------------------#
# # Segmentation Step
# # Available methods: 'deepneuro_segment'

if output is None:
    output = glob.glob(os.path.join('./INPUT_DATA/NORMALIZED_NIFTI','*'))

output_folder = './INPUT_DATA/RAW_NIFTI'
output_suffix = ''

method = 'deepneuro_segment'

modality_dict = {'T2': '*T2*', 'FLAIR': '*FLAIR*', 'T1POST': '*POST*', 'T1PRE': '*T1_*'}
output_segmentation_name = 'segmentation'
extra_parameters = [modality_dict, output_segmentation_name]

pipeline.execute('segment', output, None, None, output_folder, output_suffix, method, extra_parameters)

# #--------------------------------------------------------------------#

# pipeline.move_files_unique_folder(input_filepaths='./INPUT_DATA/NORMALIZED_NIFTI', output_base_directory='./INPUT_DATA', separator='_', prefix_segments=1)
# pipeline.clear_directories(['./INPUT_DATA/BIAS_CORRECTED_NIFTI', './INPUT_DATA/ISOTROPIC_NIFTI', './INPUT_DATA/REGISTERED_NIFTI', './INPUT_DATA/SKULLSTRIP_NIFTI', './INPUT_DATA/NORMALIZED_NIFTI'])