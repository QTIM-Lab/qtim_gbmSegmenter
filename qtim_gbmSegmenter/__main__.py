import argparse
import sys

from qtim_gbmSegmenter.Config_Library.command_line import full_pipeline

class segmenter_commands(object):

    def __init__(self):

        parser = argparse.ArgumentParser(
            description='A number of pre-packaged command used by the Quantiative Tumor Imaging Lab at the Martinos Center',
            usage='''TBD
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
            description='Segment an image from DICOMs with all preprocessing steps included')

        parser.add_argument('T2', type=str)
        parser.add_argument('T1', type=str)
        parser.add_argument('T1POST', type=str)
        parser.add_argument('FLAIR', type=str)
        parser.add_argument('output', type=str)

        args = parser.parse_args(sys.argv[2:])
        print 'Beginning segmentation pipeline...'

        full_pipeline(args.T2, args.T1, args.T1POST, args.FLAIR, args.output)


def main():
    segmenter_commands()