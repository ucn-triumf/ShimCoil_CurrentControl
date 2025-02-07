#!/usr/bin/python3
# routines to run arduino current controller

import serial
import re
from datetime import datetime

# TODO: this class needs testing, especially for readback values

class ArduinoController:
    """Arduino Current Controller. Opens a connection to the arduino to set currents on the coils

    Args:
        device (str): name of the device to connect to
        baudrate (int): 9600|115200
        quiet (bool): if true, don't print message to stdout
    """

    def __init__(self, device, baudrate=115200, quiet=True):

        self.ser = serial.Serial(device, baudrate)
        self.quiet = quiet

        # do a test read and print to stdout
        first_read=self.readuntil("voltage>\r\n")
        if not self.quiet:
            print(first_read)

    def _set(self, command, read_until='.', do_print=False):
        """Base function for sending commands

        Args:
            command (str): of the format <command>. See commands listed [here](https://github.com/ucn-triumf/ShimCoil_SerialArduino)
            read_until (str): end of readback
            doprint (bool): if true print readback to stdout
        """
        # send command
        self.ser.write(f'{command}'.encode())

        # readback message from arduino and print to stdout
        readback = self.readuntil(f"{read_until}\r\n")
        if do_print:
            print(f'{datetime.now()}: {readback}', flush=True)

        return readback

    def on(self):
        """Turns on all currents to the values stored in volatile memory."""
        self._set('<ONA>', do_print=not self.quiet)

    def off(self):
        """Turns on all currents to zero, but does not delete the values stored in volatile memory."""
        self._set('<OFA>', do_print=not self.quiet)

    def neg(self):
        """Turns on all currents to the negative of the values stored in volatile memory."""
        self._set('<ONN>', do_print=not self.quiet)

    def print(self):
        """Prints all the voltages, currents, and calibration constants in volatile memory."""
        self._set(f'<PRI>', do_print=True)

    def readuntil(self, stopchar):
        """Read output from arduino until stop string is found

        Args:
            stopchar (str): stopping condition

        Returns:
            str: output message read from arduino
        """

        outputCharacters=""
        while True:
            ch = self.ser.read().decode()

            # no message: stop
            if len(ch) == 0:
                break

            # add characters to string
            else:
                outputCharacters += ch

            # check for end condition
            if outputCharacters[-len(stopchar):] == stopchar:
                break

        return outputCharacters

    def read_eeprom(self):
        """Reads all voltages and calibration constants from EEPROM into volatile memory."""
        self._set(f'<REA>', do_print=not self.quiet)

    def reset(self):
        """Resets all voltages to zero, all calibration constants to default, and writes them all to the EEPROM. Obviously this means that everything that was in the EEPROM is lost."""
        self._set(f'<RES>', do_print=not self.quiet)

    def set_current(self, i, current):
        """Set a channel to a current

        Args:
            i (int): index of channel to set, index defined in arduino code
            current (float): amps
        """

        readback = self.set(f'<STC {i} {current}>\n', 'A')

        if not self.quiet:
            m=re.search("Current (\d+) set to ([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?) A", readback)
            i_readback=int(m.group(1))
            current_readback=float(m.group(2))
            print(f"Arduino confirms current for index {i_readback} is {current_readback}")

    def set_mux(self, cs, ch):
        """Sets the MUX on CSbar cs to ch. The MUX is an output pin to readback the voltage set by the current supply.

        Args:
            cs (int): chip select bar [1, 4]
            ch (int): channel number on that chip select [1, 8]
        """
        readback = self._set(f'<MUX {cs} {ch}>\n', do_print=not self.quiet)

    def set_offset(self, i, current):
        """Sets offset in volatile memory for the set_current function  (convert between voltage and current).

        Args:
            i (int): channel index [0, 64[
            current (float): amps

        Notes:
            current = slope*V+offset
        """
        readback = self.set(f'<SOF {i} {current}>\n', 'A')
        if not self.quiet:
            print(readback)

    def set_slope(self, i, amps_per_volt):
        """Sets slope in volatile memory for the set_current function (convert between voltage and current).

        Args:
            i (int): channel index [0, 64[
            current (float): amps

        Notes:
            current = slope*V+offset
        """
        readback = self.set(f'<SSL {i} {amps_per_volt}>\n', 'A/V')
        if not self.quiet:
            print(readback)

    def set_temp_voltage(self, i, voltage):
        """Set a channel to a current and immediately turn on only that channel. Does not update voltage in volatile memory

        Args:
            i (int): index of channel to set, index defined in arduino code
            voltage (float): volts
        """
        readback = self._set(f'<SVN {i} {voltage}>\n', 'V')

        if not self.quiet:
            m = re.search("voltage (\d+) to ([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?) V", readback)
            i_readback = int(m.group(1))
            voltage_readback = float(m.group(2))
            print(f"Arduino confirms voltage for index {i_readback} is {voltage_readback}")

    def set_voltage(self, i, voltage):
        """Set a channel to a voltage in volatile memory.

        Args:
            i (int): index of channel to set, index defined in arduino code
            voltage (float): volts
        """
        # set
        readback = self._set(f'<STV {i} {voltage}>\n', 'V')

        # print readback
        if not self.quiet:
            m = re.search("Voltage (\d+) set to ([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?) V", readback)
            i_readback=int(m.group(1))
            voltage_readback=float(m.group(2))
            print(f"Arduino confirms voltage for index {i_readback} is {voltage_readback}")

    def setv(self, cs, ch, voltage):
        """Set voltage based on hardware indexing.

        Args:
            cs (int): chip select bar [1, 4]
            ch (int): channel number on that chip select [1, 8]
            voltage (float): volts
        """
        readback = self._set(f'<SET {cs} {ch} {voltage}>\n', 'V')

        if not self.quiet:
            m = re.search("Setting CSbar (\d+) channel (\d+) to ([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?) V", readback)
            cs_readback = int(m.group(1))
            ch_readback = int(m.group(2))
            voltage_readback = float(m.group(3))
            print(f"Arduino confirms voltage for CSbar {cs_readback} channel {ch_readback} is {voltage_readback}")

    def write_eeprom(self):
        """Writes all voltages and calibration constants from volatile memory to EEPROM. The values stored to EEPROM will automatically be read into volatile memory on next reboot or by connection made to arduino by serial port."""
        self._set(f'<WRI>', do_print=not self.quiet)

    def zero(self):
        """Sets all 64 voltages to zero."""
        readback = self._set(f'<ZERO>\n', 'Done zeroing.')

        if not self.quiet:
            if 'Done zeroing.' in readback:
                print("All voltages set to zero")
            else:
                print("Failed to set all voltages to zero")


