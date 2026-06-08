import uuid
from ctypes import *
from enum import Enum, unique, IntEnum

class TsDeviceHandle(Structure):
    pass


class TsDevice(Structure):
    """
    A structure that represents a TESLASUIT device.
    It contains a UUID that uniquely identifies the device.
    Attributes:
        uuid (bytes): A 16-byte UUID of the device.
    """
    _pack_ = 1
    _fields_ = [('uuid', c_uint8 * 16)]

    def __str__(self):
        return str(uuid.UUID(hex=''.join(format(b, '02x') for b in self.uuid)))


class TsVersion(Structure):
    """
    A structure that represents the version of the TESLASUIT C API.
    It contains four fields: major, minor, patch, and build.
    Attributes:
        major (int): Major version number.
        minor (int): Minor version number.
        patch (int): Patch version number.
        build (int): Build version number.
    """
    _pack_ = 1
    _fields_ = [('major', c_uint32),
                ('minor', c_uint32),
                ('patch', c_uint32),
                ('build', c_uint32)]

    def __str__(self):
        return f'{self.major}.{self.minor}.{self.patch}'

    def __repr__(self):
        return f'TsVersion({self.major}.{self.minor}.{self.patch}.{self.build})'

@unique
class TsDeviceType(IntEnum):
    """
    An enumeration that represents the type of a TESLASUIT device.
    Attributes:
        Undefined (int): Undefined device type.
        Suit (int): TESLASUIT suit device type.
        Glove (int): TESLASUIT glove device type.
    """
    Undefined = 0
    Suit = 1
    Glove = 2

@unique
class TsDeviceSide(IntEnum):
    """
    An enumeration that represents the side of a TESLASUIT glove device.
    Attributes:
        Undefined (int): Undefined device side.
        Right (int): Right glove device side.
        Left (int): Left glove device side.
    """
    Undefined = 0
    Right = 1
    Left = 2
    
@unique
class TsDeviceEventPolicy(IntEnum):
    """
    An enumeration that represents the policy for handling TESLASUIT device events.
    Attributes:
        Enumerate (int): Enumerate all devices.
        Attach (int): Attach a device.
        Detach (int): Detach a device.
    """
    TsDeviceEventPolicy_Enumerate = 1

@unique
class TsDeviceEvent(IntEnum):
    """
    An enumeration that represents the events related to TESLASUIT devices.
    Attributes:
        DeviceAttached (int): Device attached event.
        DeviceDetached (int): Device detached event.
    """
    TsDeviceEvent_DeviceAttached = 1
    TsDeviceEvent_DeviceDetached = 2
    
    @classmethod
    def from_param(cls, obj):
        return c_int(obj)
