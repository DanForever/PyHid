# PyHid
 A python wrapper for the [hidapi](https://github.com/libusb/hidapi) library

## How to use this library
This project is designed to simply slot into your codebase without the need to install anything

You will need to grab the latest binary from [hidapi](https://github.com/libusb/hidapi) and place it inside the [pyhid/lib](pyhid/lib) folder
This has only been tested on windows, so if you want to run it on linux you will need to modify [pyhid/hidapi.py](pyhid/hidapi.py) and set `pathToDll` to point to the location of the linux shared library binary.
Please feel free to submit a pull request that adds proper cross-platform support :)

## Getting started with the API
hidapi.py exposes the raw C API of hidapi, so if you want you can use that directly in more or less the same way you would use hidapi in C.

For a more "pythonic" approach, use pyhid.py which exposes the 'Hid', 'DeviceInformation`, `Device` and `Buffer` classes

## Example
```python
from pyhid import pyhid

with pyhid.Hid() as hid, hid.enumerate() as enumeration:
    for deviceInfo in enumeration:
        if(deviceInfo.product_string):
            print(deviceInfo.product_string)
            print("vendor id: " + hex(deviceInfo.vendor_id))
            print("product id: " + hex(deviceInfo.product_id))
            print("Usage/page:" + hex(deviceInfo.usage) + " / " +  hex(deviceInfo.usage_page))
            print("")
            
        if(deviceInfo.vendor_id == 0x16c0 and deviceInfo.usage_page==0xffab):
            path = deviceInfo.path
            with deviceInfo.connect() as device:
                a = pyhid.Buffer(3)
                a[1] = ord("b")
                device.write(a)
```
