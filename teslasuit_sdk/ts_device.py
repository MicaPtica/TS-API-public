from teslasuit_sdk import ts_types
from teslasuit_sdk.subsystems import (ts_mocap, ts_emg,
                         ts_ppg, ts_haptic, ts_bia, 
                         ts_magnetic_encoder, ts_current_feedback)

from ctypes import (c_ubyte, pointer,
                    c_void_p, c_char_p,
                    POINTER, c_int)

class TsDevice:
    """
    The Device module provides functions for connecting to TESLASUIT devices,
    subscribing to connections and disconnections of TESLASUIT devices,
    functions for retrieving device information and the main device control functions..
    Attributes
    ----------
    lib : CDLL loaded TESLASUIT C API library object
    device_uuid : UUID of the device
    device_handle : TsDeviceHandle of the device
    type : Type of the device
    side : TsDeviceSide if type is glove, side of the device (left or right)
    mocap : TsMocap class that provides access to the motion capture subsystem
    emg : TsEmg class that provides access to the EMG subsystem
    ppg : TsPpg class that provides access to the PPG subsystem
    current_feedback : TsCurrentFeedback class that provides access to the current feedback subsystem
    magnetic_encoder : TsMagneticEncoder class that provides access to the magnetic encoder subsystem
    haptic : TsHapticPlayer class that provides access to the haptic subsystem
    bia : TsBia class that provides access to the BIA subsystem
    """
    def __init__(self, lib, device_uuid):
        self.__lib = lib
        self.device_uuid = ts_types.TsDevice(device_uuid.uuid)
        self.__device_handle = POINTER(ts_types.TsDeviceHandle)
        self.__open_device(self.device_uuid)
        self.__read_properties()

        self.mocap = ts_mocap.TsMocap(lib, self.__device_handle)
        self.emg = ts_emg.TsEmg(lib, self.__device_handle)
        self.ppg = ts_ppg.TsPpg(lib, self.__device_handle)
        self.current_feedback = ts_current_feedback.TsCurrentFeedback(lib, self.__device_handle)
        self.magnetic_encoder = ts_magnetic_encoder.TsMagneticEncoder(lib, self.__device_handle, self.side)
        self.haptic = ts_haptic.TsHapticPlayer(lib, self.__device_handle)
        self.bia = ts_bia.TsBia(lib, self.__device_handle)

    def __open_device(self, device_uuid):
        ts_device_open = self.__lib.ts_device_open
        ts_device_open.argtypes = [POINTER(ts_types.TsDevice)]
        ts_device_open.restype = POINTER(ts_types.TsDeviceHandle)
        self.__device_handle = ts_device_open(pointer(device_uuid))

    def __close_device(self):
        self.__lib.ts_device_close(self.__device_handle)

    def __read_properties(self):
        self.type = ts_types.TsDeviceType(self.__lib.ts_device_get_product_type(self.__device_handle))
        if self.type == ts_types.TsDeviceType.Glove:
            self.side = ts_types.TsDeviceSide(self.__lib.ts_device_get_device_side(self.__device_handle))
        else:
            self.side = ts_types.TsDeviceSide.Undefined

    def get_device_ssid(self):
        """
        Get the device SSID
        Returns:
            list: SSID of the device
        """
        ssid = (c_ubyte * SUIT_SSID_LENGTH)()
        self.__lib.ts_device_get_name(self.__device_handle, pointer(ssid))
        return list(ssid)

    def get_device_serial(self):
        """
        Get the device serial number
        Returns:
            str: serial number of the device
        """
        ts_get_device_serial = self.__lib.ts_device_get_serial
        ts_get_device_serial.argtypes = [POINTER(TsDeviceHandle)]
        ts_get_device_serial.restype = c_char_p
        serial = ts_get_device_serial(self.__device_handle)

    def get_product_type(self):
        """
        Get the product type of the device
        Returns:
            TsDeviceType: product type of the device
        """
        ts_device_get_product_type = self.__lib.ts_device_get_product_type
        ts_device_get_product_type.argtypes = [POINTER(ts_types.TsDeviceHandle)]
        ts_device_get_product_type.restype = c_int(0)
        return ts_device_get_product_type(self.__device_handle)

    def get_mapping(self):
        """
        Get the mapping according to the divice type and version.
        Returns:
            TsMapping2D: mapping of the device
        """
        mapping = c_void_p()
        self.__lib.ts_mapping2d_get_by_device(self.__device_handle, pointer(mapping))
        return mapping.value

    def __del__(self):
        self.__close_device()
