from qtim_gbmSegmenter.Config_Library.docker_wrapper import docker_segmentation

T2 = '/home/administrator/test_data/TMZ/T2'
T1 = '/home/administrator/test_data/TMZ/T1'
T1POST = '/home/administrator/test_data/TMZ/T1POST'
FLAIR = '/home/administrator/test_data/TMZ/FLAIR'
OUTPUT = '/home/administrator/test_data/TATA'

# T2 = '/home/administrator/test_data/TATA/T2SPACE_nobias_isotropic_reg.nii.gz'
# T1 = '/home/administrator/test_data/TATA/T1AxialPremosaicwithSAT_nobias_isotropic_reg.nii.gz'
# T1POST = '/home/administrator/test_data/TATA/T1AxialPostmosaic_nobias_isotropic_reg.nii.gz'
# FLAIR = '/home/administrator/test_data/TATA/FLAIRmosaic_nobias_isotropic_reg.nii.gz'
# OUTPUT = '/home/administrator/test_data/TATA'

# T2 = '/home/administrator/test_data/TATA/TATA_T2.nii.gz'
# T1 = '/home/administrator/test_data/TATA/TATA_T1.nii.gz'
# T1POST = '/home/administrator/test_data/TATA/TATA_T1C.nii.gz'
# FLAIR = '/home/administrator/test_data/TATA/TATA_FLAIR.nii.gz'
# OUTPUT = '/home/administrator/test_data/TATA'

# T2 = '/home/administrator/test_data/TATA/TATA_T2_nobias_isotropic_reg.nii.gz'
# T1 = '/home/administrator/test_data/TATA/TATA_T1_nobias_isotropic_reg.nii.gz'
# T1POST = '/home/administrator/test_data/TATA/TATA_T1C_nobias_isotropic_reg.nii.gz'
# FLAIR = '/home/administrator/test_data/TATA/TATA_FLAIR_nobias_isotropic_reg.nii.gz'
# OUTPUT = '/home/administrator/test_data/TATA'

# T2 = '/home/administrator/test_data/NORMALIZED_NIFTI/TATA_T2_nobias_isotropic_reg_ss_normalized.nii.gz'
# T1 = '/home/administrator/test_data/NORMALIZED_NIFTI/TATA_T1_nobias_isotropic_reg_ss_normalized.nii.gz'
# T1POST = '/home/administrator/test_data/NORMALIZED_NIFTI/TATA_T1C_nobias_isotropic_reg_ss_normalized.nii.gz'
# FLAIR = '/home/administrator/test_data/NORMALIZED_NIFTI/TATA_FLAIR_nobias_isotropic_reg_ss_normalized.nii.gz'
# OUTPUT = '/home/administrator/test_data/TATA'

docker_segmentation(T2, T1, T1POST, FLAIR, OUTPUT)