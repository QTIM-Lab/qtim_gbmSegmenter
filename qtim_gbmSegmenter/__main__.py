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
            description='''segment pipeline <T2> <T1pre> <T1post> <FLAIR> <output> [-nobias -niftis]

            Segment an image from DICOMs with all preprocessing steps included.
            -nobias     Skip the bias correction step.
            -niftis     Input nifti files instead of DIOCM folders.')
                ''')

        parser.add_argument('T2', type=str)
        parser.add_argument('T1', type=str)
        parser.add_argument('T1POST', type=str)
        parser.add_argument('FLAIR', type=str)
        parser.add_argument('output', type=str)
        parser.add_argument('-nobias', action='store_true')
        parser.add_argument('-niftis', action='store_true')    

        args = parser.parse_args(sys.argv[2:])
        print 'Beginning segmentation pipeline...'

        full_pipeline(args.T2, args.T1, args.T1POST, args.FLAIR, args.output, args.nobias, args.niftis)

    def pipeline(self):
        parser = argparse.ArgumentParser(
            description='''segment pipeline <T2> <T1pre> <T1post> <FLAIR> <output> [-nobias -niftis]

            Segment an image from DICOMs with all preprocessing steps included.
            -nobias     Skip the bias correction step.
            -niftis     Input nifti files instead of DIOCM folders.')
                ''')

        parser.add_argument('T2', type=str)
        parser.add_argument('T1', type=str)
        parser.add_argument('T1POST', type=str)
        parser.add_argument('FLAIR', type=str)
        parser.add_argument('output', type=str)
        parser.add_argument('-nobias', action='store_true')
        parser.add_argument('-niftis', action='store_true')    

        args = parser.parse_args(sys.argv[2:])
        print 'Beginning segmentation pipeline...'

        dicom_convert(args.T2, args.T1, args.T1POST, args.FLAIR, args.output, args.nobias, args.niftis)


def main():
    segmenter_commands()