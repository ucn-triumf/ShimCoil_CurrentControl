# Shimcontroller

[Shimcoil Index](./README.md#shimcoil-index) / Shimcontroller

> Auto-generated documentation for [ShimController](../src/ShimCoil/ShimController.py) module.

#### Attributes

- `data_path` - path to data files: os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')


- [Shimcontroller](#shimcontroller)
  - [ShimController](#shimcontroller)
    - [ShimController.close](#ShimControllerclose)
    - [ShimController.disconnect](#ShimControllerdisconnect)
    - [ShimController.read_setpoints](#ShimControllerread_setpoints)
    - [ShimController.set_all_setpoints](#ShimControllerset_all_setpoints)
    - [ShimController.set_current](#ShimControllerset_current)
    - [ShimController.set_field](#ShimControllerset_field)
    - [ShimController.set_mux](#ShimControllerset_mux)
    - [ShimController.set_voltage](#ShimControllerset_voltage)
    - [ShimController.write_setpoints](#ShimControllerwrite_setpoints)
    - [ShimController.zero](#ShimControllerzero)

## ShimController

[Show source in ShimController.py:14](../src/ShimCoil/ShimController.py#L14)

#### Attributes

- `FILE_CALIBRATION` - file for calibration constants: os.path.join(data_path, 'calibration.csv')

- `FILE_SETPOINTS` - file for saving setpoints: 'setpoints.csv'

- `NLOOPS` - number of shim coils: 64


This class provides high-level control for shim coils, set currents directly.
It expects a csv file 'calibration.csv' with columns:

coil_id, cs, ch, slope_i, offset_i, slope_b offset_b

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

### ShimController.close

[Show source in ShimController.py:114](../src/ShimCoil/ShimController.py#L114)

Alias for disconnect

#### Signature

```python
def close(self): ...
```

### ShimController.disconnect

[Show source in ShimController.py:118](../src/ShimCoil/ShimController.py#L118)

Close the serial connection to the arduino

#### Signature

```python
def disconnect(self): ...
```

### ShimController.read_setpoints

[Show source in ShimController.py:173](../src/ShimCoil/ShimController.py#L173)

Read setpoints file so as to load the last values set, write this to the arduino.

#### Notes

Expect columns "coil", "voltage", and "current"
Only one of "voltage" or "current" or "field" is needed.
Column "coil" must be the leftmost column.
Only supports setting setpoints from one column type (i.e. uniform setby column)

#### Arguments

- `filename` *str* - file path, if none use default self.FILE_SETPOINTS
- `setall` *bool* - if true, write the values to the arduino

#### Signature

```python
def read_setpoints(self, filename=None, setall=False): ...
```

### ShimController.set_all_setpoints

[Show source in ShimController.py:122](../src/ShimCoil/ShimController.py#L122)

Set all currents to their respective setpoints

#### Signature

```python
def set_all_setpoints(self): ...
```

### ShimController.set_current

[Show source in ShimController.py:133](../src/ShimCoil/ShimController.py#L133)

Set the current in a coil by calculating the needed voltage

#### Arguments

- `coil` - id of the coil
- `amps` - current in amps

#### Signature

```python
def set_current(self, coil, amps): ...
```

### ShimController.set_field

[Show source in ShimController.py:142](../src/ShimCoil/ShimController.py#L142)

Set the current in a coil by calculating the needed voltage

#### Arguments

- `coil` - id of the coil
- `nT` - field in nT

#### Signature

```python
def set_field(self, coil, nT): ...
```

### ShimController.set_mux

[Show source in ShimController.py:152](../src/ShimCoil/ShimController.py#L152)

Sets the MUX on circuit select bar to the channel corresponding to the coil id. The MUX is an output pin to readback the voltage set by the current supply.

#### Arguments

- `coil` - coil id

#### Signature

```python
def set_mux(self, coil): ...
```

### ShimController.set_voltage

[Show source in ShimController.py:164](../src/ShimCoil/ShimController.py#L164)

Directly set the voltage

#### Arguments

- `coil` - id of the coil
- `volts` - voltage in volts

#### Signature

```python
def set_voltage(self, coil, volts): ...
```

### ShimController.write_setpoints

[Show source in ShimController.py:227](../src/ShimCoil/ShimController.py#L227)

Write setpoints file so as to save the last values set

#### Arguments

- `filename` *str* - file path, if none use default self.FILE_SETPOINTS

#### Signature

```python
def write_setpoints(self, filename=None): ...
```

### ShimController.zero

[Show source in ShimController.py:256](../src/ShimCoil/ShimController.py#L256)

Set coils to zero voltage, current, or field using calibrated offsets

#### Arguments

- `mode` *str* - voltage|field|current|i|b|v

#### Signature

```python
def zero(self, mode="voltage"): ...
```