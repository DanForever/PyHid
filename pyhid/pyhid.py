from . import hidapi
from ._enumeration import *
from .buffer import *
from ._device import *

class Hid:
    """Your entry point into the pyhid library
    
    Example:
    with pyhid.Hid() as hid:
        # do stuff!
    """
    
    def init(self):
        hidapi.Init()
    
    def shutdown(self):
        hidapi.Shutdown()
        
    def enumerate(self, vendor_id = 0, product_id = 0):
        """Get a list of all hid devices connected to this machine
        
        Specify vendor_id or product_id to restrict the results to a specific group
        
        Example usage:
        with hid.enumerate() as enumeration:
            # do stuff!
        """
        return Enumeration(vendor_id, product_id)
        
    def connect(self, path = None, vendor_id = None, product_id = None, serial_number = None):
        """PyHid will attempt to connect using path if it is defined, otherwise it will use vendor_id, product_id and serial_number (serial_number is optional).
        
        connect() is intended for use as a context manager (i.e. being called from inside a "with" statement.
        device() is meant for users who want or need manual control. This comes with the caveat that they must ensure that they properly dispose of the device object when they are finished with it.
        """
        return Device(path, vendor_id, product_id, serial_number)
    
    device = connect
    
    # Context Manager
    def __enter__(self):
        self.init()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.Shutdown()