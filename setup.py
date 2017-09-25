from setuptools import setup, find_packages
from codecs import open
from os import path

# with open(path.join('./', 'README.md'), encoding='utf-8') as f:
    # long_description = f.read()

#with open('requirements.txt') as f:
#    required = f.read().splitlines()

setup(
  name = 'qtim_gbmSegmenter',
  # packages = ['qtim_tools'], # this must be the same as the name above
  version = '0.1.1',
  description = 'Test',
  packages = find_packages(),
  entry_points =  {
                  "console_scripts": ['segment = qtim_gbmSegmenter.__main__:main'], 
                  },
  author = 'Andrew Beers',
  author_email = 'abeers@mgh.harvard.edu',
  url = 'https://github.com/QTIM-Lab/qtim_gbmSegmenter', # use the URL to the github repo
  keywords = ['neuroimaging', 'niftis', 'nifti','mri','dce','dsc','ktrans','ve','tofts','machine learning','vision','texture','learning'], # arbitrary keywords
  install_requires=['pydicom'],
  classifiers = [],
)