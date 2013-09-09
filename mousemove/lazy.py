from collections import UserList
import threading

class LazyList(UserList):

    def __init__(self):
        self.lock = None
        super().__init__()
        self.lock = threading.Lock()
        self.lock.acquire()
    
    @property
    def data(self):
        with self.lock:
            return self.__data

    @data.setter
    def data(self, value):
        self.__data = value
        if self.lock:
            print('release lock')
            self.lock.release()

class FutureList(UserList):
    
    def __init__(self, future):
        self.future = future
        super().__init__()
    
    @property
    def data(self):
        return self.future.result()

    @data.setter
    def data(self, value):
        pass


__all__ = 'LazyList FutureList'.split()
            
