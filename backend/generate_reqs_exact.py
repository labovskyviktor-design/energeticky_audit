tables_u = {
    "WALL": [0.46, 0.32, 0.22, 0.15],
    "ROOF": [0.3, 0.2, 0.15, 0.1],
    "CEILING_EXT": [0.3, 0.2, 0.15, 0.1],
    "CEILING": [0.35, 0.25, 0.20, 0.15],
    
    "INT_HOR_10": [2.75, 1.5, 1.2, 1],
    "INT_UP_10": [3.35, 1.7, 1.2, 0.95],
    "INT_DOWN_10": [2.3, 1.35, 0.85, 0.6],

    "INT_HOR_15": [1.8, 1.05, 0.75, 0.7],
    "INT_UP_15": [2, 1.1, 0.75, 0.5],
    "INT_DOWN_15": [1.6, 0.95, 0.6, 0.35],

    "INT_HOR_20": [1.3, 0.8, 0.60, 0.55],
    "INT_UP_20": [1.45, 0.85, 0.6, 0.35],
    "INT_DOWN_20": [1.2, 0.75, 0.5, 0.25],

    "INT_HOR_25": [1.05, 0.65, 0.55, 0.45],
    "INT_UP_25": [1.1, 0.7, 0.5, 0.3],
    "INT_DOWN_25": [0.95, 0.6, 0.4, 0.2],

    "INT_HOR_OVER25": [0.8, 0.45, 0.40, 0.35],
    "INT_UP_OVER25": [0.85, 0.5, 0.4, 0.25],
    "INT_DOWN_OVER25": [0.75, 0.4, 0.3, 0.15],
    
    # Keeping previously calculated from R equivalents for Earth
    "EARTH_WALL_05": [0.613, 0.469, 0.38, 0.38],
    "EARTH_WALL_20": [0.885, 0.613, 0.469, 0.469],
    "EARTH_WALL_OVER20": [1.205, 0.752, 0.613, 0.613],
    "EARTH_FLOOR_EDGE": [0.599, 0.405, 0.375, 0.375],
    "EARTH_FLOOR_OTHER": [0.855, 0.599, 0.461, 0.461],
}

with open("output_reqs_rounded.py", "w") as f:
    f.write("U_REQUIREMENTS_OPAQUE: dict[ConstructionType, dict[AssessmentLevel, float]] = {\n")
    for k, u_list in tables_u.items():
        f.write(f"    ConstructionType.{k.upper()}: {{\n")
        f.write(f"        AssessmentLevel.U_MAX: {u_list[0]},\n")
        f.write(f"        AssessmentLevel.U_N: {u_list[1]},\n")
        f.write(f"        AssessmentLevel.U_R1: {u_list[2]},\n")
        f.write(f"        AssessmentLevel.U_R2: {u_list[3]},\n")
        f.write(f"    }},\n")
    f.write("}\n")
