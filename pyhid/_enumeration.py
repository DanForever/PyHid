from . import hidapi
from ._deviceinfo import *

class EnumerationIterator:
    def __init__(self, enumeratedDeviceInfo):
        self.currentItem = enumeratedDeviceInfo
        
    def __next__(self):
        self.currentItem = self.currentItem.contents.next
        
        if(not self.currentItem):
            raise StopIteration
            
        return DeviceInformation(self.currentItem)

class Enumeration:
    def __init__(self, vendorId = 0, productId = 0):
        self.vendorId = vendorId
        self.productId = productId
        
    def __enter__(self):
        self.enumeratedDeviceInfo = hidapi.Enumerate(self.vendorId, self.productId)
        return self;
        
    def __exit__(self, exc_type, exc_value, traceback):
        hidapi.FreeEnumeration(self.enumeratedDeviceInfo)
        
    def __iter__(self):
        return EnumerationIterator(self.enumeratedDeviceInfo)