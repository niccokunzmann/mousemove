import tempfile
import os
import os.path
import shutil

try: from . import constants
except SystemError: import constants

from threading import Lock

_tempfilenamelock = Lock()
def tempfilename(suffix = '', prefix = ''):
    with _tempfilenamelock:
        return tempfile.mktemp(suffix, 'Stronghold Kingdoms Bot' + os.sep + prefix)

path = os.path.dirname(tempfilename())
if os.path.isdir(path):
    try: shutil.rmtree(path)
    except PermissionError: pass
try: os.mkdir(path)
except (PermissionError, FileExistsError): pass

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
