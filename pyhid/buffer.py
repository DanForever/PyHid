from ctypes import *

class Buffer:
    def __init__(self, size):
        self.size = size
        self._type = c_ubyte * self.size
        self._instance = self._type()
        
    def __len__(self):
        return self.size
        
    def __getitem__(self, key):
        return self._instance[key]
        
    def __setitem__(self, key, value):
        self._instance[key] = value