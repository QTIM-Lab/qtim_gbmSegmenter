import Scripts.Slicer_Import_Dicom

import os
import glob
import inspect
import dicom
import qtim_tools


from subprocess import call, check_output
from qtim_tools.qtim_utilities.dicom_util import dcm_2_numpy, dcm_2_nifti

# def mri_convert(dicom_folder, output_filename):

#     if os.path.isdir(dicom_folder):
#         dicom_volume = os.path.join(dicom_folder, os.listdir(dicom_folder)[0])

#     mri_convert_base_command = ['mri_convert']

#     mri_probedicom_patient_id_command = ['mri_probedicom', '--i', dicom_volume, '--t', '10', '20']
#     mri_probedicom_series_description_command = ['mri_probedicom', '--i', dicom_volume, '--t', '08', '103e']

#     try:
#         print '\n'
#         print 'Using freesurfer\'s mri_convert to convert DICOM into nifti for folder... ' + dicom_folder
        
#         patient_id = check_output(mri_probedicom_patient_id_command).rstrip().replace(' ', '')
#         series_description = check_output(mri_probedicom_series_description_command).rstrip().replace(' ', '')

#         output_directory = os.path.dirname(output_filename)

#         mri_convert_specific_command = mri_convert_base_command + [dicom_volume, os.path.join(output_directory, patient_id + '_' + series_description + '.nii.gz')]

#         call(' '.join(mri_convert_specific_command), shell=True)

#     except:
#         print 'Converting DICOM into nifti failed for file ' + dicom_volume + 'and output file ' + output_filename

#     return

# def slicer_convert(dicom_folder, output_filename):

#     dicom_script_filepath = os.path.normpath(inspect.getfile(Scripts.Slicer_Import_Dicom)).replace('\\','/')
#     if '.pyc' in dicom_script_filepath:
#         dicom_script_filepath = dicom_script_filepath[0:-1]

#     DICOM_import_base_command = ['Slicer', '--no-main-window', '--disable-cli-modules', '--python-script', dicom_script_filepath]
#     DICOM_import_specific_command = DICOM_import_base_command + ['-i',os.path.abspath(os.path.normpath(dicom_folder)),'-o',os.path.abspath(os.path.normpath(output_filename))]

#     try:
#         print '\n'
#         print 'Using 3DSlicer\'s Dicom Importer to convert DICOM into nifti for folder... ' + dicom_folder
#         call(' '.join(DICOM_import_specific_command), shell=True)
#     except:
#         print 'Converting DICOM into nifti failed for file ' + dicom_volume + 'and output file ' + output_filename

#     return

def python_convert(dicom_folders, output_directory, output_suffix='', T2_folder=None, T1_folder=None, T1POST_folder=None, FLAIR_folder=None, use_series_descriptions=None, T2_contains=None, T1_contains=None, T1POST_contains=None, FLAIR_contains=None):

    return_filenames = {}
    modality_keys = ['T2', 'T1', 'T1POST', 'FLAIR']

    if not use_series_descriptions:

        for idx, folder in enumerate([T2_folder, T1_folder, T1POST_folder, FLAIR_folder]):

            print folder, output_directory

            return_filenames[modality_keys[idx]] = os.path.abspath(dcm_2_nifti(folder, output_directory, suffix=output_suffix)[0])

    else:

        output_filenames = dcm_2_nifti(folder, output_directory, suffix=output_suffix)

        for idx, folder in enumerate([T2_contains, T1_contains, T1POST_contains, FLAIR_contains]):
            for file in output_filenames:
                if fnmatch.fnmatch(file, regex):
                    return_filenames[modality_keys[idx]] = os.path.abspath(file)

    return return_filenames

    pass

def execute(input_volumes, output_filenames, specific_function, params):

    if specific_function == 'freesurfer_mri_convert':
        mri_convert(*[input_volumes, output_filenames] + params)
    elif specific_function == 'slicer_convert':
        slicer_convert(*[input_volumes, output_filenames] + params)       
    elif specific_function == 'python_convert':
        return python_convert(*[input_volumes, output_filenames] + params)       
    else:
        print 'There is no conversion method associated with this keyword: ' + specific_function + '. Skipping volume located at...' + input_volume

def run_test():
    return

if __name__ == '__main__':
    run_test()