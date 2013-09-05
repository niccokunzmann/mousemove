import sys
import traceback
import tkinter.messagebox
from .files import error_report_file

def report_exc():
    return report_exception(*sys.exc_info())

def report_exception(ty, err, tb):
    with error_report_file() as file:
        traceback.print_exception(ty, err, tb, file = file)
    tkinter.messagebox.showerror(ty.__name__, str(err) + \
                                 '\nThe full error was saved to\n' +
                                 file.name)
    return err.with_traceback(tb)



__all__ = 'report_exc report_exception'.split()
