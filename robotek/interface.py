from tkinter import *
from PIL import Image, ImageTk
from omron_2jcie_bu01_interact import Omron2JCIE_BU01
import asyncio
import atexit
import keyboard
import sys
from datetime import datetime, timedelta, tzinfo
import threading
import os

file_name = "Omron-2jcie-bu01-data.txt"

home_dir = os.path.expanduser("~")

file_path_desktop = os.path.join(home_dir, "Desktop", file_name)
file_path_secret = os.path.join(home_dir, "Documents", "Robotek", file_name)

s = Omron2JCIE_BU01.serial("COM3")

root = Tk()
root.iconify()

myLabel = Label(root, text="Lukk vinduet for å \n skru av Omron-sensor", font="Futura 15")
myLabel.place(relx=0.5, rely=0.5, anchor=CENTER)

counter3 = 0

print(os.path.getsize(file_path_secret))

class Worker(threading.Thread):
    def __init__(self):
        super(Worker, self).__init__()

        self.run_event = threading.Event()

    def run(self):
        self.run_event.wait()

        global counter3
        if counter3 == 0:
            s.led(0x01, (0, 255, 0))
        # info3 = s.latest_acceleration_status()
        prev_time = ""
        prev_acc_x = 0
        prev_acc_y = 0
        prev_acc_z = 0
        global counter
        counter = 0
        counter2 = 0

        while self.run_event.is_set() and counter3 == 0:
            global worker_thread
            global run_program
            run_program = True
            print(worker_thread.is_alive()) # dette er en print
            if counter2 > 0:
                counter2 -= 1
            dt = datetime.now()
            time_now = dt.strftime('%H:%M:%S')
            date = dt.strftime('%d/%m/%Y')
            info = s.latest_calculation_data()
            acc_x = abs(info.acc_x)
            acc_y = abs(info.acc_y)
            acc_z = abs(info.acc_z)

            
            # print(f'''
            # Forrige målinger:        {prev_acc_x}, {prev_acc_y}, {prev_acc_z}
            # Nåværende målinger:      {acc_x}, {acc_y}, {acc_z}
            # ''')

            if counter == 0:
                prev_acc_x = acc_x
                prev_acc_y = acc_y
                prev_acc_z = acc_z
                counter += 1
                continue

            if abs(acc_x - prev_acc_x) > 400 or abs(acc_y - prev_acc_y) > 400:
                s.led(0x01, (255, 0, 0))
                write_data(date, time_now)
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

            time_now_list_2 = datetime.now().strftime('%H:%M:%S').split(":")
            time_now_list_2_int = [int(tall) for tall in time_now_list_2]
            
            if time_now_list_2_int == future_time:
                continue

            asyncio.run(sleep_until(future_time[0], future_time[1], future_time[2]))

        counter3 = 0


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

def exit():
    global worker_thread
    global run_program
    global counter3
    if not run_program:
        counter3 = 1
        worker_thread.run_event.set()
        s.led(0x00, (255, 0, 0))
        print("Program avsluttes")
        sys.exit(0)
    print(worker_thread.is_alive())
    if worker_thread.is_alive():
        worker_thread.run_event.clear()
    print("Program avsluttes")
    s.led(0x00, (255, 0, 0))
    sys.exit(0)

def write_data(date, time_now):
    first_line = "This document contains the time and date for when Omron 2JCIE-BU01 sensor registered a reading that exceeded the accepted limit - hence turning the led red"
    with open(file_path_desktop, 'a+') as f1, open(file_path_secret, 'a+') as f2:
        file_size_desktop = os.path.getsize(file_path_desktop)
        file_size_secret = os.path.getsize(file_path_secret)
        print(file_size_secret)
        if file_size_desktop == 0:
            f1.write(first_line)
            f1.write('\n')
            f1.write('\n')
        if file_size_secret == 0:
            f2.write(first_line)
            f2.write('\n')
            f2.write('\n')
        f1.write(date + " at " + time_now)
        f1.write('\n')
        f2.write(date + " at " + time_now)
        f2.write('\n')

worker_thread = Worker()
worker_thread.start()
worker_thread.run_event.set()
print("Program starter")
run_program = False

image_path = file_path_secret = os.path.join(home_dir, "Documents", "Robotek", "icon.ico")
ico = Image.open(image_path)
photo = ImageTk.PhotoImage(ico)
root.wm_iconphoto(False, photo)

root.title("Omron 2JCIE-BU01")
root.geometry("300x150")

root.protocol("WM_DELETE_WINDOW", exit)

root.mainloop()