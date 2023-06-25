#!/usr/bin/env python3
import sys
sys.path.insert(0, "../lib-ext")
sys.path.insert(0, "..")

import time
from datetime import datetime, timedelta, tzinfo
from omron_2jcie_bu01 import Omron2JCIE_BU01

s = Omron2JCIE_BU01.serial("COM3")
# info3 = s.latest_acceleration_status()
prev_time = ""
counter = 0

while True:
    dt = datetime.now()
    time_now = dt.strftime('%H:%M:%S')
    if counter == 0:
        prev_time = time_now
        counter += 1
        continue

    info = s.latest_calculation_data()
    acc_x = info.acc_x
    acc_y = info.acc_y
    acc_z = info.acc_z

    




print(f"\n Date                : {dt.strftime('%H:%M:%S')} \n")

print(f" Acceleration X   : {info2.acc_x}")
print(f" Acceleration Y   : {info2.acc_y}")
print(f" Acceleration Z   : {info2.acc_z} \n")

print(f" Max Acceleration X   : {info3.max_acc_x}")
print(f" Max Acceleration Y   : {info3.max_acc_y}")
print(f" Max Acceleration Z   : {info3.max_acc_z}")
