import sys
import threading
try:
    from threading import get_ident
except ImportError:
    from thread import get_ident
import linecache
import time

SECONDS_FROZEN = 120 # seconds
TESTS_PER_SECOND = 1

def frame2string(frame):
    # from module traceback
    lineno = frame.f_lineno # or f_lasti
    co = frame.f_code
    filename = co.co_filename
    name = co.co_name
    s = '  File "{}", line {}, in {}'.format(filename, lineno, name)
    line = linecache.getline(filename, lineno, frame.f_globals).lstrip()
    return s + '\n\t' + line

def thread2list(frame):
    l = []
    while frame:
        l.insert(0, frame2string(frame))
        frame = frame.f_back
    return l

def monitor():
    self = get_ident()
    old_threads = {}
    while TESTS_PER_SECOND != 0:
        time.sleep(1. / TESTS_PER_SECOND)
        now = time.time()
        then = now - SECONDS_FROZEN
        frames = sys._current_frames()
        new_threads = {}
        for frame_id, frame in frames.items():
            new_threads[frame_id] = thread2list(frame)
        for thread_id, frame_list in new_threads.items():
            if thread_id == self: continue
            if thread_id not in old_threads or \
               frame_list != old_threads[thread_id][0]:
                new_threads[thread_id] = (frame_list, now)
            elif old_threads[thread_id][1] < then:
                print_frame_list(frame_list, frame_id)
            else:
                new_threads[thread_id] = old_threads[thread_id]
        old_threads = new_threads

def stdout_string(frame_list, frame_id):
    return '-' * 20 + \
           'Thread {}'.format(frame_id).center(20) + \
           '-' * 20 + \
           '\n' + \
           ''.join(frame_list)

printed_stacks = []

def print_frame_list(frame_list, frame_id):
    if (frame_list, frame_id) not in printed_stacks:
        string = stdout_string(frame_list, frame_id)
        sys.stderr.write(string)
        printed_stacks.append((frame_list, frame_id))

def start_monitoring():
    '''After hanging SECONDS_FROZEN the stack trace of the deadlock is printed automatically.'''
    thread = threading.Thread(target = monitor, daemon = True)
    thread.start()
    return thread

monitoring_thread = start_monitoring()

if __name__ == '__main__':
    SECONDS_FROZEN = 1
    time.sleep(3) # TEST
