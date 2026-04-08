def u_val(r, r_surfaces):
    return round(1.0 / (r + r_surfaces), 3)

tables = {
    "WALL": (0.17, [2.0, 3.0, 4.4, 6.5]),
    "ROOF": (0.14, [3.2, 4.9, 6.5, 9.9]),
    "CEILING_EXT": (0.14, [3.1, 4.8, 6.5, 9.8]),
    "CEILING": (0.34, [2.7, 3.9, 4.9, 6.5]), # 0.17 + 0.17 = 0.34 (strop downward ? no, from interior 0.10, from top 0.10 => 0.20? Wait! STN 73 0540-2 says Ceiling under unheated space has required values: "Strop pod nevykurovaným priestorom": b) means "tepelný tok nahor". So Rsi=0.10, Rse=0.10 => 0.20)

    "INT_HOR_10": (0.26, [0.1, 0.4, 0.6, 0.7]),
    "INT_HOR_15": (0.26, [0.3, 0.7, 1.1, 1.2]),
    "INT_HOR_20": (0.26, [0.5, 1.0, 1.4, 1.6]),
    "INT_HOR_25": (0.26, [0.7, 1.3, 1.6, 2.0]),
    "INT_HOR_OVER25": (0.26, [1.0, 2.0, 2.2, 2.6]),

    "INT_UP_10": (0.20, [0.1, 0.4, 0.6, 0.9]),
    "INT_UP_15": (0.20, [0.3, 0.7, 1.1, 1.8]),
    "INT_UP_20": (0.20, [0.5, 1.0, 1.5, 2.7]),
    "INT_UP_25": (0.20, [0.7, 1.2, 1.8, 3.1]),
    "INT_UP_OVER25": (0.20, [1.0, 1.8, 2.3, 3.8]),

    "INT_DOWN_10": (0.34, [0.1, 0.4, 0.8, 1.3]),
    "INT_DOWN_15": (0.34, [0.3, 0.7, 1.3, 2.5]),
    "INT_DOWN_20": (0.34, [0.5, 1.0, 1.7, 3.7]),
    "INT_DOWN_25": (0.34, [0.7, 1.3, 2.2, 4.7]),
    "INT_DOWN_OVER25": (0.34, [1.0, 2.2, 3.0, 6.3]),

    "EARTH_WALL_05": (0.13, [1.5, 2.0, 2.5, 2.5]),
    "EARTH_WALL_20": (0.13, [1.0, 1.5, 2.0, 2.0]),
    "EARTH_WALL_OVER20": (0.13, [0.7, 1.2, 1.5, 1.5]),

    "EARTH_FLOOR_EDGE": (0.17, [1.5, 2.3, 2.5, 2.5]),
    "EARTH_FLOOR_OTHER": (0.17, [1.0, 1.5, 2.0, 2.0]),
}

with open("output_reqs.py", "w") as f:
    f.write("class ConstructionType(str, Enum):\n")
    for k in tables.keys():
        f.write(f'    {k} = "{k.lower()}"\n')
        
    f.write("\nU_REQUIREMENTS_OPAQUE: dict[ConstructionType, dict[AssessmentLevel, float]] = {\n")
    for k, (surfaces, r_list) in tables.items():
        u_list = [u_val(r, surfaces) for r in r_list]
        f.write(f"    ConstructionType.{k.upper()}: {{\n")
        f.write(f"        AssessmentLevel.U_MAX: {u_list[0]},\n")
        f.write(f"        AssessmentLevel.U_N: {u_list[1]},\n")
        f.write(f"        AssessmentLevel.U_R1: {u_list[2]},\n")
        f.write(f"        AssessmentLevel.U_R2: {u_list[3]},\n")
        f.write(f"    }},\n")
    f.write("}\n")
