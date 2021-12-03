from networktables import NetworkTables

NetworkTables.initialize("roborio-7672-frc.local")
table = NetworkTables.getTable("vision")


def try_get_value(key):
    return table.getString(key, "")


while True:
    try:
        x = try_get_value("X")
        y = try_get_value("Y")
        w = try_get_value("W")
        h = try_get_value("H")
        d = try_get_value("D")
        r = try_get_value("R")
        b = try_get_value("B")

        print(f"X: {x} Y: {y} W: {w} H: {h} D: {d} R: {r} B: {b}")

    except KeyboardInterrupt:
        break
