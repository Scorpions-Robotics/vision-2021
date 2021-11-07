from networktables import NetworkTables


NetworkTables.initialize(server="roborio-7672-frc.local")
table = NetworkTables.getTable("vision")

while True:
    x = table.getNumber("X", 0)
    print(x)
