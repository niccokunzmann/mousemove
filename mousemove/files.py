import tempfile
import os
import os.path
from . import constants

def tempfilename(suffix = ''):
    return tempfile.mktemp(suffix, 'Stronghold Kingdoms Bot' + os.sep)

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

__all__ = 'tempfilename image_folder forschungsordner config_file_name'.split()
