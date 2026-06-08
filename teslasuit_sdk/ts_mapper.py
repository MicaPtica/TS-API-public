from ctypes import (c_void_p, c_uint8,
                    POINTER, pointer,
                    c_uint64, Structure,
                    c_float)
from enum import IntEnum, unique


class TsVec2f(Structure):
    """
    Vector 2D float struct.
    Represent a point in 2d space.
    Attributes:
        x (float): X coordinate.
        y (float): Y coordinate.
    """
    _pack_ = 1
    _fields_ = [('x', c_float),
                ('y', c_float)]

    def __str__(self):
        return f'{self.x};{self.y}'


@unique
class TsMapping2dVersion(IntEnum):
    """
    Mapping version.

    Possible values:
        Undefined = 0,
        Mapping_4_5_4 = 1,
        Mapping_4_5_5 = 2,
        Mapping_4_6_0 = 3,
        MappingLeftGlove_1_0_0 = 4,
        MappingRightGlove_1_0_0 = 5,
        Mapping_4_5_4_Legacy = 6,
        Mapping_4_5_5_Legacy = 7,
        Mapping_5_0_0 = 8,
        MappingLeftGlove_1_2_0 = 9,
        MappingRightGlove_1_2_0 = 10,
        Mapping_5_0_1 = 11,
        Mapping_5_0_2 = 12,
        Mapping_5_0_3 = 13,
        Mapping_4_7_0 = 14,
        MappingLeftGlove_1_3_0 = 15,
        MappingRightGlove_1_3_0 = 16,
        Mapping_4_X_Medical = 17,
        Mapping_4_5_6 = 18
    """
    Undefined = 0
    Mapping_4_5_4 = 1
    Mapping_4_5_5 = 2
    Mapping_4_6_0 = 3
    MappingLeftGlove_1_0_0 = 4
    MappingRightGlove_1_0_0 = 5
    Mapping_4_5_4_Legacy = 6
    Mapping_4_5_5_Legacy = 7
    Mapping_5_0_0 = 8
    MappingLeftGlove_1_2_0 = 9
    MappingRightGlove_1_2_0 = 10
    Mapping_5_0_1 = 11
    Mapping_5_0_2 = 12
    Mapping_5_0_3 = 13
    Mapping_4_7_0 = 14    
    MappingLeftGlove_1_3_0 = 15,
    MappingRightGlove_1_3_0 = 16,
    Mapping_4_X_Medical = 17,
    Mapping_4_5_6 = 18,
    Mapping_5_1_0_Men = 19,
    Mapping_5_1_0_Women = 20


@unique
class TsLayout2dType(IntEnum):
    """
    Layout2dType represents a type of layout.
    Layout2dType is used to identify the type of layout in the mapping.
    """
    Undefined = 0
    Electric = 1
    Temperature = 2
    Vibration = 3
    Emg = 4
    Ecg = 5


@unique
class TsLayout2dElementType(IntEnum):
    """
    Layout element type.
    Possible values:
        Undefined = 0,
        Cell = 1,
        Channel = 2
    """
    Undefined = 0
    Cell = 1
    Channel = 2


@unique
class TsBone2dIndex(IntEnum):
    """
    Bone2dIndex represents a bone index in the mapping.
    Bone2dIndex is used to identify the bone in the mapping.
    Possible values:
        Hips = 0,
        LeftUpperLeg = 1,
        RightUpperLeg = 2,
        LeftLowerLeg = 3,
        RightLowerLeg = 4,
        LeftFoot = 5,
        RightFoot = 6,
        Spine = 7,
        Chest = 8,
        UpperChest = 9,
        Neck = 10,
        Head = 11,
        LeftShoulder = 12,
        RightShoulder = 13,
        LeftUpperArm = 14,
        RightUpperArm = 15,
        LeftLowerArm = 16,
        RightLowerArm = 17,
        LeftHand = 18,
        RightHand = 19,
        LeftThumbProximal = 20,
        LeftThumbIntermediate = 21,
        LeftThumbDistal = 22,
        LeftIndexProximal = 23,
        LeftIndexIntermediate = 24,
        LeftIndexDistal = 25,
        LeftMiddleProximal = 26,
        LeftMiddleIntermediate = 27,
        LeftMiddleDistal = 28,
        LeftRingProximal = 29,
        LeftRingIntermediate = 30,
        LeftRingDistal = 31,
        LeftLittleProximal = 32,
        LeftLittleIntermediate = 33,
        LeftLittleDistal = 34,
        RightThumbProximal = 35,
        RightThumbIntermediate = 36,
        RightThumbDistal = 37,
        RightIndexProximal = 38,
        RightIndexIntermediate = 39,
        RightIndexDistal = 40,
        RightMiddleProximal = 41,
        RightMiddleIntermediate = 42,
        RightMiddleDistal = 43,
        RightRingProximal = 44,
        RightRingIntermediate = 45,
        RightRingDistal = 46,
        RightLittleProximal = 47,
        RightLittleIntermediate = 48,
        RightLittleDistal = 49
    """
    Hips = 0
    LeftUpperLeg = 1
    RightUpperLeg = 2
    LeftLowerLeg = 3
    RightLowerLeg = 4
    LeftFoot = 5
    RightFoot = 6
    Spine = 7
    Chest = 8
    UpperChest = 9
    Neck = 10
    Head = 11
    LeftShoulder = 12
    RightShoulder = 13
    LeftUpperArm = 14
    RightUpperArm = 15
    LeftLowerArm = 16
    RightLowerArm = 17
    LeftHand = 18
    RightHand = 19
    LeftThumbProximal = 20
    LeftThumbIntermediate = 21
    LeftThumbDistal = 22
    LeftIndexProximal = 23
    LeftIndexIntermediate = 24
    LeftIndexDistal = 25
    LeftMiddleProximal = 26
    LeftMiddleIntermediate = 27
    LeftMiddleDistal = 28
    LeftRingProximal = 29
    LeftRingIntermediate = 30
    LeftRingDistal = 31
    LeftLittleProximal = 32
    LeftLittleIntermediate = 33
    LeftLittleDistal = 34
    RightThumbProximal = 35
    RightThumbIntermediate = 36
    RightThumbDistal = 37
    RightIndexProximal = 38
    RightIndexIntermediate = 39
    RightIndexDistal = 40
    RightMiddleProximal = 41
    RightMiddleIntermediate = 42
    RightMiddleDistal = 43
    RightRingProximal = 44
    RightRingIntermediate = 45
    RightRingDistal = 46
    RightLittleProximal = 47
    RightLittleIntermediate = 48
    RightLittleDistal = 49


@unique
class TsBone2dSide(IntEnum):
    """
    Bone side.
    Possible values:
        Undefined = 0,
        Front = 1,
        Back = 2
    """
    Undefined = 0
    Front = 1
    Back = 2

@unique
class TsBiomechanicalIndex(IntEnum):
    """
    Biomechanical index used to identify plane of movement in mocap data writing.
    Possible values:
        PelvisTilt = 0,
        PelvisList = 1,
        PelvisRotation = 2,
        HipFlexExtR = 3,
        HipAddAbdR = 4,
        HipRotR = 5,
        KneeFlexExtR = 6,
        AnkleFlexExtR = 7,
        AnkleProSupR = 8,
        HipFlexExtL = 9,
        HipAddAbdL = 10,
        HipRotL = 11,
        KneeFlexExtL = 12,
        AnkleFlexExtL = 13,
        AnkleProSupL = 14,
        ElbowFlexExtR = 15,
        ForearmProSupR = 16,
        WristFlexExtR = 17,
        WristDeviationR = 18,
        ElbowFlexExtL = 19,
        ForearmProSupL = 20,
        WristFlexExtL = 21,
        WristDeviationL = 22,
        ShoulderAddAbdR = 36,
        ShoulderRotR = 37,
        ShoulderFlexExtR = 38,
        ShoulderAddAbdL = 39,
        ShoulderRotL = 40,
        ShoulderFlexExtL = 41
    """
    PelvisTilt = 0
    PelvisList = 1
    PelvisRotation = 2
    HipFlexExtR = 3
    HipAddAbdR = 4
    HipRotR = 5
    KneeFlexExtR = 6
    AnkleFlexExtR = 7
    AnkleProSupR = 8
    HipFlexExtL = 9
    HipAddAbdL = 10
    HipRotL = 11
    KneeFlexExtL = 12
    AnkleFlexExtL = 13
    AnkleProSupL = 14
    ElbowFlexExtR = 15
    ForearmProSupR = 16
    WristFlexExtR = 17
    WristDeviationR = 18
    ElbowFlexExtL = 19
    ForearmProSupL = 20
    WristFlexExtL = 21
    WristDeviationL = 22
    ShoulderAddAbdR = 36
    ShoulderRotR = 37
    ShoulderFlexExtR = 38
    ShoulderAddAbdL = 39
    ShoulderRotL = 40
    ShoulderFlexExtL = 41

class TsBoneContentType(Structure):
    """
    BoneContentType represents a type of element and layout tyoe of bone content.
    Attributes:
        layout_type (c_uint8): layout type
        element_type (c_uint8): element type
    Possible values:
        layout_type: 0 - 2
    """ ### Depricated??? not used in the code
    _pack_ = 1
    _fields_ = [('layout_type', c_uint8),
                ('element_type', c_uint8)]


class TsBoneId(Structure):
    """
    BoneId represents a bone index and side. 
    Attributes:
        bone_index (c_uint8): bone index
        bone_side (c_uint8): bone side
    Possible values:
        bone_index: 0 - 49
        bone_side: 0 - 2
    """ ### Depricated??? not used in the code
    _pack_ = 1
    _fields_ = [('bone_index', c_uint8),
                ('bone_side', c_uint8)]


class TsBone(Structure):
    """
    Represents a bone data in the mapping.
    Attributes:
        id (c_uint8): bone id
        bone_index (c_uint8): bone index
        bone_side (c_uint8): bone side
        channels (c_uint8): bone channels
    """
    _pack_ = 1
    _fields_ = [('id', c_uint8),
                ('bone_index', c_uint8),
                ('bone_side', c_uint8),
                ('channels', c_uint8)]


class TsLayout(Structure):
    """
    Represents a layout data in the mapping.
    Attributes:
        id (c_uint8): layout id
        layout_type (c_uint8): layout type
        element_type (c_uint8): element type
        layout_index (c_uint8): layout index
        bone (POINTER(TsBone)): pointer to a bone
    """
    _pack_ = 1
    _fields_ = [('id', c_uint8),
                ('layout_type', c_uint8),
                ('element_type', c_uint8),
                ('layout_index', c_uint8),
                ('bone', POINTER(TsBone))]


class TsMappingData(Structure):
    """
    MappingData represents a set of device's elements mapped on 2d space.
    Attributes:
        mapping_handle (c_void_p): mapping handle
        layouts (POINTER(TsLayout)): pointer to an array of layouts
    """
    _pack_ = 1
    _fields_ = [('mapping_handle', c_void_p),
                ('layouts', POINTER(TsLayout))]


class TsMapper:
    """
    Mapping represents a set of device's elements mapped on 2d space.
    Elements are described by the 2D Polygon - an array of points.
    Elements are bound to bones, a full set of bones is included in a layout, 
    multiple layouts with the same element types are contained in an array,
    an array of layouts with same type are packed by TsLayout2dType and TsLayout2dElementType.
    Mappings might have different versions. 
    Mapping can be requested by a mapping version or by a device handler because each device has a bound mapping version by default.
    """
    def __init__(self, lib):
        self.__lib = lib

    def get_mapping_by_device(self, device):
        """
        Get default mapping2d handler for a device.
        Args:
            device (TsDevice): device handle
        Returns:
            TsMapping2d: mapping2d handler
        """
        mapping = c_void_p()
        self.__lib.ts_mapping2d_get_by_device(device, pointer(mapping))

        return mapping.value

    def get_mapping_by_version(self, version):
        """
        Gets mapping2d handler by the mapping version.
        Args:
            version (TsMapping2dVersion): mapping version
        Returns:
            TsMapping2d: mapping2d handler
        """
        mapping = c_void_p(0)
        self.__lib.ts_mapping2d_get_by_version(c_uint8(version), pointer(mapping))

        return mapping

    def get_number_of_layouts(self, mapping):
        """
        Gets mapping2d layouts number.
        Args:
            mapping (TsMapping2d): mapping2d handler
        Returns:
            int: number of layouts
        """
        number_of_layouts = c_uint64(0)
        self.__lib.ts_mapping2d_get_number_of_layouts(c_void_p(mapping), pointer(number_of_layouts))

        return number_of_layouts.value

    def get_layouts(self, mapping):
        """
        Gets mapping2d layouts.
        Args:
            mapping (TsMapping2d): mapping2d handler
        Returns:
            list: list of layouts
        """
        number_of_layouts = self.get_number_of_layouts(mapping)
        layouts = (c_void_p * number_of_layouts)()

        self.__lib.ts_mapping2d_get_layouts(c_void_p(mapping), pointer(layouts), c_uint64(number_of_layouts))
        return [*layouts]

    def get_layout_index(self, layout):
        """
        Gets mapping2d layout index.
        Args:
            layout (TsLayout): layout handle
        Returns:
            int: layout index
        """
        layout_index = c_uint8(0)
        self.__lib.ts_mapping2d_layout_get_index(c_void_p(layout), pointer(layout_index))

        return layout_index.value

    def get_layout_type(self, layout):
        """
        Gets mapping2d layout type.
        Args:
            layout (TsLayout): layout handle
        Returns:
            int: layout type
        """
        layout_type = c_uint8(0)
        self.__lib.ts_mapping2d_layout_get_type(c_void_p(layout), pointer(layout_type))

        return layout_type.value

    def get_layout_element_type(self, layout):
        """
        Gets mapping2d layout element type.

        Args:
            layout (TsLayout): layout handle
        Returns:
            int: layout element type
        """
        layout_element_type = c_uint8(0)
        self.__lib.ts_mapping2d_layout_get_element_type(c_void_p(layout), pointer(layout_element_type))

        return layout_element_type.value

    def get_number_of_bones(self, layout):
        """
        Gets mapping2d layout bones number.

        Args:
            layout (TsLayout): layout handle
        Returns:
            int: number of bones
        """
        number_of_bones = c_uint64(0)
        self.__lib.ts_mapping2d_layout_get_number_of_bones(c_void_p(layout), pointer(number_of_bones))

        return number_of_bones.value

    def get_layout_bones(self, layout):
        """
        Gets mapping2d bones from provided layout.
        Receives possible pointers to bones, that can be used to get corresponding bone content such as cells and channels.
        Function fills preallocated array bone_ids with size.
        To allocate correct array bone_ids should be used ts_mapping2d_layout_get_number_of_bones.
        Args:
            layout (TsLayout): layout handle
        Returns:
            list: list of bones
        """
        number_of_bones = self.get_number_of_bones(layout)
        bones = (c_void_p * number_of_bones)()

        self.__lib.ts_mapping2d_layout_get_bones(c_void_p(layout), pointer(bones), c_uint64(number_of_bones))
        return [*bones]

    def get_bone_index(self, bone_handle):
        """
        Gets bone index from passed bone object.
        Args:
            bone_handle (TsBone): bone handle
        Returns:
            int: bone index
        """
        bone_index = c_uint8(0)
        self.__lib.ts_mapping2d_bone_get_index(c_void_p(bone_handle), pointer(bone_index))

        return bone_index.value

    def get_bone_side(self, bone_handle):
        """
        Gets bone side from passed bone object.
        Args:
            bone_handle (TsBone): bone handle
        Returns:
            int: bone side
        """
        bone_side = c_uint8(0)
        self.__lib.ts_mapping2d_bone_get_side(c_void_p(bone_handle), pointer(bone_side))

        return bone_side.value

    def get_bone_number_of_contents(self, bone_handle):
        """
        Gets mapping2d layout bone contents number.
        Args:
            bone_handle (TsBone): bone handle
        Returns:
            int: number of contents
        """
        number_of_contents = c_uint64(0)
        self.__lib.ts_mapping2d_bone_get_number_of_contents(c_void_p(bone_handle), pointer(number_of_contents))

        return number_of_contents.value

    def get_bone_contents(self, bone_handle):
        """
        Gets mapping2d layout bone content objects.
        Receives possible pointers to bone contents, that can be used to get corresponding bone content such as cells and channels.
        Function fills preallocated array bone_contents with size.
        To allocate correct array bone_contents should be used ts_mapping2d_bone_get_number_of_contents.
        Args:
            bone_handle (TsBone): bone handle
        Returns:
            list: list of bone contents
        """
        number_of_contents = self.get_bone_number_of_contents(bone_handle)
        bone_contents = (c_void_p * number_of_contents)()

        self.__lib.ts_mapping2d_bone_get_contents(c_void_p(bone_handle), pointer(bone_contents),
                                                  c_uint64(number_of_contents))
        return [*bone_contents]

    def get_bone_number_of_points(self, bone_handle):
        """
        Gets mapping2d layout bone content points number.

        Args:
            bone_handle (TsBone): bone handle
        Returns:
            int: number of points
        """
        number_of_points = c_uint64(0)
        self.__lib.ts_mapping2d_bone_content_get_number_of_points(c_void_p(bone_handle), pointer(number_of_points))

        return number_of_points.value

    def get_bone_points(self, bone_handle):
        """
        Gets mapping2d bone content shape points.
        Points represent a shape of bone content element in 2d space.
        Args:
            bone_handle (TsBone): bone handle
        Returns:
            list: list of points
        """
        number_of_points = self.get_bone_number_of_points(bone_handle)
        points = (TsVec2f * number_of_points)()

        self.__lib.ts_mapping2d_bone_content_get_points(c_void_p(bone_handle), pointer(points),
                                                        c_uint64(number_of_points))

        return [*points]


    # mapping utils

    def get_layout_by_type(self, mapping, layout_type, layout_element_type):
        """
        Get layout by type and element type.
        Args:
            mapping (TsMapping2d): mapping handle
            layout_type (int): layout type
            layout_element_type (int): layout element type
        Returns:
            TsLayout: layout handle
        """
        layouts = self.get_layouts(mapping)
        for layout in layouts:
            if self.get_layout_type(layout) == layout_type and self.get_layout_element_type(layout) == layout_element_type:
                return layout
        return None

    def get_haptic_electric_channel_layout(self, mapping):
        """
        Get haptic channel layout.
        Args:
            mapping (TsMapping2d): mapping handle
        Returns:
            TsLayout: electric channel layout handle
        """
        return self.get_layout_by_type(mapping, TsLayout2dType.Electric.value, TsLayout2dElementType.Channel.value)