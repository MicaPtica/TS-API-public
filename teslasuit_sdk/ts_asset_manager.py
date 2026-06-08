from ctypes import (pointer, c_void_p, c_char_p,
                    POINTER, c_char, cast)
from enum import Enum, unique, IntEnum
from teslasuit_sdk import ts_types

@unique
class TsAssetType(IntEnum):
    """
    Asset type.

    Possible values:
        Undefined = 0,
        Spline = 1,
        HapticEffect = 2,
        Material = 3,
        TouchSequence = 4,
        PresetAnimation = 5,
        SceneAnimation = 6
    """
    Undefined = 0
    Spline = 1
    HapticEffect = 2
    Material = 3
    TouchSequence = 4
    PresetAnimation = 5
    SceneAnimation = 6

class TsAssetManager:
    """
    A class that provides access to TESLASUIT assets.
    """
    def __init__(self, lib):
        self.__lib = lib

    def load_asset_from_path(self, path):
        """
        Loads asset from path.
        Args:
            path (str): Path to the asset.
        Returns:
            TsAssetHandle: Handle to the loaded asset.
        """
        byte_path = path.encode('utf-8')
        c_path = c_char_p(byte_path)
        ts_asset_load_from_path = self.__lib.ts_asset_load_from_path
        ts_asset_load_from_path.argtypes = [POINTER(c_char)]
        ts_asset_load_from_path.restype = c_void_p
        return ts_asset_load_from_path(c_path)

    def load_asset_from_data(self, data, size):
        """
        Loads asset from binary data.
        Args:
            data (bytes): Binary data of the asset.
            size (int): Size of the binary data.
        Returns:
            TsAssetHandle: Handle to the loaded asset.
        """
        ts_asset_load_from_binary_data = self.__lib.ts_asset_load_from_binary_data
        ts_asset_load_from_binary_data.argtypes = [POINTER(c_uint8), c_uint64]
        self.__lib.ts_asset_load_from_binary_data(data, size)

    def get_asset_type(self, asset_handle):
        """
        Gets the type of the asset.
        Args:
            asset_handle (TsAssetHandle): Handle to the asset.
        Returns:
            TsAssetType: Type of the asset.
        """
        ts_asset_get_type = self.__lib.ts_asset_get_type
        ts_asset_get_type.argtypes = [c_void_p, POINTER(c_int)]
        asset_type = c_int(0)
        ts_asset_get_type(asset_handle, asset_type)
        return asset_type.value

    def unload_asset(self, asset_handle):
        """
        Unloads the asset.
        Args:
            asset_handle (TsAssetHandle): Handle to the asset.
        """
        ts_asset_unload = self.__lib.ts_asset_unload
        ts_asset_unload.argtypes = [c_void_p]
        ts_asset_unload(asset_handle)
