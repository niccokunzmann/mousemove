from collections import UserList
import threading
from collections import namedtuple

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

    def position_at(self, index):
        return FuturePosition(self, index)

    def add_done_callback(self, callback):
        self.future.add_done_callback(lambda fut: callback(self))

class NoPositionsFoundInList(IndexError):
    pass

Position = namedtuple('Position', ('x', 'y'))

class FuturePosition:

    def __init__(self, list, index):
        assert index >= 0
        self.list = list
        self.index = index

    @property
    def x(self):
        if not self:
            raise NoPositionsFoundInList(self.list, self.index)
        return self.list[self.index].x

    @property
    def y(self):
        if not self:
            raise NoPositionsFoundInList(self.list, self.index)
        return self.list[self.index].y

    def __bool__(self):
        return  len(self.list) > self.index

    def __iter__(self):
        return iter((self.x, self.y))

    def __eq__(self, other):
        return other == tuple(self)

    def __hash__(self):
        return hash(tuple(self))

    def add_done_callback(self, callback):
        self.list.add_done_callback(lambda list: self and callback(self))

    def __reduce__(self):
        return self.__class__, (list(self.list), self.index)

__all__ = 'LazyList FutureList NoPositionsFoundInList FuturePosition'.split()
            
