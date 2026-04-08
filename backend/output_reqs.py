class ConstructionType(str, Enum):
    WALL = "wall"
    ROOF = "roof"
    CEILING_EXT = "ceiling_ext"
    CEILING = "ceiling"
    INT_HOR_10 = "int_hor_10"
    INT_HOR_15 = "int_hor_15"
    INT_HOR_20 = "int_hor_20"
    INT_HOR_25 = "int_hor_25"
    INT_HOR_OVER25 = "int_hor_over25"
    INT_UP_10 = "int_up_10"
    INT_UP_15 = "int_up_15"
    INT_UP_20 = "int_up_20"
    INT_UP_25 = "int_up_25"
    INT_UP_OVER25 = "int_up_over25"
    INT_DOWN_10 = "int_down_10"
    INT_DOWN_15 = "int_down_15"
    INT_DOWN_20 = "int_down_20"
    INT_DOWN_25 = "int_down_25"
    INT_DOWN_OVER25 = "int_down_over25"
    EARTH_WALL_05 = "earth_wall_05"
    EARTH_WALL_20 = "earth_wall_20"
    EARTH_WALL_OVER20 = "earth_wall_over20"
    EARTH_FLOOR_EDGE = "earth_floor_edge"
    EARTH_FLOOR_OTHER = "earth_floor_other"

U_REQUIREMENTS_OPAQUE: dict[ConstructionType, dict[AssessmentLevel, float]] = {
    ConstructionType.WALL: {
        AssessmentLevel.U_MAX: 0.461,
        AssessmentLevel.U_N: 0.315,
        AssessmentLevel.U_R1: 0.219,
        AssessmentLevel.U_R2: 0.15,
    },
    ConstructionType.ROOF: {
        AssessmentLevel.U_MAX: 0.299,
        AssessmentLevel.U_N: 0.198,
        AssessmentLevel.U_R1: 0.151,
        AssessmentLevel.U_R2: 0.1,
    },
    ConstructionType.CEILING_EXT: {
        AssessmentLevel.U_MAX: 0.309,
        AssessmentLevel.U_N: 0.202,
        AssessmentLevel.U_R1: 0.151,
        AssessmentLevel.U_R2: 0.101,
    },
    ConstructionType.CEILING: {
        AssessmentLevel.U_MAX: 0.329,
        AssessmentLevel.U_N: 0.236,
        AssessmentLevel.U_R1: 0.191,
        AssessmentLevel.U_R2: 0.146,
    },
    ConstructionType.INT_HOR_10: {
        AssessmentLevel.U_MAX: 2.778,
        AssessmentLevel.U_N: 1.515,
        AssessmentLevel.U_R1: 1.163,
        AssessmentLevel.U_R2: 1.042,
    },
    ConstructionType.INT_HOR_15: {
        AssessmentLevel.U_MAX: 1.786,
        AssessmentLevel.U_N: 1.042,
        AssessmentLevel.U_R1: 0.735,
        AssessmentLevel.U_R2: 0.685,
    },
    ConstructionType.INT_HOR_20: {
        AssessmentLevel.U_MAX: 1.316,
        AssessmentLevel.U_N: 0.794,
        AssessmentLevel.U_R1: 0.602,
        AssessmentLevel.U_R2: 0.538,
    },
    ConstructionType.INT_HOR_25: {
        AssessmentLevel.U_MAX: 1.042,
        AssessmentLevel.U_N: 0.641,
        AssessmentLevel.U_R1: 0.538,
        AssessmentLevel.U_R2: 0.442,
    },
    ConstructionType.INT_HOR_OVER25: {
        AssessmentLevel.U_MAX: 0.794,
        AssessmentLevel.U_N: 0.442,
        AssessmentLevel.U_R1: 0.407,
        AssessmentLevel.U_R2: 0.35,
    },
    ConstructionType.INT_UP_10: {
        AssessmentLevel.U_MAX: 3.333,
        AssessmentLevel.U_N: 1.667,
        AssessmentLevel.U_R1: 1.25,
        AssessmentLevel.U_R2: 0.909,
    },
    ConstructionType.INT_UP_15: {
        AssessmentLevel.U_MAX: 2.0,
        AssessmentLevel.U_N: 1.111,
        AssessmentLevel.U_R1: 0.769,
        AssessmentLevel.U_R2: 0.5,
    },
    ConstructionType.INT_UP_20: {
        AssessmentLevel.U_MAX: 1.429,
        AssessmentLevel.U_N: 0.833,
        AssessmentLevel.U_R1: 0.588,
        AssessmentLevel.U_R2: 0.345,
    },
    ConstructionType.INT_UP_25: {
        AssessmentLevel.U_MAX: 1.111,
        AssessmentLevel.U_N: 0.714,
        AssessmentLevel.U_R1: 0.5,
        AssessmentLevel.U_R2: 0.303,
    },
    ConstructionType.INT_UP_OVER25: {
        AssessmentLevel.U_MAX: 0.833,
        AssessmentLevel.U_N: 0.5,
        AssessmentLevel.U_R1: 0.4,
        AssessmentLevel.U_R2: 0.25,
    },
    ConstructionType.INT_DOWN_10: {
        AssessmentLevel.U_MAX: 2.273,
        AssessmentLevel.U_N: 1.351,
        AssessmentLevel.U_R1: 0.877,
        AssessmentLevel.U_R2: 0.61,
    },
    ConstructionType.INT_DOWN_15: {
        AssessmentLevel.U_MAX: 1.562,
        AssessmentLevel.U_N: 0.962,
        AssessmentLevel.U_R1: 0.61,
        AssessmentLevel.U_R2: 0.352,
    },
    ConstructionType.INT_DOWN_20: {
        AssessmentLevel.U_MAX: 1.19,
        AssessmentLevel.U_N: 0.746,
        AssessmentLevel.U_R1: 0.49,
        AssessmentLevel.U_R2: 0.248,
    },
    ConstructionType.INT_DOWN_25: {
        AssessmentLevel.U_MAX: 0.962,
        AssessmentLevel.U_N: 0.61,
        AssessmentLevel.U_R1: 0.394,
        AssessmentLevel.U_R2: 0.198,
    },
    ConstructionType.INT_DOWN_OVER25: {
        AssessmentLevel.U_MAX: 0.746,
        AssessmentLevel.U_N: 0.394,
        AssessmentLevel.U_R1: 0.299,
        AssessmentLevel.U_R2: 0.151,
    },
    ConstructionType.EARTH_WALL_05: {
        AssessmentLevel.U_MAX: 0.613,
        AssessmentLevel.U_N: 0.469,
        AssessmentLevel.U_R1: 0.38,
        AssessmentLevel.U_R2: 0.38,
    },
    ConstructionType.EARTH_WALL_20: {
        AssessmentLevel.U_MAX: 0.885,
        AssessmentLevel.U_N: 0.613,
        AssessmentLevel.U_R1: 0.469,
        AssessmentLevel.U_R2: 0.469,
    },
    ConstructionType.EARTH_WALL_OVER20: {
        AssessmentLevel.U_MAX: 1.205,
        AssessmentLevel.U_N: 0.752,
        AssessmentLevel.U_R1: 0.613,
        AssessmentLevel.U_R2: 0.613,
    },
    ConstructionType.EARTH_FLOOR_EDGE: {
        AssessmentLevel.U_MAX: 0.599,
        AssessmentLevel.U_N: 0.405,
        AssessmentLevel.U_R1: 0.375,
        AssessmentLevel.U_R2: 0.375,
    },
    ConstructionType.EARTH_FLOOR_OTHER: {
        AssessmentLevel.U_MAX: 0.855,
        AssessmentLevel.U_N: 0.599,
        AssessmentLevel.U_R1: 0.461,
        AssessmentLevel.U_R2: 0.461,
    },
}
