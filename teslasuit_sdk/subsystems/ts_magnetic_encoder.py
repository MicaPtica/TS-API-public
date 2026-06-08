from ctypes import *
from teslasuit_sdk import ts_types
from teslasuit_sdk.ts_mapper import TsBone2dIndex
from enum import Enum, unique, IntEnum


@unique
class TsForceFeedbackLockDirection(Enum):
    """
    Force feedback lock direction.
    A direction value that corresponds for what side will be limited to move by servomotor.
    """
    Up = 1
    Down = 2
    Both = 3

class TsForceFeedbackConfig(Structure):
    """
    Force feedback config.
    Describes servomotor force feedback control by bone index with the given angle in degrees and its direction.
    Attributes:
        bone_index (int): Index of the bone.
        angle (float): Angle for the force feedback.
        hardness_percent (int): Hardness percentage from 0 to 100.
        lock_direction (TsForceFeedbackLockDirection): Direction of the lock.
    """
    _pack_ = 1
    _fields_ = [('bone_index', c_uint32),
                ('angle', c_float),
                ('hardness_percent', c_uint8),
                ('lock_direction', c_uint32)]

class TsFingerMEPosition:
    """
    Represensts the position of a finger. """
    def __init__(self):
        self.flexion_angle = 0
        self.abduction_angle = 0

class TsGloveMEPosition:
    """
    Class for handling the magnetic encoder position structures for the fingers."""
    def __init__(self, side):
        self.side = side
        if self.side == ts_types.TsDeviceSide.Left:
            self.fingers = get_left_default_position_struct()
        elif self.side == ts_types.TsDeviceSide.Right:
            self.fingers = get_right_default_position_struct()
        else:
            self.fingers = dict()

ENCODER_COUNT = 5
LEFT_BONE_INDEXES = [TsBone2dIndex.LeftThumbProximal, TsBone2dIndex.LeftIndexProximal,
                     TsBone2dIndex.LeftMiddleProximal, TsBone2dIndex.LeftRingProximal,
                     TsBone2dIndex.LeftLittleProximal]
RIGHT_BONE_INDEXES = [TsBone2dIndex.RightThumbProximal, TsBone2dIndex.RightIndexProximal,
                      TsBone2dIndex.RightMiddleProximal, TsBone2dIndex.RightRingProximal,
                      TsBone2dIndex.RightLittleProximal]

class TsMagneticEncoder:
    """
    Class for handling the magnetic encoder data streaming and force feedback.
    Attributes:
        lib: The library instance.
        device: The device handle.
        side: The side of the device (left or right).
        positions: The positions of the fingers.
        data_callback: The callback function for data updates.
    """
    def __init__(self, lib, device, side):
        self.__device = device
        self.side = side
        self.__lib = lib
        self.__is_data_ready = False
        self.__is_started = False
        self.__positions = TsGloveMEPosition(self.side)
        self.__data_callback = None
        self.data_callback = None

    def __str__(self):
        return str(self.__positions)

    def __subscribe_on_data_update(self):
        def on_update_callback(device_ptr, data_ptr, user_data_ptr):
            for bone, position in self.__positions.fingers.items():
                flexion_angle = c_float()
                abduction_angle = c_float()
                self.__lib.ts_force_feedback_get_flexion_angle(c_void_p(data_ptr), bone.value, pointer(flexion_angle))                
                self.__lib.ts_force_feedback_get_abduction_angle(c_void_p(data_ptr), bone.value, pointer(abduction_angle))
                position.flexion_angle = flexion_angle.value
                position.abduction_angle = abduction_angle.value
            if self.data_callback != None:
                self.data_callback(self.__positions)

        me_update_prototype = CFUNCTYPE(None, c_void_p, c_void_p, c_void_p)
        self.__data_callback = me_update_prototype(on_update_callback)
        self.__lib.ts_force_feedback_set_position_update_callback(self.__device, self.__data_callback, c_void_p())

    def set_data_update_callback(self, callback): # must be private???? Check if needed
        self.data_callback = callback

    def get_positions(self):
        """
        Get the current positions of the fingers.
        Returns:
            dict: A dictionary of bone indexes and their corresponding TsFingerMEPosition.
        """
        return self.__positions

    def start_me_streaming(self):
        """
        Starts magnetic encoder data streaming.
        This method subscribes to the data update callback and starts streaming.
        """
        if self.__is_started:
            return
        self.__subscribe_on_data_update()
        self.__lib.ts_force_feedback_start_position_streaming(self.__device)
        self.__is_started = True

    def stop_me_streaming(self):
        """
        Stops magnetic encoder data streaming.
        This method stops the streaming and unsubscribes from the data update callback.
        """
        if not self.__is_started:
            return
        self.__lib.ts_force_feedback_stop_position_streaming(self.__device)
        self.__is_started = False

    def ts_force_feedback_enable(self, ff_configs):
        """
        Enable force feedback for the specified bone indexes.
        Parameters:
            ff_configs: A list of TsForceFeedbackConfig objects.
        """
        control_casted = (TsForceFeedbackConfig * len(ff_configs))(*ff_configs)
        self.__lib.ts_force_feedback_enable(self.__device,
                                            cast(control_casted, POINTER(TsForceFeedbackConfig)),
                                            c_uint64(len(ff_configs)))

    def ts_force_feedback_disable(self, bone_indexes):
        """
        Disable force feedback for the specified bone indexes.
        Returns:
            list: A list of bone indexes to disable force feedback for.
        """
        bone_indexes_casted = (c_uint32 * len(bone_indexes))(*bone_indexes)
        self.__lib.ts_force_feedback_disable(self.__device,
                                             pointer(bone_indexes_casted),
                                             c_uint64(len(bone_indexes)))

    def get_default_position_struct(self):
        """
        Get the default position structure for the magnetic encoder.
        Returns:
            dict: A dictionary of bone indexes and their corresponding TsFingerMEPosition.
        """
        if self.side == ts_types.TsDeviceSide.Left:
            return get_left_default_position_struct()
        else:
            return get_right_default_position_struct()

    def get_default_ff_controls_struct(self):
        """
        Get the default force feedback controls structure for the magnetic encoder.
        Returns:
            A TsForceFeedbackConfig structure.
        """
        if self.side == ts_types.TsDeviceSide.Left:
            return get_left_default_ff_controls_struct()
        else:
            return get_right_default_ff_controls_struct()

    def get_bone_indexes(self):
        """
        Get the bone indexes for the magnetic encoder.
        Returns:
            list: A list of bone indexes.
        """
        if self.side == ts_types.TsDeviceSide.Left:
            return LEFT_BONE_INDEXES
        else:
            return RIGHT_BONE_INDEXES

# utils

def get_position_struct_for_bones(bone_indexes):
    """
    Create a dictionary of TsFingerMEPosition for the given bone indexes.
    Parameters:
        param bone_indexes: List of bone indexes.
    Returns:
        dict: A dictionary of bone indexes and their corresponding TsFingerMEPosition.
    """
    positions = dict()
    for index in bone_indexes:
        positions[index] = TsFingerMEPosition()
    return positions

def get_left_default_position_struct():
    """
    Create a default position struct for the left hand.
    Returns:
        dict: A dictionary of bone indexes and their corresponding TsFingerMEPosition.
    """
    return get_position_struct_for_bones(LEFT_BONE_INDEXES)

def get_right_default_position_struct():
    """
    Create a default position struct for the right hand.
    Returns:
        dict: A dictionary of bone indexes and their corresponding TsFingerMEPosition.
    """
    return get_position_struct_for_bones(RIGHT_BONE_INDEXES)

def mirror_bone_index(bone_index):
    """
    Mirror the bone index for the opposite hand.
    Parameters:
        bone_index: Bone index to be mirrored.
    Returns:
        Mirrored bone index.
    """
    for i in range(0, len(LEFT_BONE_INDEXES)):
        if LEFT_BONE_INDEXES[i] == bone_index:
            return RIGHT_BONE_INDEXES[i]
        if RIGHT_BONE_INDEXES[i] == bone_index:
            return LEFT_BONE_INDEXES[i]
    return bone_index

def get_ff_controls_struct_for_bones(bone_indexes):
    """
    Create a TsForceFeedbackConfig structure for the given bone indexes.
    Parameters:
        bone_indexes: List of bone indexes.
    Returns: 
            TsForceFeedbackConfig structure.
    """    
    ff_controls = (TsForceFeedbackConfig * len(bone_indexes))()
    for i in range(0, len(bone_indexes)):
        ff_controls[i].bone_index = bone_indexes[i]
    return ff_controls

def get_left_default_ff_controls_struct():
    """
    Create a default force feedback controls struct for the left hand.
    Returns:
        TsForceFeedbackConfig structure.
    """
    return get_ff_controls_struct_for_bones(LEFT_BONE_INDEXES)

def get_right_default_ff_controls_struct():
    """
    Create a default force feedback controls struct for the right hand.
    Returns:
        TsForceFeedbackConfig structure.
    """
    return get_ff_controls_struct_for_bones(RIGHT_BONE_INDEXES)
