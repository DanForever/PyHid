from . import hidapi

class Device:
    def __init__(self, path = None, vendor_id = None, product_id = None, serial_number = None):
        self.path = path
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.serial_number = serial_number
        
        # Set the internal variable directly as we don't want to call into hidapi just yet
        self._nonblocking = False
    
    def __enter__(self):
        if(self.path is not None):
            self._handle = hidapi.OpenPath(self.path)
        elif(self.vendor_id is not None and self.product_id is not None):
            print("pie")
            self._handle = hidapi.Open(self.vendor_id, self.product_id, self.serial_number)
        else:
            raise Exception("No valid parameters specified for device connection")
            
        if(not self._handle):
            raise Exception("Failed to connect to device")
            
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        print("Device Exit!")
        print(exc_value)
        hidapi.Close(self._handle)
        
    @property
    def nonblocking(self):
        return self._nonblocking
        
    @nonblocking.setter
    def nonblocking(self, value):
        self._nonblocking = value
        hidapi.SetNonBlocking(self._handle, self.nonblocking)
        
    def write(self, buffer):
        return hidapi.Write(self._handle, buffer._instance)
        
    def read(self, buffer):
        return hidapi.Read(self._handle, buffer._instance)