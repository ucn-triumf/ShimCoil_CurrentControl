#!/usr/bin/python3

import serial
import time
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt

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
    line = CheckReadUntil(ser, "V\r\n")
    if 'received' in line:
        print("All voltages set to zero")
    else:
        parsing = line.split(" ")
        if len(parsing) > 11:
            voltage_readback = float(parsing[11])
            print(f"Set all voltages to zero, readback: {voltage_readback}")
        else:
            print("Failed to set all voltages to zero")

def set_individual_voltage():
    chip_select = int(chip_select_entry.get())
    channel = int(channel_entry.get())
    voltage = float(voltage_entry.get())
    if chip_select < 7 or chip_select > 10 or channel < 0 or channel > 15:
        print("Invalid chip select or channel number")
        return
    set_voltage(ser, chip_select, channel, voltage)

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
    with open('channel_voltage_data.txt', 'r') as file:
        for line in file:
            if line.strip():  # Skip empty lines
                try:
                    chip_select, channel, voltage = map(float, line.strip().split(" "))
                    all_chip_selects.append((chip_select - 7) * 16 + channel)
                    all_voltages.append(voltage)
                except ValueError:
                    print("Error parsing line:", line)

    plt.bar(all_chip_selects, all_voltages)
    plt.xlabel('Channels')
    plt.ylabel('Voltage')
    plt.title('Voltages Set for All Channels')
    plt.show()

def open_file_dialog():
    file_path = filedialog.askopenfilename(initialdir="/", title="Select Voltage Values File", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if file_path:
        file_path_entry.delete(0, tk.END)
        file_path_entry.insert(0, file_path)

# Create the GUI
root = tk.Tk()
root.title("Current Control GUI")

# Serial port connection
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=3)
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
set_individual_button = tk.Button(root, text="Set Individual Voltage", command=set_individual_voltage)
set_individual_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

set_all_button = tk.Button(root, text="Set All Voltages", command=set_all_voltages)
set_all_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

zero_all_button = tk.Button(root, text="Zero All Voltages", command=zero_all_voltages)
zero_all_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

plot_button = tk.Button(root, text="Plot Voltages", command=plot_voltages)
plot_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
