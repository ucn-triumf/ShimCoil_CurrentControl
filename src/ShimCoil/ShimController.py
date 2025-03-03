# Shim coil current controller
# Derek Fujimoto
# Feb 2025

from .ArduinoControllerCS import ArduinoControllerCS
import pandas as pd
import numpy as np
from datetime import datetime
import os, shutil

# path to data files
data_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')

class ShimController(object):
    """This class provides high-level control for shim coils, set currents directly.
    It expects a csv file 'calibration.csv' with columns:

    coil_id, cs, ch, slope_i, offset_i, slope_b offset_b

    Where cs and ch are the chip select and channel on that chip respectively.

    Args:
        device (str): connect to a device at this location
        zeroed (bool): if true, start and don't set setpoints, otherwise set according to last set values'
        debug (bool): if true, print debugging statements

    Attributes:
        arduino (ArduinoControllerCS): talk to arduino
        calib (pd.DataFrame): calibration constants and channel mapping
        debug (bool): if true print debug statements
        setpoints (pd.DataFrame): set currents and voltages

    Notes:
        this object writes to the file self.FILE_SETPOINTS every time a value is sent to the arduino. This ensures a record of the last set of values. It also allows the object to restore the last set of points. We can also save these values to a user-defined file and load that.
    """

    # file for calibration constants
    FILE_CALIBRATION = os.path.join(data_path, 'calibration.csv')

    # file for saving setpoints
    FILE_SETPOINTS = 'setpoints.csv'

    # number of shim coils
    NLOOPS = 64

    def __init__(self, device, zeroed=True, debug=False):

        self.debug = debug

        # get calibration file
        self.calib = pd.read_csv(self.FILE_CALIBRATION, comment='#', index_col=0)

        # setup current setpoints dataframe
        if not os.path.isfile(self.FILE_SETPOINTS):
            shutil.copyfile(os.path.join(data_path, self.FILE_SETPOINTS), self.FILE_SETPOINTS)
        self.read_setpoints(setall=False)

        # connect to device
        self.arduino = ArduinoControllerCS(device, quiet=not debug)

        # rezero
        if zeroed:
            self.zero_voltage()

        # write values to arduino
        self.set_all_setpoints()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

    def _update_setpoints(self, coil, current=None, voltage=None, field=None):
        # update the dataframe with new values
        # use only one of the current, voltage, or field to set the values

        # get calibration constants for this coil
        cal = self.calib.loc[coil]

        # calculate missing paramters
        if current is not None:
            assert voltage is not None or field is not None, 'Only one of current, voltage, field can be not None'
            voltage = (current-cal.offset_i) / cal.slope_i
            field = voltage*cal.slope_b + cal.offset_b
            setby = 'current'
        elif voltage is not None:
            assert current is not None or field is not None, 'Only one of current, voltage, field can be not None'
            current = voltage*cal.slope_i + cal.offset_i
            field = voltage*cal.slope_b + cal.offset_b
            setby = 'voltage'
        elif field is not None:
            assert voltage is not None or current is not None, 'Only one of current, voltage, field can be not None'
            voltage = (current-cal.offset_b) / cal.slope_b
            current = voltage*cal.slope_i + cal.offset_i
            setby = 'field'
        else:
            raise RuntimeError('Missing field, current, or voltage input')

        # debug
        if self.debug:
            print(f'Setting coil {coil} ({cal.cs, cal.ch}) to {self.setpoints.loc[coil, "voltage"]}V ({current}A, {field}nT, set by {setby})')

        # set the voltage
        self.arduino.setv(cal.cs, cal.ch, voltage)

        # save the inputs
        self.setpoints.loc[coil, 'current'] = current
        self.setpoints.loc[coil, 'voltage'] = voltage
        self.setpoints.loc[coil, 'field'] = field
        self.setpoints.loc[coil, 'setby'] = setby
        self.write_setpoints()

    def close(self):
        """Alias for disconnect"""
        return self.disconnect()

    def disconnect(self):
        """Close the serial connection to the arduino"""
        self.arduino.disconnect()

    def set_all_setpoints(self):
        """Set all currents to their respective setpoints"""
        for coil in self.setpoints.index:
            cal = self.calib.loc[coil]

            if self.debug:
                print(f'Setting coil {coil} ({cal.cs, cal.ch}) to {self.setpoints.loc[coil, "voltage"]}V')

            # set voltage
            self.arduino.setv(cal.cs, cal.ch, self.setpoints.loc[coil, 'voltage'])

    def set_current(self, coil, amps):
        """Set the current in a coil by calculating the needed voltage

        Args:
            coil: id of the coil
            amps: current in amps
        """
        self._update_setpoints(coil, current=amps)

    def set_field(self, coil, nT):
        """Set the current in a coil by calculating the needed voltage

        Args:
            coil: id of the coil
            nT: field in nT
        """
        # set and save
        self._update_setpoints(coil, field=nT)

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
        self._update_setpoints(coil, voltage=volts)

    def read_setpoints(self, filename=None, setall=False):
        """Read setpoints file so as to load the last values set, write this to the arduino.

        Notes:
            Expect columns "coil", "voltage", and "current"
            Only one of "voltage" or "current" or "field" is needed.
            Column "coil" must be the leftmost column.
            Only supports setting setpoints from one column type (i.e. uniform setby column)

        Args:
            filename (str): file path, if none use default self.FILE_SETPOINTS
            setall (bool): if true, write the values to the arduino
        """

        # default filename
        if filename is None:
            filename = self.FILE_SETPOINTS

        # read
        setpts = pd.read_csv(filename, comment='#', index_col=0)

        # check for missing columns
        needed_cols = ['setby', 'voltage', 'current', 'field']
        missing_columns = [c for c in needed_cols if c not in setpts.columns]
        present_columns = [c for c in needed_cols if c in setpts.columns]

        # uniform setby
        setpts['setby'] = present_columns[0]

        if 'voltage' in missing_columns:

            # conversion
            if present_columns[0] == 'current':
                setpts['voltage'] = self.calib.slope_i*setpts.current + self.calib.offset_i
            elif present_columns[0] == 'field':
                setpts['voltage'] = self.calib.slope_b*setpts.field + self.calib.offset_b
            else:
                raise RuntimeError('Did not find column to calculate voltages from')

        if 'field' in missing_columns:
            setpts['field'] = (setpts.voltage - self.calib.offset_b) / self.calib.slope_b

        if 'current' in missing_columns:
            setpts['current'] = (setpts.voltage - self.calib.offset_i) / self.calib.slope_i

        # set setpoints
        self.setpoints = setpts

        if self.debug:
            print(f'Read setpoints from {filename}:\n{setpts}')

        if setall:
            self.set_all_setpoints()

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
                    lines.append(line.strip())
                else:
                    break

        # update the datetime
        lines[-1] = f'# {datetime.now()}'

        # write the new file
        with open(filename, 'w') as fid:
            fid.write('\n'.join(lines))
            fid.write('\n')
        self.setpoints.to_csv(filename, mode='a')

    def zero(self, mode='voltage'):
        """Set coils to zero voltage, current, or field using calibrated offsets

        Args:
            mode (str): voltage|field|current|i|b|v
        """

        # select mode
        mode = mode.lower()
        if mode in 'voltage' or mode == 'v':
            method = self.set_voltage
        elif mode in 'current' or mode == 'i':
            method = self.set_current
        elif mode in 'field' or mode == 'b':
            method = self.set_field

        # set
        for i in self.calib.index:
            method(i, 0)