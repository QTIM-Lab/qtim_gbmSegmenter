import argparse
import sys

from qtim_gbmSegmenter.Config_Library.command_line import full_pipeline, dicom_convert

class segmenter_commands(object):

    def __init__(self):

        parser = argparse.ArgumentParser(
            description='A number of pre-packaged command used by the Quantiative Tumor Imaging Lab at the Martinos Center',
            usage='''segment <command> [<args>]

The following commands are available:
   pipeline               Run the entire segmentation pipeline, with options to leave certain pre-processing steps out.
   dicom_2_nifti          Convert an inpute DICOM folder into a series of Nifti files.
                ''')

        parser.add_argument('command', help='Subcommand to run')
        args = parser.parse_args(sys.argv[1:2])

        if not hasattr(self, args.command):
            print 'Sorry, that\'s not one of the commands.'
            parser.print_help()
            exit(1)

        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def pipeline(self):
        parser = argparse.ArgumentParser(
            description='''segment pipeline <T2> <T1pre> <T1post> <FLAIR> <output_folder> [-nobias -niftis]

            Segment an image from DICOMs with all preprocessing steps included.
            -niftis             Input nifti files instead of DIOCM folders.
            -nobias             Skip the bias correction step.
            -preprocessed       Skip bias correction, resampling, and registration.
            -mask [file]        Provide a skull-stripping mask. If provided, no skull-stripping will be performed.
                ''')

        parser.add_argument('T2', type=str)
        parser.add_argument('T1', type=str)
        parser.add_argument('T1POST', type=str)
        parser.add_argument('FLAIR', type=str)
        parser.add_argument('output', type=str)
        parser.add_argument('-niftis', action='store_true')  
        parser.add_argument('-nobias', action='store_true')
        parser.add_argument('-preprocessed', action='store_true')
        parser.add_argument('-no_ss', action='store_true') 
        parser.add_argument('-keep_outputs', action='store_true') 

        args = parser.parse_args(sys.argv[2:])
        print 'Beginning segmentation pipeline...'

        full_pipeline(args.T2, args.T1, args.T1POST, args.FLAIR, args.output, args.niftis, args.nobias, args.preprocessed, args.no_ss, args.keep_outputs)

    def dicom_2_nifti(self):
        parser = argparse.ArgumentParser(
            description='''segment dicom_2_nifti <input_folder> <output_folder>

            Recursively convert an input folder of DICOMs into a output folder of Nifti files. File names
            are determined from the DICOM SeriesDescription tag.
                ''')

        parser.add_argument('input_folder', type=str)
        parser.add_argument('output_folder', type=str)

        args = parser.parse_args(sys.argv[2:])
        print 'Beginning segmentation pipeline...'

        dicom_convert(args.input_folder, args.output_folder)


def main():
    segmenter_commands()