# routines to run arduino current controller
# Derek Fujimoto (reinterpreted from Jeff Martin)
# Feb 2025

import serial
import re
from datetime import datetime
import time

class ArduinoControllerCS(object):
    """Arduino Current Controller. Opens a connection to the arduino to set
    currents on the coils. This version provides the simplest low-level access

    Args:
        device (str): name of the device to connect to
        baudrate (int): 9600|115200
        quiet (bool): if true, don't print message to stdout
    """

    READ_TIMEOUT = 10 # s, timeout in s until error is thrown on readback

    def __init__(self, device, baudrate=115200, quiet=True):

        self.ser = serial.Serial(device, baudrate)
        self.quiet = quiet

        # do a test read and print to stdout
        first_read = self._readuntil("voltage>\r\n")
        if not self.quiet:
            print(f'{datetime.now()}: {first_read}')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

    def _readuntil(self):
        """Read output from arduino until stop string is found

        Args:
            stopchar (str): stopping condition

        Returns:
            str: output message read from arduino
        """

        outputCharacters = ""

        time_start = time.time()

        while True:
            ch = self.ser.read().decode()

            # no message: stop
            if len(ch) == 0:
                break

            # add characters to string
            else:
                outputCharacters += ch

            # check for end condition
            if outputCharacters[-1] == '#':
                break

            # runtime timeout
            if time.time()- time_start > self.READ_TIMEOUT:
                raise RuntimeError(f'readuntil timeout! Expected endcharacter (#) not receieved from arduino. Messages until now:\n{outputCharacters}')

        return outputCharacters

    def _cmd(self, command, do_print=False):
        """Base function for sending commands

        Args:
            command (str): of the format <command>. See commands listed [here](https://github.com/ucn-triumf/ShimCoil_SerialArduino)
            read_until (str): end of readback
            doprint (bool): if true print readback to stdout
        """
        # send command
        self.ser.write(f'<{command}>\n'.encode())

        # readback message from arduino and print to stdout
        readback = self._readuntil(f"#\r\n")
        if do_print:
            print(f'{datetime.now()}: {readback[:-1]}', flush=True)

        return readback

    def disconnect(self):
        """Close the connection to the arduino"""
        self.ser.close()

    def mem_read(self):
        """read to volatile memory from onboard storage"""
        self._cmd('ERD')

    def mem_reset(self):
        """reset volatile memory to zero"""
        self._cmd('ERST')

    def mem_write(self):
        """write volatile memory to onboard storage"""
        self._cmd('EWR')

    def pwr_down(self, cs):
        """Powers down all channels on a CSbar

        Args:
            cs (int): chip select bar 10|9|8|7
        """
        self._cmd(f'PWR {cs}', do_print=not self.quiet)

    def set_mux(self, cs, ch):
        """Sets the MUX on CSbar cs to ch. The MUX is an output pin to readback the voltage set by the current supply.

        Args:
            cs (int): chip select bar 10|9|8|7
            ch (int): channel number on that chip select [0, 15]
        """
        self._cmd(f'MUX {cs} {ch}', do_print=not self.quiet)

    def setv(self, cs, ch, voltage):
        """Set voltage based on hardware indexing and turn on that channel

        Args:
            cs (int): chip select bar 10|9|8|7
            ch (int): channel number on that chip select [0, 15]
            voltage (float): volts
        """

        if abs(voltage) > 10:
            raise RuntimeError(f'Requested voltage ({voltage}V) is too high. Voltages must be less than 10V in magnitude. ')

        readback = self._cmd(f'SET {cs} {ch} {voltage}')

        if not self.quiet:
            m = re.search("Setting CSbar (\d+) channel (\d+) to ([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?) V#", readback)
            cs_readback = int(m.group(1))
            ch_readback = int(m.group(2))
            voltage_readback = float(m.group(3))
            print(f"{datetime.now()}: Arduino confirms voltage for CSbar {cs_readback} channel {ch_readback} is {voltage_readback}")

    def setv_from_mem(self, cs, ch):
        """Set a voltage from the volatile memory

        Args:
            cs (int): chip select bar 10|9|8|7
            ch (int): channel number on that chip select [0, 15]
        """
        readback = self._cmd(f'ESET {cs} {ch}')

        if not self.quiet:
            m = re.search("Setting CSbar (\d+) channel (\d+) to ([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?) V#", readback)
            cs_readback = int(m.group(1))
            ch_readback = int(m.group(2))
            voltage_readback = float(m.group(3))
            print(f"{datetime.now()}: Arduino confirms voltage for CSbar {cs_readback} channel {ch_readback} is {voltage_readback}")

    def setv_all_mem(self):
        """Set all voltages from the volatile memory saved values"""
        readback = self._cmd(f'ESTA')

        if not self.quiet:
            print(f'{readback[:-1]}')

    def setv_all_nmem(self):
        """Set all voltages to -1 * the volatile memory saved values"""
        readback = self._cmd(f'ENEG')

        if not self.quiet:
            print(f'{readback[:-1]}')

    def zero(self):
        """Sets all 64 voltages to zero, does not adjust volatile memory."""
        readback = self._cmd(f'ZERO', 'Done zeroing.')

        if not self.quiet:
            if 'Done zeroing' in readback:
                print(f"{datetime.now()}: All voltages set to zero")
            else:
                print(f"{datetime.now()}: Failed to set all voltages to zero")
