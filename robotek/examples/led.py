from omron_2jcie_bu01_interact import Omron2JCIE_BU01

s = Omron2JCIE_BU01.serial("COM3")
#s = Omron2JCIE_BU01.serial("/dev/ttyUSB0")

# Show current setting
print(s.led())

# rule=0x06 (noise)
# rgb=(0, 255, 200)
s.led(0x00, (255, 255, 0))