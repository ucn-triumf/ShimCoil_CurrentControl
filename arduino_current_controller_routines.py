#!/usr/bin/python3
# routines to run arduino current controller

import serial
import re


class acc:
    def __init__(self):
        # Open a connection to the Arduino, so that we can set
        # currents on the coils.
        self.ser=serial.Serial('/dev/ttyACM0',115200)
        first_read=self.CheckReadUntil("voltage>\r\n")
        print(first_read)

    def CheckReadUntil(self,readUntil):
        outputCharacters=""
        while True:
            ch=self.ser.read().decode()
            if len(ch)==0:
                break
            outputCharacters+=ch
            if outputCharacters[-len(readUntil):]==readUntil:
                break
            outputLines=''.join(outputCharacters)
        return outputLines

    def set_voltage(self,i,voltage):
        self.ser.write(f'<STV {i} {voltage}>\n'.encode())
        line=self.CheckReadUntil("V\r\n")
        m=re.search("Voltage (\d+) set to ([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?) V",line)
        i_readback=int(m.group(1))
        voltage_readback=float(m.group(2))
        print(f"Arduino confirms voltage for i {i_readback} is {voltage_readback}")

    def set_current(self,i,current):
        self.ser.write(f'<STC {i} {current}>\n'.encode())
        line=self.CheckReadUntil("A\r\n")
        m=re.search("Current (\d+) set to ([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?) A",line)
        i_readback=int(m.group(1))
        current_readback=float(m.group(2))
        print(f"Arduino confirms current for i {i_readback} is {current_readback}")

    def write_eeprom(self):
        self.ser.write(f'<WRI>'.encode())
        line=self.CheckReadUntil(".\r\n")
        print(line)

    def turn_on(self):
        self.ser.write(f'<ONA>'.encode())
        line=self.CheckReadUntil(".\r\n")
        print(line)

    def turn_off(self):
        self.ser.write(f'<OFA>'.encode())
        line=self.CheckReadUntil(".\r\n")
        print(line)

    def turn_neg(self):
        self.ser.write(f'<ONN>'.encode())
        line=self.CheckReadUntil(".\r\n")
        print(line)

    def set_voltage_now(self,i,voltage):
        self.ser.write(f'<SVN {i} {voltage}>\n'.encode())
        line=self.CheckReadUntil("V\r\n")
        m=re.search("voltage (\d+) to ([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?) V",line)
        i_readback=int(m.group(1))
        voltage_readback=float(m.group(2))
        print(f"Arduino confirms voltage for i {i_readback} is {voltage_readback}")

    def set_voltage_now_cs_ch(self,cs,ch,voltage):
        self.ser.write(f'<SET {cs} {ch} {voltage}>\n'.encode())
        line=self.CheckReadUntil("V\r\n")
        m=re.search("Setting CSbar (\d+) channel (\d+) to ([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?) V",line)
        cs_readback=int(m.group(1))
        ch_readback=int(m.group(2))
        voltage_readback=float(m.group(3))
        print(f"Arduino confirms voltage for CSbar {cs_readback} channel {ch_readback} is {voltage_readback}")


    def zero_all_voltages(self):
        self.ser.write(f'<ZERO>\n'.encode())
        line=self.CheckReadUntil(ser, "Done zeroing.\r\n")
        print(line)
        if 'Done zeroing.' in line:
            print("All voltages set to zero")
        else:
            print("Failed to set all voltages to zero")


