from ctypes import (c_void_p, c_uint32,
                    c_uint64, c_float,
                    c_bool, POINTER,
                    pointer, Structure, cast)
from enum import Enum, unique


@unique
class TsHapticParamType(Enum):
    """
    Haptic parameters types.
    """
    Undefined = 0
    Period = 1
    Amplitude = 2
    PulseWidth = 3
    Temperature = 4


class TsHapticParam(Structure):
    """
    Haptic parameters structure.
    Attributes:
        type (TsHapticParamType): Type of the parameter.
        value (float): Value of the parameter.
    """
    _pack_ = 1
    _fields_ = [('type', c_uint32),
                ('value', c_uint64)]


class TsHapticParamMultiplier(Structure):
    """
    Haptic parameter multiplier struct. Used to control haptic output parameters by multiplication coefficien
    Attributes:
        type (TsHapticParamType): Type of the parameter.
        value (float): Haptic parameter multiplier value (between 0 and 1).
    """
    _pack_ = 1
    _fields_ = [('type', c_uint32),
                ('value', c_float)]


class TsHapticPlayer:
    """
    A player for haptic assets and instant touches. Player is binded to single device

    """

    def __init__(self, __lib, device):
        self.__device = device
        self.__lib = __lib

    def is_player_running(self):
        """
        Gets if the haptic player is in running state.
        Return: 
            bool: true if the player is running
        """
        is_running = c_bool(False)
        self.__lib.ts_haptic_is_player_running(self.__device, pointer(is_running))
        return is_running.value

    def stop_player(self):
        """
        Stop the haptic player for a device.
        """
        self.__lib.ts_haptic_stop_player(self.device_handle)

    def is_player_paused(self):
        """
        Gets if the haptic player is in paused state.
        Return: 
            bool: true if the player is paused
        """
        is_player_paused = c_bool(False)
        self.__lib.ts_haptic_get_player_paused(self.__device, pointer(is_player_paused))

        return is_player_paused.value

    def set_player_paused(self, is_paused):
        """
        Sets the haptic player in paused state or resume.
        """
        self.__lib.ts_haptic_set_player_paused(self.__device, c_bool(is_paused))

    def is_player_muted(self):
        """
        Gets if the haptic player is in muted state.
        Return: 
            bool: true if the player is muted
        """
        is_player_muted = c_bool(False)

        self.__lib.ts_haptic_get_player_muted(self.__device, pointer(is_player_muted))
        return is_player_muted.value

    def set_player_muted(self, is_muted):
        """
        Sets the haptic player in muted state.
        """
        self.__lib.ts_haptic_set_player_muted(self.__device, c_bool(is_muted))

    def get_player_time(self):
        """
        Gets haptic player time since the player has started.
        """
        player_time = c_uint64(0)

        self.__lib.ts_haptic_get_player_muted(self.__device, pointer(player_time))
        return player_time.value

    def get_number_of_master_multipliers(self):
        """
        Gets haptic playable multipliers size.
        Return: 
            int: number of multipliers
        """
        number = c_uint64(0)
        self.__lib.ts_haptic_get_number_of_master_multipliers(self.__device, pointer(number))

        self.number_of_master_multipliers = number.value
        return number.value

    def get_master_multipliers(self):
        """
        Gets haptic player master multipliers.
        Return: 
            list: list of TsHapticParamMultiplier
        """
        number = self.get_number_of_master_multipliers()

        self.master_multipliers = (TsHapticParamMultiplier * number)()
        self.__lib.ts_haptic_get_master_multipliers(self.__device, pointer(self.master_multipliers),
                                                    c_uint64(number))
        return [*self.master_multipliers]

    def set_master_multipliers(self, multipliers):
        """
        Sets haptic player master multipliers.
        Parameters:
            multipliers: list of TsHapticParamMultiplier
        """
        number = self.get_number_of_master_multipliers()
        if len(multipliers) != number:
            print(
                f'TsHapticPlayer set_master_multiplier not valid argument: {multipliers}; expecting {number} multipliers')
            return

        data = cast((TsHapticParamMultiplier * number)(), POINTER(TsHapticParamMultiplier))
        for i, param_multilpier in enumerate(multipliers):
            data[i].type = param_multilpier.type
            data[i].value = param_multilpier.value

        self.__lib.ts_haptic_set_master_multipliers(self.__device, data, c_uint64(number))

    def get_master_multiplier(self, type):
        """
        Gets haptic player master multiplier of specific type.
        Parameters:
            type: TsHapticParamType
        Returns:
            TsHapticParamMultiplier
        """
        multipliers = self.get_master_multipliers()
        for m in multipliers:
            if m.type == type.value:
                return m

        print(f'TsHapticPlayer get_master_multiplier failed to find multiplier of type: {type}')
        return TsHapticParamMultiplier(0, 0)

    def set_master_multiplier(self, multiplier):
        """
        Set haptic player specific master multiplier.
        Parameters:
            multiplier: TsHapticParamMultiplier
        """

        multipliers = self.get_master_multipliers()
        for m in multipliers:
            if m.type == multiplier.type:
                m.value = multiplier.value
                self.set_master_multipliers(multipliers)
                return
        print(f'TsHapticPlayer set_master_multiplier failed to find multiplier of type: {type}')

    def create_playable(self, asset, is_looped):
        """
        Creates a playable from asset.
        Parameters:
            asset: TsAsset
            is_looped: bool
        Returns:
            playable_id: playable id
        """
        playable_id = c_uint64(0)
        self.__lib.ts_haptic_create_playable_from_asset(self.__device, c_void_p(asset),
                                                        c_bool(is_looped), pointer(playable_id))
        return playable_id.value

    def is_playable_exists(self, playable_id):
        """
        Gets if haptic playable exists in the haptic player.
        Parameters:
            playable_id: playable id
        Returns:
            bool: true if the playable exists
        """
        is_exists = c_bool(False)

        self.__lib.ts_haptic_is_playable_exists(self.__device, c_uint64(playable_id), pointer(is_exists))
        return is_exists.value

    def play_playable(self, playable_id):
        """
        Play haptic playable by an id.
        Parameters:
            playable_id: playable id
        """
        self.__lib.ts_haptic_play_playable(self.__device, c_uint64(playable_id))

    def play_touch(self, params, channels, duration):
        """
        Plays haptic touch with provided parameters instanly.
        Parameters:
            params: list of TsHapticParam
            channels: list of channel ids
            duration: duration in ms
        Returns:
            playable_id: playable id
        """
        params_casted = cast((TsHapticParam * len(params))(), POINTER(TsHapticParam))
        for i, param in enumerate(params):
            params_casted[i].type = param.type
            params_casted[i].value = param.value

        channels_casted = cast((c_void_p * len(channels))(), POINTER(c_void_p))
        for i, channel in enumerate(channels):
            channels_casted[i] = channel

        self.__lib.ts_haptic_play_touch(self.__device, params_casted,
                                        c_uint64(len(params)), channels_casted,
                                        c_uint64(len(channels)), c_uint64(duration))

    def create_touch(self, params, channels, duration):
        """
        Creates a haptic touch with provided parameters.
        Parameters:
            params: list of TsHapticParam
            channels: list of channel ids
            duration: duration in ms
        Returns:
            playable_id: playable id
        """
        playable_id = c_uint64(0)
        self.__lib.ts_haptic_create_touch(self.__device, (TsHapticParam * len(params))(*params),
                                          len(params), (c_void_p * len(channels))(*channels),
                                          len(channels), c_uint64(duration), pointer(playable_id))
        return playable_id.value

    def is_playable_playing(self, playable_id):
        """
        Gets if a haptic playable is in playing state.
        Parameters:
            playable_id: playable id
        Returns:
            bool: true if the playable is playing
        """
        is_playing = c_bool(False)

        self.__lib.ts_haptic_is_playable_playing(self.__device, c_uint64(playable_id), pointer(is_playing))
        return bool(is_playing)

    def stop_playable(self, playable_id):
        """
        Stops a haptic playable.
        Parameters:
            playable_id: playable id
        """
        self.__lib.ts_haptic_stop_playable(self.__device, c_uint64(playable_id))

    def remove_playable(self, playable_id):
        """
        Removes a playable from the haptic player.
        Parameters:
            playable_id: playable id
        """
        self.__lib.ts_haptic_remove_playable(self.__device, c_uint64(playable_id))

    def get_playable_paused(self, playable_id):
        """
        Gets if a haptic playable is in paused state.
        Parameters:
            playable_id: playable id
        Returns:
            bool: true if the playable is paused
        """
        is_paused = c_bool(False)

        self.__lib.ts_haptic_get_playable_paused(self.__device, c_uint64(playable_id), pointer(is_paused))
        return bool(is_paused)

    def set_playable_paused(self, playable_id, is_paused):
        """
        Sets a haptic playable in paused state.
        Parameters:
            playable_id: playable id
            is_paused: bool
        """
        self.__lib.ts_haptic_set_playable_paused(self.__device, c_uint64(playable_id), c_bool(is_paused))

    def get_playable_muted(self, playable_id):
        """
        Gets if a haptic playable is in muted state.
        This function returns true if the playable is muted.
        Parameters:
            playable_id: playable id
        Returns:
            bool: true if the playable is muted
        """
        is_muted = c_bool(False)

        self.__lib.ts_haptic_get_playable_muted(self.__device, c_uint64(playable_id), pointer(is_muted))
        return bool(is_muted)

    def set_playable_muted(self, playable_id, is_muted):
        """
        Sets a haptic playable in muted state.
        Parameters:
            playable_id: playable id
            is_muted: bool
        """
        self.__lib.ts_haptic_set_playable_muted(self.__device, c_uint64(playable_id), c_bool(is_muted))

    def get_playable_looped(self, playable_id):
        """
        Gets if a haptic playable is looped.
        This function returns true if the playable is looped.
        Parameters:
            playable_id: playable id
        Returns:
            bool: true if the playable is looped
        """
        is_looped = c_bool(False)

        self.__lib.ts_haptic_get_playable_looped(self.__device, c_uint64(playable_id), pointer(is_looped))
        return bool(is_looped)

    def set_playable_looped(self, playable_id, is_looped):
        """
        Sets a haptic playable in looped state.
        Parameters:
            playable_id: playable id
            is_looped: bool§
        """
        self.__lib.ts_haptic_set_playable_looped(self.__device, c_uint64(playable_id), c_bool(is_looped))

    def get_number_of_playable_multipliers(self, playable_id):
        """
        Gets haptic playable multipliers size.
        This function returns the number of multipliers for the playable.
        Parameters:
            playable_id: playable id
        Returns:
            int: number of multipliers
        """
        number = c_uint64(0)
        self.__lib.ts_haptic_get_number_of_playable_multipliers(self.__device, c_uint64(playable_id),
                                                                pointer(number))
        return number.value

    def get_playable_multipliers(self, playable_id):
        """
        Gets haptic playable multipliers.
        This function returns the multipliers for the playable.
        Parameters:
            playable_id: playable id
        Returns:
            list of TsHapticParamMultiplier
        """
        number = self.get_number_of_playable_multipliers(playable_id)
        multipliers = (TsHapticParamMultiplier * number.value)()
        self.__lib.ts_haptic_get_playable_multipliers(self.__device, c_uint64(playable_id),
                                                      pointer(multipliers), c_uint64(number.value))
        return multipliers

    def set_playable_multipliers(self, playable_id, multipliers):
        """
        Sets haptic playable multipliers.
        This function sets the multipliers for the playable.
        Parameters:
            playable_id: playable id
            multipliers: list of TsHapticParamMultiplier
        """
        number = len(multipliers)
        playable_multipliers = (TsHapticParamMultiplier * number)(*multipliers)
        self.__lib.ts_haptic_set_playable_multipliers(self.__device, c_uint64(playable_id),
                                                      pointer(playable_multipliers), c_uint64(number))

    def get_playable_local_time(self, playable_id):
        """
        Gets haptic playable local playback time.
        This function returns the local time of the playable in milliseconds.
        Parameters:
            playable_id: playable id
        Returns:
            int: local time in milliseconds
        """
        local_time = c_uint64(0)
        self.__lib.ts_haptic_get_playable_local_time(self.__device, c_uint64(playable_id),
                                                     pointer(local_time))
        return int(local_time.value)

    def set_playable_local_time(self, playable_id, local_time):
        """
        Sets haptic playable local playback time.
        Parameters:
            playable_id: playable id
            local_time: int
        """
        self.__lib.ts_haptic_set_playable_local_time(self.__device, c_uint64(playable_id),
                                                     c_uint64(local_time))

    def get_playable_duration(self, playable_id):
        """
        Gets haptic playable duration.
        This function returns the duration of the playable in milliseconds.
        Pareameters:
            playable_id: playable id
        Returns:
            int: duration in milliseconds
        """
        duration = c_uint64(0)
        self.__lib.ts_haptic_get_playable_duration(self.__device, c_uint64(playable_id), pointer(duration))
        return int(duration.value)

    def clear_all_playables(self):
        """
        Removes all haptic playables from the haptic player.
        """
        self.__lib.ts_haptic_clear_all_playables(c_void_p(self.__device))

    def add_channel_to_dynamic_playable(self, channel_id, playable_id):
        """
        Adds a channel to dynamic haptic playable.
        Parameters:
            channel_id: channel id
            playable_id: playable id
        """
        self.__lib.ts_haptic_add_channel_to_dynamic_playable(self.__device, pointer(channel_id),
                                                             c_uint64(playable_id))

    def remove_channel_from_dynamic_playable(self, channel_id, playable_id):
        """
        Removes a channel from dynamic haptic playable.
        Parameters:
            channel_id: channel id
            playable_id: playable id
        """
        self.__lib.ts_haptic_remove_channel_from_dynamic_playable(self.__device, pointer(channel_id),
                                                                  c_uint64(playable_id))

    def set_material_channel_impact(self, channel_id, impact, playable_id):
        """
        Sets channel impact for haptic material.
        Parameters:
            channel_id: channel id
            impact: impact value
            playable_id: playable id
        """
        self.__lib.ts_haptic_set_material_channel_impact(self.__device, pointer(channel_id),
                                                         c_float(impact), c_uint64(playable_id))

    # haptic utils

    def create_touch_parameters(self, period_ms, amplitude, pulse_width):
        """
        Creates touch parameters for haptic touch.
        Parameters:
            period_ms: period in ms
            amplitude: amplitude value
            pulse_width: pulse width value
        Returns:
            list of TsHapticParam
        """
        return [TsHapticParam(TsHapticParamType.Period.value, period_ms),
                TsHapticParam(TsHapticParamType.Amplitude.value, amplitude),
                TsHapticParam(TsHapticParamType.PulseWidth.value, pulse_width)]

    def create_touch_multipliers(self, period_ms_m, amplitude_m, pulse_width_m):
        """
        Creates touch multipliers for haptic touch.
        Arguments:
            period_ms_m: period in ms
            amplitude_m: amplitude value
            pulse_width_m: pulse width value
        Returns:
            list: list of TsHapticParamMultiplier
        """
        return [TsHapticParamMultiplier(TsHapticParamType.Period.value, period_ms_m),
                TsHapticParamMultiplier(TsHapticParamType.Amplitude.value, amplitude_m),
                TsHapticParamMultiplier(TsHapticParamType.PulseWidth.value, pulse_width_m)]
