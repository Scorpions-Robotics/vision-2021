
from networktables import NetworkTables

NetworkTables.initialize("roborio-7672-frc.local")
nt = NetworkTables.getTable("vision")

while True:
    print("X", nt.getString("X", ""))
    print("Y", nt.getString("Y", ""))
    print("W", nt.getString("W", ""))
    print("H", nt.getString("H", ""))
    print("D", nt.getString("D", ""))
    print("B", nt.getNumber("B", -1))
    print("R", nt.getString("R", ""))
    