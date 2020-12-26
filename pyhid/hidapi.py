import os
from ctypes import *

# Define the structures that belong to hidapi
class hid_device_info(Structure):
    pass

hid_device_info._fields_ = \
[
    ("path", c_char_p),
    ("vendor_id", c_ushort),
    ("product_id", c_ushort),
    ("serial_number", c_wchar_p),
    ("release_number", c_ushort),
    ("manufacturer_string", c_wchar_p),
    ("product_string", c_wchar_p),
    ("usage_page", c_ushort),
    ("usage", c_ushort),
    ("interface_number", c_int),
    ("next", POINTER(hid_device_info)),
]

class hid_device(Structure):
    pass

# Load the hidapp.dll library
pathOfScript = os.path.realpath(__file__)
pathToDll = os.path.dirname(pathOfScript) + "/lib/hidapi.dll"
_loadedDll = WinDLL(pathToDll)

# enumerate()
_loadedDll.hid_enumerate.restype = POINTER(hid_device_info)
_loadedDll.hid_enumerate.argtypes = [c_ushort, c_ushort]

# free_enumeration()
_loadedDll.hid_free_enumeration.argtypes = [POINTER(hid_device_info)]

# hid_open()
_loadedDll.hid_open.restype = POINTER(hid_device)
_loadedDll.hid_open.argtypes = [c_ushort,c_ushort,c_wchar_p]

# hid_open_path
_loadedDll.hid_open_path.restype = POINTER(hid_device)
_loadedDll.hid_open_path.argtypes = [c_char_p]

# hid_close
_loadedDll.hid_close.argtypes = [POINTER(hid_device)]

# hid_set_nonblocking
_loadedDll.hid_set_nonblocking.argtypes = [POINTER(hid_device), c_int]

# hid_read
_loadedDll.hid_read.argtypes = [POINTER(hid_device), POINTER(c_ubyte), c_size_t]

# hid_read_timeout
_loadedDll.hid_read_timeout.argtypes = [POINTER(hid_device), POINTER(c_ubyte), c_size_t, c_int]

# hid_write
_loadedDll.hid_write.argtypes = [POINTER(hid_device), POINTER(c_ubyte), c_size_t]

# Define the python API for hidapi
def Init():
    _loadedDll.hid_init()

def Shutdown():
    _loadedDll.hid_exit()
    
def Enumerate(vendorId = 0, productId = 0):
    return _loadedDll.hid_enumerate(vendorId, productId)

def FreeEnumeration(enumeration):
    _loadedDll.hid_free_enumeration(enumeration)

def Open(vendorId, productId, serialNumber = None):
    return _loadedDll.hid_open(vendorId, productId, serialNumber);

def OpenPath(path):
    return _loadedDll.hid_open_path(path);
    
def Close(device):
    _loadedDll.hid_close(device)

def CreateBuffer(size):
    bufferType = c_ubyte * size
    return bufferType()

def ZeroBuffer(buffer):
    memset(buffer, 0, len(buffer))

def SetNonBlocking(device, nonblocking = True):
    _loadedDll.hid_set_nonblocking(device, nonblocking)

def Read(device, buffer):
    return _loadedDll.hid_read(device, buffer, len(buffer))

def ReadTimeout(device, buffer, timeout):
    return _loadedDll.hid_read_timeout(device, buffer, len(buffer), timeout)

def Write(device, buffer):
    towrite = len(buffer) - 1
    print("Writing " + str(towrite) + " bytes to hid device")
    return _loadedDll.hid_write(device, buffer, towrite)