from ctypes import (c_void_p, c_uint8,
                    c_uint32, c_uint64,
                    c_bool, CFUNCTYPE,
                    POINTER, pointer,
                    Structure, cast,
                    c_float)
from teslasuit_sdk.ts_types import TsDeviceHandle
from enum import Enum
import time


class PpgSensorType(Enum):
    """Represents a PPG Sensor type."""
    UNDEFINED = 0
    MAX30102 = 1
    MAX86916 = 2

class TsHrv(Structure):
    """Represents Heart Rate Variability (HRV) metrics.

    This structure stores various HRV parameters, which are used to analyze 
    fluctuations in heart rate over time. These metrics help assess autonomic 
    nervous system activity and overall heart health.

    Attributes:
        mean_rr (float): Mean RR interval (time between successive heartbeats) in milliseconds.
        sdnn (float): Standard deviation of NN (normal-to-normal) intervals, indicating overall HRV.
        sdsd (float): Standard deviation of successive RR interval differences.
        rmssd (float): Root Mean Square of Successive Differences between RR intervals, 
                       reflecting short-term HRV.
        sd1 (float): Poincaré plot standard deviation perpendicular to the line of identity 
                     (short-term HRV component).
        sd2 (float): Poincaré plot standard deviation along the line of identity 
                     (long-term HRV component).
        hlf (float): High-frequency component of HRV, associated with parasympathetic nervous activity.
    """
    _pack_ = 1
    _fields_ = [('mean_rr', c_float),
                ('sdnn', c_float),
                ('sdsd', c_float),
                ('rmssd', c_float),
                ('sd1', c_float),
                ('sd2', c_float),
                ('hlf', c_float)]

class TsPpgNodeData(Structure):
    """
    Represents processed PPG (Photoplethysmography) data for a single sensor node.

    This structure stores heart rate, blood oxygen level, and validity flags 
    for a specific PPG sensor node, along with a timestamp indicating when 
    the data was recorded.

    Attributes:
        heart_rate (int): Heart rate calculated in BPM.
        is_heart_rate_valid (bool): Is calculated heart rate valid.
        timestamp (int): Time point that set when the last raw PPG data sample was processed.
    """
    _pack_ = 1
    _fields_ = [('heart_rate', c_uint32),
                ('is_heart_rate_valid', c_bool),
                ('timestamp', c_uint32)]


class TsPpgData(Structure):
    """
    Represents processed PPG (Photoplethysmography) data from multiple sensor nodes.

    This structure stores processed PPG data collected from multiple sensor nodes. 
    Each node contains PPG-related metrics, including heart rate validation.

    Attributes:
        number_of_nodes (int): The number of sensor nodes providing PPG data.
        nodes (POINTER(TsPpgNodeData)): Pointer to an array of processed node data structures.
    """
    _pack_ = 1
    _fields_ = [('number_of_nodes', c_uint32),
                ('nodes', POINTER(TsPpgNodeData))]

    def __str__(self):
        assert self.nodes is not None
        return str("PPG nodes number = {}, first frame heart rate = {}".format(self.number_of_nodes,
                                                                               self.nodes))


class TsPpgRawNodeData(Structure):
    """
    Represents raw PPG (Photoplethysmography) sensor data.

    This structure stores raw PPG sensor data, including infrared, red, blue, and green 
    sensor values, along with a timestamp indicating when the last sample was captured.

    Attributes:
        sample_size (int): Number of samples in the data arrays.
        ir_data (POINTER(c_uint64)): Infrared sensor values sample.
        red_data (POINTER(c_uint64)): Red sensor values sample.
        blue_data (POINTER(c_uint64)): Blue sensor values sample.
        green_data (POINTER(c_uint64)): Green sensor values sample.
        timestamp (int): Time point when the last value from the sample was captured.
    """
    _pack_ = 1
    _fields_ = [('sample_size', c_uint64),
                ('ir_data', POINTER(c_uint64)),
                ('red_data', POINTER(c_uint64)),
                ('blue_data', POINTER(c_uint64)),
                ('green_data', POINTER(c_uint64)),
                ('timestamp', c_uint64)]


class TsPpgRawData(Structure):
    """
    Represents raw PPG (Photoplethysmography) data from multiple sensor nodes.

    This structure holds raw PPG data collected from multiple sensor nodes, each of which 
    contains infrared, red, blue, and green sensor values, along with timestamps.

    Attributes:
        number_of_nodes (int): The number of sensor nodes providing PPG data.
        nodes (POINTER(TsPpgRawNodeData)): Pointer to an array of node data structures.
    """
    _pack_ = 1
    _fields_ = [('number_of_nodes', c_uint8),
                ('nodes', POINTER(TsPpgRawNodeData))]

    def __str__(self):
        assert self.nodes is not None
        return f'Raw PPG nodes number = {self.number_of_nodes}, first frame sample = {self.nodes}'


class TsPpg:
    """
    Handles PPG (Photoplethysmography) sensor data processing and streaming.

    This class manages the interaction with a PPG sensor, including raw and processed data streaming, 
    calibration, and retrieving heart rate variability (HRV) and raw PPG data.

    Attributes:
        __lib: A reference to the underlying sensor library for API calls.
        __device: The handle to the connected PPG sensor device.
        __is_hrv_data_ready (bool): Indicates whether HRV data is ready for retrieval.
        __is_data_ready (bool): Indicates whether processed PPG data is ready.
        __is_data_raw_ready (bool): Indicates whether raw PPG data is ready.
        __is_started (bool): Tracks if the processed data streaming has started.
        __is_started_raw (bool): Tracks if the raw data streaming has started.
        __hrv_callback (CFUNCTYPE): Callback function for HRV data updates.
        __data_callback (CFUNCTYPE): Callback function for processed PPG data updates.
        __data_raw_callback (CFUNCTYPE): Callback function for raw PPG data updates.
        __hrv (TsHrv): Stores the latest processed HRV data.
        __data (TsPpgData): Stores the latest processed PPG data.
        __data_raw (TsPpgRawData): Stores the latest raw PPG data.
    """
    def __init__(self, lib, device):
        self.__lib = lib
        self.__device = device

        self.__is_hrv_data_ready = False
        self.__is_data_ready = False
        self.__is_data_raw_ready = False

        self.__is_started = False
        self.__is_started_raw = False

        self.__hrv_callback = None
        self.__data_callback = None
        self.__data_raw_callback = None

        self.__hrv = TsHrv()
        self.__data = TsPpgData()
        self.__data_raw = TsPpgRawData()

    def start_raw_streaming(self):
        """Starts the streaming of a PPG raw data"""
        if self.__is_started_raw:
            return

        self.__subscribe_on_data_update()
        self.__subscribe_on_data_raw_update()

        self.__lib.ts_ppg_raw_start_streaming(self.__device)
        self.__is_started_raw = True

    def stop_raw_streaming(self):
        """Stops the streaming of a PPW raw data"""
        if not self.__is_started_raw:
            return

        self.__lib.ts_ppg_raw_stop_streaming(self.__device)
        self.__is_started_raw = False

    def get_hrv_data_on_ready(self):
        """Blocks execution until HRV data is ready and returns the latest HRV data.

        Returns:
            TsHrv: The latest HRV data.
        """
        while not self.__is_hrv_data_ready and self.__is_started_raw:
            time.sleep(0.001)

        self.__is_hrv_data_ready = False
        return self.__hrv

    def get_raw_data_on_ready(self):
        """Blocks execution until raw PPG data is ready and returns the latest raw data.

        Returns:
            TsPpgRawData: The latest raw PPG data.
        """
        while not self.__is_data_raw_ready and self.__is_started_raw:
            time.sleep(0.001)

        self.__is_data_raw_ready = False
        return self.__data_raw

    def get_hrv(self):
        """Retrieves the latest HRV data.

        Returns:
            TsHrv: The latest HRV data.
        """
        return self.__hrv

    def get_data(self):
        """Retrieves the latest processed PPG data.

        Returns:
            TsPpgData: The latest processed PPG data.
        """
        return self.__data

    def get_data_raw(self):
        """Retrieves the latest raw PPG data.

        Returns:
            TsPpgRawData: The latest raw PPG data.
        """
        return self.__data_raw

    def calibrate(self):
        '''
        Calibrates PPG processor.
        The calibration procedure is capturing interval of the raw data during 3 seconds. 
        The captured interval will be used in calculation of all ppg parameters.
        By default, calibration procedure starts on starting PPG processor.
        In case on bad start, the calibration procedure might be restarted using this function.
        '''
        self.__lib.ts_ppg_calibrate(self.__device)

    def __subscribe_on_data_raw_update(self):
        def __on_hrv_updated(device_ptr, data_ptr, user_data):
            self.__lib.ts_hrv_get_data(c_void_p(data_ptr), pointer(self.__hrv))
            self.__is_hrv_data_ready = True
            
        hrv_data_callback_prototype = CFUNCTYPE(None, POINTER(TsDeviceHandle), c_void_p, c_void_p)
        self.__hrv_callback = hrv_data_callback_prototype(__on_hrv_updated)
        self.__lib.ts_hrv_set_update_callback(self.__device, self.__hrv_callback,
                                                  c_void_p(0))
                                                  
        def __on_updated_raw_callback(device_ptr, data_ptr, user_data):
            self.__parse_data_raw(data_ptr)
            self.__is_data_raw_ready = True

        data_raw_callback_prototype = CFUNCTYPE(None, POINTER(TsDeviceHandle), c_void_p, c_void_p)
        self.__data_raw_callback = data_raw_callback_prototype(__on_updated_raw_callback)
        self.__lib.ts_ppg_raw_set_update_callback(self.__device, self.__data_raw_callback,
                                                  c_void_p(0))

    def __subscribe_on_data_update(self):
        def __on_updated_callback(device_ptr, data_ptr, user_data):
            nodes_indexes = self.__get_nodes_indexes(data_ptr)
            self.__data.number_of_nodes = len(nodes_indexes)

            data = (TsPpgNodeData * len(nodes_indexes))()

            for i, node_index in enumerate(nodes_indexes):
                heart_rate = self.__get_heart_rate(data_ptr, node_index)
                is_valid_heart_rate = self.__get_is_valid_heart_rate(data_ptr, node_index)
                timestamp = self.__get_timestamp(data_ptr, node_index)

                data[i] = TsPpgNodeData(heart_rate, is_valid_heart_rate, timestamp)
                
            self.__data.nodes = cast(data, POINTER(TsPpgNodeData))
            self.__is_data_ready = True

        data_callback_prototype = CFUNCTYPE(None, POINTER(TsDeviceHandle), c_void_p, c_void_p)
        self.__data_callback = data_callback_prototype(__on_updated_callback)
        self.__lib.ts_ppg_set_update_callback(self.__device, self.__data_callback,
                                              c_void_p(0))

    def __parse_data_raw(self, data_ptr):
        nodes_indexes = self.__get_raw_nodes_indexes(data_ptr)
        data = (TsPpgRawNodeData * len(nodes_indexes))()

        for i, node_index in enumerate(nodes_indexes):
            sample_size = self.__get_raw_number_of_sample(data_ptr, node_index)

            ir_data = self.__get_raw_ir_data(data_ptr, node_index)
            red_data = self.__get_raw_red_data(data_ptr, node_index)
            green_data = self.__get_raw_green_data(data_ptr, node_index)
            blue_data = self.__get_raw_blue_data(data_ptr, node_index)
            timestamp = self.__get_raw_timestamp(data_ptr, node_index)

            data[i] = TsPpgRawNodeData(sample_size,
                                       cast(ir_data, POINTER(c_uint64)), cast(red_data, POINTER(c_uint64)),
                                       cast(blue_data, POINTER(c_uint64)), cast(green_data, POINTER(c_uint64)),
                                       timestamp)
        
        self.__data_raw.number_of_nodes = len(nodes_indexes)
        self.__data_raw.nodes = cast(data, POINTER(TsPpgRawNodeData))

    def __get_number_of_nodes(self, data_ptr):
        number_of_nodes = c_uint8(0)
        self.__lib.ts_ppg_get_number_of_nodes(c_void_p(data_ptr), pointer(number_of_nodes))

        return number_of_nodes.value

    def __get_raw_nodes_indexes(self, data_ptr):
        number_of_nodes = self.__get_number_of_nodes(data_ptr)
        nodes_indexes = (c_uint8 * number_of_nodes)()

        self.__lib.ts_ppg_raw_get_node_indexes(c_void_p(data_ptr), pointer(nodes_indexes), number_of_nodes)

        return [*nodes_indexes]

    def __get_nodes_indexes(self, data_ptr):
        number_of_nodes = self.__get_number_of_nodes(data_ptr)
        nodes_indexes = (c_uint8 * number_of_nodes)()

        self.__lib.ts_ppg_get_node_indexes(c_void_p(data_ptr), pointer(nodes_indexes), number_of_nodes)

        return [*nodes_indexes]

    def __get_heart_rate(self, data_ptr, node_index):
        heart_rate = c_uint8(0)
        self.__lib.ts_ppg_get_heart_rate(c_void_p(data_ptr), c_uint8(node_index), pointer(heart_rate))

        return heart_rate.value

    def __get_is_valid_heart_rate(self, data_ptr, node_index):
        is_valid = c_uint8(0)
        self.__lib.ts_ppg_is_heart_rate_valid(c_void_p(data_ptr), c_uint8(node_index), pointer(is_valid))

        return is_valid.value

    def __get_timestamp(self, data_ptr, node_index):
        timestamp = c_uint64(0)
        self.__lib.ts_ppg_get_timestamp(c_void_p(data_ptr), c_uint8(node_index), pointer(timestamp))

        return timestamp.value
        
    def __get_raw_timestamp(self, data_ptr, node_index):
        timestamp = c_uint64(0)
        self.__lib.ts_ppg_raw_get_timestamp(c_void_p(data_ptr), c_uint8(node_index), pointer(timestamp))

        return timestamp.value

    def __get_raw_number_of_sample(self, data_ptr, node_index):
        number_of_samples = c_uint64(0)
        self.__lib.ts_ppg_raw_get_data_size(c_void_p(data_ptr), node_index, pointer(number_of_samples))

        return number_of_samples.value

    def __get_raw_red_data(self, data_ptr, node_index):
        number_of_samples = self.__get_raw_number_of_sample(data_ptr, node_index)

        red_data = (c_uint64 * number_of_samples)()
        self.__lib.ts_ppg_raw_get_red_data(c_void_p(data_ptr), c_uint8(node_index), pointer(red_data), c_uint64(number_of_samples))

        return red_data

    def __get_raw_ir_data(self, data_ptr, node_index):
        number_of_samples = self.__get_raw_number_of_sample(data_ptr, node_index)

        ir_data = (c_uint64 * number_of_samples)()
        self.__lib.ts_ppg_raw_get_infrared_data(c_void_p(data_ptr), c_uint8(node_index), pointer(ir_data), c_uint64(number_of_samples))

        return ir_data

    def __get_raw_blue_data(self, data_ptr, node_index):
        number_of_samples = self.__get_raw_number_of_sample(data_ptr, node_index)

        blue_data = (c_uint64 * number_of_samples)()
        self.__lib.ts_ppg_raw_get_blue_data(c_void_p(data_ptr), c_uint8(node_index), pointer(blue_data), c_uint64(number_of_samples))

        return blue_data

    def __get_raw_green_data(self, data_ptr, node_index):
        number_of_samples = self.__get_raw_number_of_sample(data_ptr, node_index)

        green_data = (c_uint64 * number_of_samples)()
        self.__lib.ts_ppg_raw_get_green_data(c_void_p(data_ptr), c_uint8(node_index), pointer(green_data), c_uint64(number_of_samples))

        return green_data
