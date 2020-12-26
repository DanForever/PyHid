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
    
    def __enter__(self):
        hidapi.Init()
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
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
        """PyHid will attempt to connect using path if it is defined, otherwise it will use vendor_id, product_id and serial_number (serial_number is optional)"""
        return Device(path, vendor_id, product_id, serial_number)