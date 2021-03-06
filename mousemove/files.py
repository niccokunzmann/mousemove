import tempfile
import os
import os.path
import shutil
import time
import threading

try: from . import constants
except SystemError: import constants

from threading import Lock

_tempfilenamelock = Lock()
def tempfilename(suffix = '', prefix = ''):
    with _tempfilenamelock:
        return tempfile.mktemp(suffix, 'Stronghold Kingdoms Bot' + os.sep + prefix)

def delete_old_tempfiles():
    path = os.path.dirname(tempfilename())
    deadline = time.time() - 6 * 60 * 60 # 6 hours
    if not os.path.isdir(path):
        os.mkdir(path)
    files = os.listdir(path)
    for filename in files:
        filepath = os.path.join(path, filename)
        try:
            if os.path.getmtime(filepath) < deadline:
                if os.path.isfile(filepath):
                    os.remove(filepath)
                else:
                    shutil.rmtree(filepath)
        except (FileNotFoundError, PermissionError): pass

delete_old_tempfiles_thread = threading.Thread(target = delete_old_tempfiles)
delete_old_tempfiles_thread.setDaemon(True)
delete_old_tempfiles_thread.start()

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

def screenshot_script_path():
    return os.path.join(os.path.dirname(__file__), '_screenshot script.py')

__all__ = 'tempfilename image_folder forschungsordner config_file_name '\
          'error_report_file screenshot_script_path delete_old_tempfiles '\
          'delete_old_tempfiles_thread'.split()
