def full_pipeline(T2_folder, T1_folder, T1POST_folder, FLAIR_folder, final_output_folder, nobias, niftis):

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

    T2_folder = os.path.join('./INPUT_DATA', T2_folder)
    T1_folder = os.path.join('./INPUT_DATA', T1_folder)
    T1POST_folder = os.path.join('./INPUT_DATA', T1POST_folder)
    FLAIR_folder = os.path.join('./INPUT_DATA', FLAIR_folder)
    final_output_folder = os.path.join('./INPUT_DATA', final_output_folder)
    
    # --------------------------------------------------------------------#
    # DICOM Conversion Step
    # Available methods: 'python_convert'

    if not niftis:

        output_folder = './INPUT_DATA/RAW_NIFTI'

        method = 'python_convert'

        output_suffix = ''
        extra_parameters = [output_suffix, T2_folder, T1_folder, T1POST_folder, FLAIR_folder]

        output = pipeline.execute('dicom_convert', None, None, None, output_folder, output_suffix, method, extra_parameters)

    else:

        output = {'T2': T2_folder, 'T1': T1_folder, 'T1POST': T1POST_folder, 'FLAIR': FLAIR_folder}

    # #--------------------------------------------------------------------#

    # # #--------------------------------------------------------------------#
    # Modality Identification Step
    # Available methods: TBD

    # # #--------------------------------------------------------------------#

    # # #--------------------------------------------------------------------#
    # Bias Correction Step
    # Available methods: 'ants_n4_bias'

    if not nobias:

        output_folder = './INPUT_DATA/BIAS_CORRECTED_NIFTI'
        output_suffix = '_nobias'

        method = 'ants_n4_bias'

        extra_parameters = []

        output = pipeline.execute('bias_correct', output, None, None, output_folder, output_suffix, method, extra_parameters)

    # # #--------------------------------------------------------------------#

    # # #--------------------------------------------------------------------#
    # Resampling Step
    # Available methods: 'slicer_resample'

    output_folder = './INPUT_DATA/ISOTROPIC_NIFTI'
    output_suffix = '_isotropic'

    method = 'slicer_resample'

    dimensions = [1,1,1]
    interpolation_mode = 'linear'
    extra_parameters = [dimensions, interpolation_mode]

    output = pipeline.execute('resample', output, None, None, output_folder, output_suffix, method, extra_parameters)

    # #--------------------------------------------------------------------#

    # #--------------------------------------------------------------------#
    # # Registration Step
    # # Available methods: 'slicer_registration'

    output_folder = final_output_folder
    output_suffix = '_reg'

    method = 'slicer_registration'

    fixed_volume = 'T2'
    transform_type = 'Rigid,ScaleVersor3D,ScaleSkewVersor3D,Affine'
    transform_mode = 'useMomentsAlign'
    interpolation_mode = 'Linear'
    sampling_percentage = .002
    extra_parameters = [fixed_volume, transform_type, transform_mode, interpolation_mode, sampling_percentage]

    output = pipeline.execute('register', output, None, None, output_folder, output_suffix, method, extra_parameters)

    # # # #--------------------------------------------------------------------#

    # # # #--------------------------------------------------------------------#
    # # # Skull-Stripping Step
    # # # Available methods: 'deepneuro_skull_stripping'

    output_folder = './INPUT_DATA/SKULLSTRIP_NIFTI'
    output_suffix = '_ss'

    method = 'deepneuro_skull_stripping'

    output_mask_suffix = '_mask'
    extra_parameters = [output_mask_suffix]

    output = pipeline.execute('skull_strip', output, None, None, output_folder, output_suffix, method, extra_parameters)

    # # # # #--------------------------------------------------------------------#

    # # # #--------------------------------------------------------------------#
    # # # Normalizing Step
    # # # Available methods: 'zeromean_normalize'

    output_folder = './INPUT_DATA/NORMALIZED_NIFTI'
    output_suffix = '_normalized'

    method = 'zeromean_normalize'

    extra_parameters = []

    output = pipeline.execute('normalize', output, None, None, output_folder, output_suffix, method, extra_parameters)

    # # #--------------------------------------------------------------------#

    # # #--------------------------------------------------------------------#
    # # Segmentation Step
    # # Available methods: 'deepneuro_segment'

    output_folder = final_output_folder
    output_suffix = ''

    method = 'deepneuro_segment'

    output_wholetumor_name = 'wholetumor_segmentation'
    output_enhancing_name = 'enhancing_segmentation'
    extra_parameters = [output_wholetumor_name, output_enhancing_name]

    pipeline.execute('segment', output, None, None, output_folder, output_suffix, method, extra_parameters)

    # #--------------------------------------------------------------------#

    pipeline.clear_directories(['./INPUT_DATA/RAW_NIFTI', './INPUT_DATA/BIAS_CORRECTED_NIFTI', './INPUT_DATA/ISOTROPIC_NIFTI', './INPUT_DATA/SKULLSTRIP_NIFTI', './INPUT_DATA/NORMALIZED_NIFTI'])

    return

def dicom_convert(input_folder, output_folder):

    output_folder = os.path.join('./INPUT_DATA', output_folder)
    input_folder = os.path.join('/INPUT_DATA', input_folder)

    method = 'python_convert'

    output_suffix = ''
    extra_parameters = [output_suffix]

    output = pipeline.execute('dicom_convert', input_folder, None, None, output_folder, output_suffix, method, extra_parameters)

    return

if __name__ == '__main__':
    pass