from . import hidapi

class HidConnectionError(Exception):
    pass

class Device:
    def __init__(self, path = None, vendor_id = None, product_id = None, serial_number = None):
        self.path = path
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.serial_number = serial_number
        
        self._handle = None
        
        # Set the internal variable directly as we don't want to call into hidapi just yet
        self._nonblocking = False
    
    def connect(self):
        if(self.path is not None):
            self._handle = hidapi.OpenPath(self.path)
        elif(self.vendor_id is not None and self.product_id is not None):
            self._handle = hidapi.Open(self.vendor_id, self.product_id, self.serial_number)
        else:
            raise ValueError("Either 'path', or 'vendor_id' and 'product_id' must be specified in order to connect to a human interface device")
            
        if(not self._handle):
            raise HidConnectionError("Failed to connect to device")
        
    def try_connect(self) -> bool:
        try:
            self.connect()
        except HidConnectionError as error:
            print(error)
            return False
            
        return True
    
    def disconnect(self):
        hidapi.Close(self._handle)
        self._handle = None
    
    def __enter__(self):
        self.connect()
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        print("Device Exit!")
        print(exc_value)
        self.disconnect()
        
    @property
    def connected(self):
        return self._handle is not None
        
    @property
    def nonblocking(self):
        return self._nonblocking
        
    @nonblocking.setter
    def nonblocking(self, value):
        self._nonblocking = value
        hidapi.SetNonBlocking(self._handle, self.nonblocking)
        
    def write(self, buffer):
        [print(hex(b), end=" ") for b in buffer._instance]
        print("")
        bytesWritten = hidapi.Write(self._handle, buffer._instance)
        
        if(bytesWritten == -1):
            print("There was an error writing to the device, disconnecting...")
            self.disconnect()
        
        return bytesWritten
        
    def read(self, buffer):
        bytesRead = hidapi.Read(self._handle, buffer._instance)
        
        if(bytesRead == -1):
            print("There was an error reading from the device, disconnecting...")
            self.disconnect()
            
        return bytesRead