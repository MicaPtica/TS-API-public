from ctypes import (c_uint8, POINTER,
                    pointer, Structure,
                    c_uint64, c_int, c_uint32,
                    CFUNCTYPE, c_void_p, cast)
from teslasuit_sdk.ts_types import TsDeviceHandle
import time

class TsBiaConfig(Structure):
    """
    BIA streaming configuration struct.
    Attributes:
        channels (list): List of channel indexes to stream.
        number_of_channels (int): Number of channels.
        start_frequency (int): Starting frequency for the BIA data streaming.
        frequency_step (int): Frequency step size.
        number_of_steps (int): Number of frequency steps.
    """
    _pack_ = 1
    _fields_ = [("channels", POINTER(c_uint32)),
                ("number_of_channels", c_uint32),
                ("start_frequency", c_uint32),
                ("frequency_step", c_uint32),
                ("number_of_steps", c_uint32)]

class TsComplexNumber(Structure):
    """
    Complex number struct.
    Attributes:
        real_value (int): Real part of the complex number.
        im_value (int): Imaginary part of the complex number.
    """
    _pack_ = 1
    _fields_ = [('real_value', c_int),
                ('im_value', c_int)]


class TsBiaFrequencyData(Structure):
    """
    BIA frequency data struct.
    Attributes:
        frequency (int): Frequency value.
        complex_number (TsComplexNumber): Complex number associated with the frequency.
    """
    _pack_ = 1
    _fields_ = [('frequency', c_uint32),
                ('complex_number', TsComplexNumber)]


class TsBiaChannelData(Structure):
    """
    BIA channel data struct.
    Attributes:
        channel_index (int): Index of the channel.
        number_of_frequencies (int): Number of frequencies in the channel.
        frequencies (list): List of frequency data.
    """
    _pack_ = 1
    _fields_ = [('channel_index', c_uint32),
                ('number_of_frequencies', c_uint64),
                ('frequencies', POINTER(TsBiaFrequencyData))]


class TsBiaChannels(Structure):
    """
    BIA channels data struct.
    Attributes:
        number_of_channels (int): Number of channels.
        channels (list): List of channel data.
    """
    _pack_ = 1
    _fields_ = [('number_of_channels', c_uint32),
                ('channels', POINTER(TsBiaChannelData))]

class TsBia:
    """
    Class for handling BIA (Bioelectrical Impedance Analysis) data streaming from the device.
    Attributes:
        lib (object): Library object for interfacing with the device.
        device (object): Device object for communication.
        is_started (bool): Flag indicating if streaming is started.
        is_data_ready (bool): Flag indicating if data is ready to be retrieved.
        data (TsBiaChannels): Structure to hold BIA channels data.
    """
    def __init__(self, lib, device):
        self.__lib = lib
        self.__device = device

        self.__is_started = False
        self.__is_data_ready = False

        self.__data = TsBiaChannels()

    def start_streaming(self):
        """
        Start streaming BIA data from the device.
        """
        if self.__is_started:
            return

        self.__subscribe_on_data_update()

        self.__lib.ts_bia_start_streaming(self.__device)
        self.__is_started = True

    def stop_streaming(self):
        """
        Stop streaming BIA data from the device.
        """
        if not self.__is_started:
            return

        self.__lib.ts_bia_stop_streaming(self.__device)
        self.__is_started = False

    def get_data_on_ready(self):
        """
        Wait for BIA data to be ready and return it.
        This method blocks until the data is ready.
        Return:
            TsBiaChannels: The BIA data containing channels information.
        """
        while not self.__is_data_ready and self.__is_started:
            time.sleep(0.001)

        self.__is_data_ready = False
        return self.__data

    def set_streaming_config(self, channels, start_frequency=10000, number_of_steps=10, frequency_step=10000):
        """
        Set the streaming configuration for BIA data.
        Parameters:
            channels: List of channel indexes to stream.
            start_frequency: Starting frequency for the BIA data.
            number_of_steps: Number of frequency steps.
            frequency_step: Frequency step size.
        """
        converted_channels = (c_uint32 * len(channels))(*channels)
        
        config = TsBiaConfig()
        
        config.channels = cast(converted_channels, POINTER(c_uint32))
        config.number_of_channels = len(channels)
        config.start_frequency = c_uint32(start_frequency)
        config.number_of_steps = c_uint32(number_of_steps)
        config.frequency_step = c_uint32(frequency_step)
        
        self.__lib.ts_bia_set_streaming_config(self.__device,  pointer(config))
    
    def __subscribe_on_data_update(self):
        def __on_updated_callback(device, data_ptr, user_data):
            self.__data.number_of_channels = self.__get_number_of_channels(data_ptr)
            self.__data.channels = (TsBiaChannelData * self.__data.number_of_channels)()
   
            channels_indexes = self.__get_channels_indexes(data_ptr, self.__data.number_of_channels)               
            
            for i, channel_index in enumerate([*channels_indexes]):
                self.__data.channels[i].channel_index = channel_index
                 
                number_of_frequencies = self.__get_channel_frequencies_size(data_ptr, channel_index)
                channel_frequencies = self.__get_channel_frequencies(data_ptr, channel_index, number_of_frequencies)
                
                frequencies_data = (TsBiaFrequencyData * number_of_frequencies)()
                self.__data.channels[i].number_of_frequencies = number_of_frequencies
                self.__data.channels[i].frequencies = cast(frequencies_data, POINTER(TsBiaFrequencyData))
                
                for j, frequency in enumerate([*channel_frequencies]):
                    frequency_value = self.__get_channel_frequency_complex_value(data_ptr, channel_index, frequency)
                    frequencies_data[j].frequency = frequency
                    frequencies_data[j].complex_number = frequency_value
            
            self.__is_data_ready = True

        data_callback_prototype = CFUNCTYPE(None, POINTER(TsDeviceHandle), c_void_p, c_void_p)
        self.__data_callback = data_callback_prototype(__on_updated_callback)
        self.__lib.ts_bia_set_update_callback(self.__device, self.__data_callback,
                                              c_void_p())

    def __get_channels_indexes(self, data_ptr , number_of_channels):
        indexes = (c_uint32 * number_of_channels)()
        self.__lib.ts_bia_get_channels_indexes(c_void_p(data_ptr), pointer(indexes), c_uint64(number_of_channels))
        
        return indexes
        
    def __get_number_of_channels(self, data_ptr):
        number_of_channels = c_uint64(0)
        self.__lib.ts_bia_get_number_of_channels(c_void_p(data_ptr), pointer(number_of_channels))

        return number_of_channels.value

    def __get_channel_frequencies_size(self, data_ptr, channel_index):
        number_of_frequencies = c_uint64(0)
        self.__lib.ts_bia_get_channel_number_of_frequencies(c_void_p(data_ptr), 
                                                            c_uint32(channel_index), 
                                                            pointer(number_of_frequencies))
        
        return number_of_frequencies.value

    def __get_channel_frequencies(self, data_ptr, channel_index, number_of_frequencies):
        frequencies = (c_uint32 * number_of_frequencies)()
        self.__lib.ts_bia_get_channel_frequencies(c_void_p(data_ptr), c_uint32(channel_index),
                                                  pointer(frequencies), c_uint64(number_of_frequencies))
                                                  
        return frequencies

    def __get_channel_frequency_complex_value(self,
                                              data_ptr,
                                              channel_index,
                                              frequency):
        complex_number = TsComplexNumber()
        self.__lib.ts_bia_get_channel_frequency_complex_value(c_void_p(data_ptr),
                                                              c_uint32(channel_index),
                                                              c_uint32(frequency),
                                                              pointer(complex_number))
        return complex_number
