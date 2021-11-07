
from networktables import NetworkTables

NetworkTables.initialize("roborio-7672-frc.local")
nt = NetworkTables.getTable("vision")

while True:
    print("X", nt.getNumber("X", -1))
    print("Y", nt.getNumber("Y", -1))
    print("W", nt.getNumber("W", -1))
    print("H", nt.getNumber("H", -1))
    print("D", nt.getNumber("D", -1))
    print("B", nt.getNumber("B", -1))
    print("R", nt.getNumber("R", -1))
    