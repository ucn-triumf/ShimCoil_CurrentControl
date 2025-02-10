# Shimcontroller

[Shimcoil Index](./README.md#shimcoil-index) / Shimcontroller

> Auto-generated documentation for [ShimController](../src/ShimCoil/ShimController.py) module.

#### Attributes

- `data_path` - path to data files: os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'data')


- [Shimcontroller](#shimcontroller)
  - [ShimController](#shimcontroller)
    - [ShimController.disconnect](#ShimControllerdisconnect)
    - [ShimController.read_setpoints](#ShimControllerread_setpoints)
    - [ShimController.set_all_setpoints](#ShimControllerset_all_setpoints)
    - [ShimController.set_current](#ShimControllerset_current)
    - [ShimController.set_mux](#ShimControllerset_mux)
    - [ShimController.set_voltage](#ShimControllerset_voltage)
    - [ShimController.write_setpoints](#ShimControllerwrite_setpoints)
    - [ShimController.zero_current](#ShimControllerzero_current)
    - [ShimController.zero_voltage](#ShimControllerzero_voltage)

## ShimController

[Show source in ShimController.py:14](../src/ShimCoil/ShimController.py#L14)

#### Attributes

- `FILE_CALIBRATION` - file for calibration constants: os.path.join(data_path, 'calibration.csv')

- `FILE_SETPOINTS` - file for saving setpoints: 'setpoints.csv'

- `NLOOPS` - number of shim coils: 64


This class provides high-level control for shim coils, set currents directly.
It expects a csv file 'calibration.csv' with columns:

coil_id, cs, ch, slope, offset

Where cs and ch are the chip select and channel on that chip respectively.

#### Arguments

- `device` *str* - connect to a device at this location
- `zeroed` *bool* - if true, start and don't set setpoints, otherwise set according to last set values'
- `debug` *bool* - if true, print debugging statements

#### Attributes

- `arduino` *ArduinoControllerCS* - talk to arduino
- `calib` *pd.DataFrame* - calibration constants and channel mapping
- `debug` *bool* - if true print debug statements
- `setpoints` *pd.DataFrame* - set currents and voltages

#### Notes

this object writes to the file self.FILE_SETPOINTS every time a value is sent to the arduino. This ensures a record of the last set of values. It also allows the object to restore the last set of points. We can also save these values to a user-defined file and load that.

#### Signature

```python
class ShimController(object):
    def __init__(self, device, zeroed=True, debug=False): ...
```

### ShimController.disconnect

[Show source in ShimController.py:81](../src/ShimCoil/ShimController.py#L81)

Close the serial connection to the arduino

#### Signature

```python
def disconnect(self): ...
```

### ShimController.read_setpoints

[Show source in ShimController.py:147](../src/ShimCoil/ShimController.py#L147)

Read setpoints file so as to load the last values set, write this to the arduino.

#### Notes

Expect columns "coil", "voltage", and "current"
Only one of "voltage" or "current" is needed.
Column "coil" must be the leftmost column.

#### Arguments

- `filename` *str* - file path, if none use default self.FILE_SETPOINTS
- `setall` *bool* - if true, write the values to the arduino

#### Signature

```python
def read_setpoints(self, filename=None, setall=False): ...
```

### ShimController.set_all_setpoints

[Show source in ShimController.py:85](../src/ShimCoil/ShimController.py#L85)

Set all currents to their respective setpoints

#### Signature

```python
def set_all_setpoints(self): ...
```

### ShimController.set_current

[Show source in ShimController.py:96](../src/ShimCoil/ShimController.py#L96)

Set the current in a coil by calculating the needed voltage

#### Arguments

- `coil` - id of the coil
- `amps` - current in amps

#### Signature

```python
def set_current(self, coil, amps): ...
```

### ShimController.set_mux

[Show source in ShimController.py:117](../src/ShimCoil/ShimController.py#L117)

Sets the MUX on circuit select bar to the channel corresponding to the coil id. The MUX is an output pin to readback the voltage set by the current supply.

#### Arguments

- `coil` - coil id

#### Signature

```python
def set_mux(self, coil): ...
```

### ShimController.set_voltage

[Show source in ShimController.py:129](../src/ShimCoil/ShimController.py#L129)

Directly set the voltage

#### Arguments

- `coil` - id of the coil
- `volts` - voltage in volts

#### Signature

```python
def set_voltage(self, coil, volts): ...
```

### ShimController.write_setpoints

[Show source in ShimController.py:183](../src/ShimCoil/ShimController.py#L183)

Write setpoints file so as to save the last values set

#### Arguments

- `filename` *str* - file path, if none use default self.FILE_SETPOINTS

#### Signature

```python
def write_setpoints(self, filename=None): ...
```

### ShimController.zero_current

[Show source in ShimController.py:212](../src/ShimCoil/ShimController.py#L212)

Set coils to zero current using calibrated offsets

#### Signature

```python
def zero_current(self): ...
```

### ShimController.zero_voltage

[Show source in ShimController.py:217](../src/ShimCoil/ShimController.py#L217)

Set all coils to zero voltage

#### Signature

```python
def zero_voltage(self): ...
```