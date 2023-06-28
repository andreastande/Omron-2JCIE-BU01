import time
from datetime import datetime, timedelta, tzinfo
from omron import Omron2JCIE_BU01
import asyncio

s = Omron2JCIE_BU01.serial("COM3")
s.led(0x01, (0, 255, 0))
# info3 = s.latest_acceleration_status()
prev_time = ""
prev_acc_x = 0
prev_acc_y = 0
prev_acc_z = 0
counter = 0
counter2 = 0

async def sleep_until(hour: int, minute: int, second: int):
    """Asynchronous wait until specific hour, minute and second

    Args:
        hour (int): Hour
        minute (int): Minute
        second (int): Second

    """
    t = datetime.today()
    future = datetime(t.year, t.month, t.day, int(hour), int(minute), int(second))
    if t.timestamp() > future.timestamp():
        future += timedelta(days=1)
    await asyncio.sleep((future - t).total_seconds())

while True:
    if counter2 > 0:
        counter2 -= 1
    dt = datetime.now()
    time_now = dt.strftime('%H:%M:%S')
    info = s.latest_calculation_data()
    acc_x = abs(info.acc_x)
    acc_y = abs(info.acc_y)
    acc_z = abs(info.acc_z)

    print(f'''
    Forrige målinger:        {prev_acc_x}, {prev_acc_y}, {prev_acc_z}
    Nåværende målinger:      {acc_x}, {acc_y}, {acc_z}
    ''')

    if counter == 0:
        prev_acc_x = acc_x
        prev_acc_y = acc_y
        prev_acc_z = acc_z
        counter += 1
        continue

    if abs(acc_x - prev_acc_x) > 400 or abs(acc_y - prev_acc_y) > 400:
        s.led(0x01, (255, 0, 0))
        counter2 = 10
    else:
        if counter2 == 0:
            s.led(0x01, (0, 255, 0))

    prev_time = datetime.now().strftime('%H:%M:%S')
    prev_acc_x = acc_x
    prev_acc_y = acc_y
    prev_acc_z = acc_z
 
    time_now_list = time_now.split(":")
    future_time = []
    if int(time_now_list[2]) == 59:
        if int(time_now_list[1]) == 59:
            if int(time_now_list[2]) == 23:
                future_time = [int(0), int(0), int(0)]
            else:
                future_time = [int(time_now_list[0]) + 1, int(0), int(0)]
        else:
            future_time = [int(time_now_list[0]), int(time_now_list[1]) + 1, int(0)]
    else:
        future_time = [int(time_now_list[0]), int(time_now_list[1]), int(time_now_list[2]) + 1]

    if datetime.now().strftime('%H:%M:%S').split(":") == future_time:
        continue

    asyncio.run(sleep_until(future_time[0], future_time[1], future_time[2]))









'''
print(f"\n Date                : {dt.strftime('%H:%M:%S')} \n")

print(f" Acceleration X   : {info2.acc_x}")
print(f" Acceleration Y   : {info2.acc_y}")
print(f" Acceleration Z   : {info2.acc_z} \n")

print(f" Max Acceleration X   : {info3.max_acc_x}")
print(f" Max Acceleration Y   : {info3.max_acc_y}")
print(f" Max Acceleration Z   : {info3.max_acc_z}")
'''
