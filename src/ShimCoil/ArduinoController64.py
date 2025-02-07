# routines to run arduino current controller
# Derek Fujimoto (reinterpreted from Jeff Martin)
# Feb 2025

from .ArduinoControllerCS import ArduinoControllerCS
import re
from datetime import datetime

class ArduinoController64(ArduinoControllerCS):
    """Arduino Current Controller. Opens a connection to the arduino to set
    currents on the coils.

    This version provides access to the eeprom onboard storage as well as a
    0 - 64 indexing for channel access, in addition to onboard volatile memeory.
    Channel mapping can be found in the [arduino code](https://github.com/ucn-triumf/ShimCoil_SerialArduino)

    Args:
        device (str): name of the device to connect to
        baudrate (int): 9600|115200
        quiet (bool): if true, don't print message to stdout
    """

    def neg(self):
        """Turns on all currents to the negative of the values stored in volatile memory."""
        self._set('ONN', do_print=not self.quiet)

    def off(self):
        """Turns on all currents to zero, but does not delete the values stored in volatile memory."""
        self._set('OFA', do_print=not self.quiet)

    def on(self):
        """Turns on all currents to the values stored in volatile memory."""
        self._set('ONA', do_print=not self.quiet)

    def print(self):
        """Prints all the voltages, currents, and calibration constants in volatile memory."""
        self._set(f'PRI', do_print=True)

    def read_eeprom(self):
        """Reads all voltages and calibration constants from EEPROM into volatile memory."""
        self._set(f'REA', do_print=not self.quiet)

    def reset_eeprom(self):
        """Resets all voltages to zero, all calibration constants to default, and writes them all to the EEPROM. Obviously this means that everything that was in the EEPROM is lost."""
        self._set(f'RES', do_print=not self.quiet)

    def set_current(self, i, current):
        """Set a channel to a current

        Args:
            i (int): index of channel to set, index defined in arduino code
            current (float): amps
        """

        readback = self._set(f'STC {i} {current}', 'A')

        if not self.quiet:
            m=re.search("Current (\d+) set to ([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?) A", readback)
            i_readback=int(m.group(1))
            current_readback=float(m.group(2))
            print(f"{datetime.now()}: Arduino confirms current for index {i_readback} is {current_readback}")

    def set_offset(self, i, current):
        """Sets offset in volatile memory for the set_current function  (convert between voltage and current).

        Args:
            i (int): channel index [0, 64[
            current (float): amps

        Notes:
            current = slope*V+offset
        """
        readback = self._set(f'SOF {i} {current}', 'A')
        if not self.quiet:
            print(f'{datetime.now()}: Offset is {readback}')

    def set_slope(self, i, amps_per_volt):
        """Sets slope in volatile memory for the set_current function (convert between voltage and current).

        Args:
            i (int): channel index [0, 64[
            current (float): amps

        Notes:
            current = slope*V+offset
        """
        readback = self._set(f'SSL {i} {amps_per_volt}', 'A/V')
        if not self.quiet:
            print(f'{datetime.now()}: Slope is {readback}')

    def set_temp_voltage(self, i, voltage):
        """Set a channel to a current and immediately turn on only that channel. Does not update voltage in volatile memory

        Args:
            i (int): index of channel to set, index defined in arduino code
            voltage (float): volts
        """
        readback = self._set(f'SVN {i} {voltage}', 'V')

        if not self.quiet:
            m = re.search("voltage (\d+) to ([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?) V", readback)
            i_readback = int(m.group(1))
            voltage_readback = float(m.group(2))
            print(f"{datetime.now()}: Arduino confirms voltage for index {i_readback} is {voltage_readback}")

    def set_voltage(self, i, voltage):
        """Set a channel to a voltage in volatile memory.

        Args:
            i (int): index of channel to set, index defined in arduino code
            voltage (float): volts
        """
        # set
        readback = self._set(f'STV {i} {voltage}', 'V')

        # print readback
        if not self.quiet:
            m = re.search("Voltage (\d+) set to ([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?) V", readback)
            i_readback=int(m.group(1))
            voltage_readback=float(m.group(2))
            print(f"{datetime.now()}: Arduino confirms voltage for index {i_readback} is {voltage_readback}")

    def write_eeprom(self):
        """Writes all voltages and calibration constants from volatile memory to EEPROM. The values stored to EEPROM will automatically be read into volatile memory on next reboot or by connection made to arduino by serial port."""
        self._set(f'WRI', do_print=not self.quiet)
