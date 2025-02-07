# Shim coil current controller
# Derek Fujimoto
# Feb 2025

from ArduinoController import ArduinoControllerCS
import pandas as pd
import numpy as np
from datetime import datetime

class ShimController(object):
    """This class provides high-level control for shim coils, set currents directly.
    It expects a csv file 'calibration.csv' with columns:

    coil_id, cs, ch, slope, offset

    Where cs and ch are the chip select and channel on that chip respectively.

    Args:
        device (str): connect to a device at this location
        debug (bool): if true, print debugging statements

    Attributes:
        arduino (ArduinoControllerCS): talk to arduino
        calib (pd.DataFrame): calibration constants and channel mapping
        debug (bool): if true print debug statements
        setpoints (pd.DataFrame): set currents and voltages
    """

    # file for calibration constants
    FILE_CALIBRATION = 'calibration.csv'

    # file for saving setpoints
    FILE_SETPOINTS = 'setpoints.csv'

    # number of shim coils
    NLOOPS = 64

    def __init__(self, device, debug=False):

        self.debug = debug

        # get calibration file
        self.calib = pd.read_csv(self.FILE_CALIBRATION, comment='#', index_col=0)

        # connect to device
        self.arduino = ArduinoControllerCS(device, quiet=not debug)

        # setup current settings dataframe
        self.setpoints = pd.DataFrame()

    def _update_setpoints(self, coil, current, voltage):
        # update the dataframe with new values
        self.setpoints.loc[coil, 'current'] = current
        self.setpoints.loc[coil, 'voltage'] = voltage

    def set_all_setpoints(self):
        """Set all currents to their respective setpoints"""
        for coil in self.setpoints.index:
            cal = self.calib.loc[coil]

            # set voltage
            self.arduino.setv(cal.cs, cal.ch, self.setpoints.loc[coil, 'voltage'])

            if self.debug:
                print(f'Set coil {coil} to {self.setpoints.loc[coil, "voltage"]}V')

    def set_current(self, coil, amps):
        """Set the current in a coil by calculating the needed voltage

        Args:
            coil: id of the coil
            amps: current in amps
        """

        # get calibration constants for this coil
        cal = self.calib.loc[coil]

        # get the voltage we want to set
        voltage = cal.slope*amps + cal.offset

        if self.debug:
            print(f'Calculated {voltage}V needed for coil {coil} to get {amps}A')

        # set and save
        self.arduino.setv(cal.cs, cal.ch, voltage)
        self._update_setpoints(coil, voltage=voltage, current=amps)

    def set_mux(self, coil):
        """Sets the MUX on circuit select bar to the channel corresponding to the coil id. The MUX is an output pin to readback the voltage set by the current supply.

        Args:
            coil: coil id
        """
        # get calibration constants for this coil
        cal = self.calib.loc[coil]

        # set the mux
        self.arduino.set_mux(cal.cs, cal.ch)

    def set_voltage(self, coil, volts):
        """Directly set the voltage

        Args:
            coil: id of the coil
            volts: voltage in volts
        """

        # get calibration constants for this coil
        cal = self.calib.loc[coil]

        # set voltage
        self.arduino.setv(cal.cs, cal.ch, volts)

        # calculate the corresponding current
        current = (volts-cal.offset)/cal.slope
        self._update_setpoints(coil, voltage=volts, current=current)

    def read_setpoints(self, filename=None):
        """Read setpoints file so as to load the last values set

        Args:
            filename (str): file path, if none use default self.FILE_SETPOINTS
        """

        # default filename
        if filename is None:
            filename = self.FILE_SETPOINTS

        # read
        self.setpoints = pd.read_csv(filename, comment='#', index_col=0)

    def write_setpoints(self, filename=None):
        """Write setpoints file so as to save the last values set

        Args:
            filename (str): file path, if none use default self.FILE_SETPOINTS
        """

        # default filename
        if filename is None:
            filename = self.FILE_SETPOINTS

        # get the comments from the old file
        with open(filename, 'r') as fid:
            lines = []
            for line in fid:
                if line.startswith('#') or line.strip() == '':
                    lines.append(line)
                else:
                    break

        # update the datetime
        lines[-1] = str(datetime.now())

        # write the new file
        with open(filename, 'w') as fid:
            fid.write('\n'.join(lines))
            fid.write('\n')

        self.setpoints.to_csv(filename, mode='a')

    def zero_current(self):
        """Set coils to zero current using calibrated offsets"""
        for i in self.calib.index:
            self.set_current(i, 0)

    def zero_voltage(self):
        """Set all coils to zero voltage"""

        self.arduino.zero()

        # update all setpoints
        self.setpoints.voltage = 0
        self.setpoints.current = -self.calib.offset/self.calib.slope