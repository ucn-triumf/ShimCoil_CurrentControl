#!/usr/bin/python3

import serial
import time
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt

coil_sign=[1]*50 # initialize all coil signs to 1
print(coil_sign)

# coils you want to set to -1
coils_to_set_negative = [9,10,12,14,17,27,30,32,33,34,35,
                         43,44,45,46,47,49,24,25,26,
                         41,42,36,37,0,1,5,4,6,8]
# need to fix:  9

# change sign of coils to -1
for coil in coils_to_set_negative:
    coil_sign[coil] = -1

print("coil sign",coil_sign)

def CheckReadUntil(ser, readUntil):
    outputCharacters = ""
    while True:
        ch = ser.read().decode()
        if len(ch) == 0:
            break
        outputCharacters += ch
        if outputCharacters[-len(readUntil):] == readUntil:
            break
    outputLines = ''.join(outputCharacters)
    return outputLines

def set_voltage(ser, chip_select, channel, voltage):
    ser.write(f'<SET {chip_select} {channel} {voltage}>\n'.encode())
    line = CheckReadUntil(ser, "V\r\n")
    parsing = line.split(" ")
    voltage_readback = float(parsing[11])
    print(f"Set voltage for channel {channel} (Chip Select {chip_select}) to {voltage}, readback: {voltage_readback}")

def zero_all_voltages():
    ser.write(f'<ZERO>\n'.encode())
    line = CheckReadUntil(ser, "Done zeroing.\r\n")
    print(line)
    if 'Done zeroing.' in line:
        print("All voltages set to zero")
    else:
        print("Failed to set all voltages to zero")


def mux_all_voltages():
    for cs in [7,8,9,10]:
        for ch in range(0,16):
            ser.write(f'<MUX {cs} {ch}>\n'.encode())
            time.sleep(2)
            line = CheckReadUntil(ser, "Changing MUX\r\n")
            if 'Changing MUX' in line:
                print(f"MUX changed successfully to {cs} {ch}")
            else:
                print("Failed to change MUX")

def set_individual_voltage():
    chip_select = int(chip_select_entry.get())
    channel = int(channel_entry.get())
    voltage = float(voltage_entry.get())
    if chip_select < 7 or chip_select > 10 or channel < 0 or channel > 15:
        print("Invalid chip select or channel number")
        return
    set_voltage(ser, chip_select, channel, voltage)
   #set_voltage(channel_number, current)

import csv

def set_all_voltages():
    with open('channel_voltage_data.txt', 'r') as file:
        for line in file:
            if line.strip():  # Skip empty lines
                try:
                    chip_select, channel, voltage = map(float, line.strip().split(" "))
                    if chip_select < 7 or chip_select > 10 or channel < 0 or channel > 15:
                        print("Invalid chip select or channel number")
                        continue
                    set_voltage(ser, int(chip_select), int(channel), voltage)
                      # Adjust the sleep time as needed
                except ValueError:
                    print("Error parsing line:", line)

def plot_voltages():
    all_chip_selects = []
    all_voltages = []
    with open('current.csv', 'r') as file:
        for line in file:
            if line.strip():  # Skip empty lines
                try:
                    channel, voltage = map(float, line.strip().split(" "))
                    all_chip_selects.append((chip_select - 7) * 16 + channel)
                    all_voltages.append(voltage)
                except ValueError:
                    print("Error parsing line:", line)

                    pass
                   

    plt.bar(all_chip_selects, all_voltages)
    plt.xlabel('Channels')
    plt.ylabel('Voltage')
    plt.title('Voltages Set for All Channels')
    plt.show()

#def map_coil():
    
    

def open_file_dialog():
    file_path = filedialog.askopenfilename(initialdir="/", title="Select Voltage Values File", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if file_path:
        file_path_entry.delete(0, tk.END)
        file_path_entry.insert(0, file_path)

from functools import partial
def cycle_coil():
    global w,zfield
    w=tk.Tk()
    w.title("Cycle coil")
    c=[]
    for i in range(50):
        c.append(tk.Button(w, text="%d"%i, command=partial(do_coil,i)))
        c[i].grid(row=int(i/9), column=i%9, padx=5, pady=5)
    close=tk.Button(w,text="Close",command=w.destroy)
    close.grid(row=5, column=8, padx=5, pady=5)
    zfield=tk.Label(w,text="zfield")
    zfield.grid(row=6,column=0,columnspan=8)
    
def plot_voltages():
    all_chip_selects = []
    all_voltages = []
    with open('current.csv', 'r') as file:
        for line in file:
            if line.strip():  # Skip empty lines
                try:
                    channel, voltage = map(float, line.strip().split(" "))
                    all_chip_selects.append((chip_select - 7) * 16 + channel)
                    all_voltages.append(voltage)
                except ValueError:
                    pass
                    print("Error parsing line:", line)

    plt.bar(all_chip_selects, all_voltages)
    plt.xlabel('Channels')
    plt.ylabel('Voltage')
    plt.title('Voltages Set for All Channels')
    plt.show()

#def map_coil():
    
    

def open_file_dialog():
    file_path = filedialog.askopenfilename(initialdir="/", title="Select Voltage Values File", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if file_path:
        file_path_entry.delete(0, tk.END)
        file_path_entry.insert(0, file_path)

from functools import partial
def cycle_coil():
    global w,zfield
    w=tk.Tk()
    w.title("Cycle coil")
    c=[]
    for i in range(50):
        c.append(tk.Button(w, text="%d"%i, command=partial(do_coil,i)))
        c[i].grid(row=int(i/9), column=i%9, padx=5, pady=5)
    close=tk.Button(w,text="Close",command=w.destroy)
    close.grid(row=5, column=8, padx=5, pady=5)
    zfield=tk.Label(w,text="zfield")
    zfield.grid(row=6,column=0,columnspan=8)


from labjack import ljm

# open a connection to the labjack and set the ranges for measurement

# LabJack T7 Pro connection settings
handle = ljm.openS("T7", "ANY", "ANY")  # Change if needed

# SCU channel configuration
scu_channels = [0, 1, 2]  # Change to the appropriate SCU channels for X, Y, and Z axes

# Configure SCU channels as analog inputs
for channel in scu_channels:
    ljm.eWriteName(handle, "AIN%s_RANGE" % channel, 10.0)  # Sets the range to +/- 10V

import signal

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    ljm.close(handle)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

file1=open("coils.txt","w")


def do_coil(i):

    #for j in range(4):
    set_coil(i,10)
    time.sleep(0.25)
    voltages_on=[ljm.eReadName(handle, "AIN%s" % channel) for channel in scu_channels]
    nT_on=[voltages_on[i]*100/10*1000 for i in range(len(voltages_on))]
    time.sleep(0.25)
    set_coil(i,-10)
    time.sleep(0.25)
    voltages_off = [ljm.eReadName(handle, "AIN%s" % channel) for channel in scu_channels]
    nT_off=[voltages_off[i]*100/10*1000 for i in range(len(voltages_on))]
    time.sleep(0.25)

    voltages_delta=[voltages_on[i]-voltages_off[i] for i in range(len(voltages_on))]
    nT_delta=[nT_on[i]-nT_off[i] for i in range(len(voltages_on))]

    print('Field in nT',nT_delta)
    zfield.config(text="%f nT"%(nT_delta[2]))
    set_coil(i,0)
    file1.write("%d %f\n"%(i,nT_delta[2]))


def set_coil(i,voltage):
    if ((i>=0)&(i<=15)):
        cs=10
        ch=i
    elif ((i>=16)&(i<=31)):
        cs=9
        ch=i-16
    elif ((i>=32)&(i<=47)):
        cs=8
        ch=i-32
    elif ((i>=48)&(i<=49)):
        cs=7
        ch=i-48
    print("Coil %d is cs %d and ch %d and will be set to %f"%(i,cs,ch,voltage))
    set_voltage(ser,cs,ch,voltage*coil_sign[i])


    
# Create the GUI
root = tk.Tk()
root.title("Current Control GUI")

# Serial port connection
ser=serial.Serial('/dev/ttyACM0', 9600, timeout=3)
time.sleep(2)  # wait for the serial connection to initialize

# Entry widgets
chip_select_label = tk.Label(root, text="Chip Select (7-10):")
chip_select_label.grid(row=0, column=0, padx=5, pady=5)
chip_select_entry = tk.Entry(root)
chip_select_entry.grid(row=0, column=1, padx=5, pady=5)

channel_label = tk.Label(root, text="Channel (0-15):")
channel_label.grid(row=1, column=0, padx=5, pady=5)
channel_entry = tk.Entry(root)
channel_entry.grid(row=1, column=1, padx=5, pady=5)

voltage_label = tk.Label(root, text="Voltage:")
voltage_label.grid(row=2, column=0, padx=5, pady=5)
voltage_entry = tk.Entry(root)
voltage_entry.grid(row=2, column=1, padx=5, pady=5)

# Buttons
i=4
set_individual_button = tk.Button(root, text="Set Individual Voltage", command=set_individual_voltage)
set_individual_button.grid(row=i, column=0, columnspan=2, padx=5, pady=5)

i+=1
cycle_coil_button = tk.Button(root, text="Cycle coil", command=cycle_coil)
cycle_coil_button.grid(row=i, column=0, columnspan=2, padx=5, pady=5)

i+=1
set_all_button = tk.Button(root, text="Set All Voltages", command=set_all_voltages)
set_all_button.grid(row=i, column=0, columnspan=2, padx=5, pady=5)

i+=1
zero_all_button = tk.Button(root, text="Zero All Voltages", command=zero_all_voltages)
zero_all_button.grid(row=i, column=0, columnspan=2, padx=5, pady=5)

i+=1
mux_all_button = tk.Button(root, text="MUX All Voltages", command=mux_all_voltages)
mux_all_button.grid(row=i, column=0, columnspan=2, padx=5, pady=5)

i+=1
plot_button = tk.Button(root, text="Plot Voltages", command=plot_voltages)
plot_button.grid(row=i, column=0, columnspan=2, padx=5, pady=5)

i+=1
plot_button = tk.Button(root, text="map coils", command=plot_voltages)
plot_button.grid(row=i, column=0, columnspan=2, padx=5, pady=5)


root.mainloop()
ljm.close(handle)
file1.close()
