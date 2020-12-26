from ._device import *

class DeviceInformation:
    def __init__(self, rawDeviceInfo):
        self._rawDeviceInfo = rawDeviceInfo
        
    def __getattr__(self, name):
        return object.__getattribute__(self._rawDeviceInfo.contents, name)
        
    def connect(self):
        return Device(self.path)