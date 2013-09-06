import tempfile
import os
import os.path
import shutil

from . import constants

def tempfilename(suffix = '', prefix = ''):
    return tempfile.mktemp(suffix, 'Stronghold Kingdoms Bot' + os.sep + prefix)

path = os.path.dirname(tempfilename())
if os.path.isdir(path):
    shutil.rmtree(path)
os.mkdir(path)

image_folder = os.path.join(os.path.dirname(__file__), 'images')
if not os.path.isdir(image_folder):
    os.mkdir(image_folder)

forschungsordner = os.path.join(image_folder, 'Forschung')


def config_file_name():
    return constants.config_file_name()

def error_report_file():
    filename = tempfilename('.txt', 'error_report_')
    file = open(filename, 'w', encoding = 'utf8')
    file.write('\ufeff')
    return file

def tesser_exe():
    return constants.tesser_exe()

__all__ = 'tempfilename image_folder forschungsordner config_file_name '\
          'error_report_file'.split()
