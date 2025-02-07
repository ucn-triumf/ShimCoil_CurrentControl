# Arduinocontroller64

[Shimcoil Index](./README.md#shimcoil-index) / Arduinocontroller64

> Auto-generated documentation for [ArduinoController64](../../../ArduinoController64.py) module.

- [Arduinocontroller64](#arduinocontroller64)
  - [ArduinoController64](#arduinocontroller64)
    - [ArduinoController64.neg](#arduinocontroller64()neg)
    - [ArduinoController64.off](#arduinocontroller64()off)
    - [ArduinoController64.on](#arduinocontroller64()on)
    - [ArduinoController64.print](#arduinocontroller64()print)
    - [ArduinoController64.read_eeprom](#arduinocontroller64()read_eeprom)
    - [ArduinoController64.reset_eeprom](#arduinocontroller64()reset_eeprom)
    - [ArduinoController64.set_current](#arduinocontroller64()set_current)
    - [ArduinoController64.set_offset](#arduinocontroller64()set_offset)
    - [ArduinoController64.set_slope](#arduinocontroller64()set_slope)
    - [ArduinoController64.set_temp_voltage](#arduinocontroller64()set_temp_voltage)
    - [ArduinoController64.set_voltage](#arduinocontroller64()set_voltage)
    - [ArduinoController64.write_eeprom](#arduinocontroller64()write_eeprom)

## ArduinoController64

[Show source in ArduinoController64.py:9](../../../ArduinoController64.py#L9)

Arduino Current Controller. Opens a connection to the arduino to set
currents on the coils.

This version provides access to the eeprom onboard storage as well as a
0 - 64 indexing for channel access, in addition to onboard volatile memeory.
Channel mapping can be found in the [arduino code](https://github.com/ucn-triumf/ShimCoil_SerialArduino)

#### Arguments

- `device` *str* - name of the device to connect to
- `baudrate` *int* - 9600|115200
- `quiet` *bool* - if true, don't print message to stdout

#### Signature

```python
class ArduinoController64(ArduinoControllerCS): ...
```

#### See also

- [ArduinoControllerCS](./ArduinoControllerCS.md#arduinocontrollercs)

### ArduinoController64.neg

[Show source in ArduinoController64.py:23](../../../ArduinoController64.py#L23)

Turns on all currents to the negative of the values stored in volatile memory.

#### Signature

```python
def neg(self): ...
```

### ArduinoController64.off

[Show source in ArduinoController64.py:27](../../../ArduinoController64.py#L27)

Turns on all currents to zero, but does not delete the values stored in volatile memory.

#### Signature

```python
def off(self): ...
```

### ArduinoController64.on

[Show source in ArduinoController64.py:31](../../../ArduinoController64.py#L31)

Turns on all currents to the values stored in volatile memory.

#### Signature

```python
def on(self): ...
```

### ArduinoController64.print

[Show source in ArduinoController64.py:35](../../../ArduinoController64.py#L35)

Prints all the voltages, currents, and calibration constants in volatile memory.

#### Signature

```python
def print(self): ...
```

### ArduinoController64.read_eeprom

[Show source in ArduinoController64.py:39](../../../ArduinoController64.py#L39)

Reads all voltages and calibration constants from EEPROM into volatile memory.

#### Signature

```python
def read_eeprom(self): ...
```

### ArduinoController64.reset_eeprom

[Show source in ArduinoController64.py:43](../../../ArduinoController64.py#L43)

Resets all voltages to zero, all calibration constants to default, and writes them all to the EEPROM. Obviously this means that everything that was in the EEPROM is lost.

#### Signature

```python
def reset_eeprom(self): ...
```

### ArduinoController64.set_current

[Show source in ArduinoController64.py:47](../../../ArduinoController64.py#L47)

Set a channel to a current

#### Arguments

- `i` *int* - index of channel to set, index defined in arduino code
- `current` *float* - amps

#### Signature

```python
def set_current(self, i, current): ...
```

### ArduinoController64.set_offset

[Show source in ArduinoController64.py:63](../../../ArduinoController64.py#L63)

Sets offset in volatile memory for the set_current function  (convert between voltage and current).

#### Arguments

- `i` *int* - channel index [0, 64[
- `current` *float* - amps

#### Notes

current = slope*V+offset

#### Signature

```python
def set_offset(self, i, current): ...
```

### ArduinoController64.set_slope

[Show source in ArduinoController64.py:77](../../../ArduinoController64.py#L77)

Sets slope in volatile memory for the set_current function (convert between voltage and current).

#### Arguments

- `i` *int* - channel index [0, 64[
- `current` *float* - amps

#### Notes

current = slope*V+offset

#### Signature

```python
def set_slope(self, i, amps_per_volt): ...
```

### ArduinoController64.set_temp_voltage

[Show source in ArduinoController64.py:91](../../../ArduinoController64.py#L91)

Set a channel to a current and immediately turn on only that channel. Does not update voltage in volatile memory

#### Arguments

- `i` *int* - index of channel to set, index defined in arduino code
- `voltage` *float* - volts

#### Signature

```python
def set_temp_voltage(self, i, voltage): ...
```

### ArduinoController64.set_voltage

[Show source in ArduinoController64.py:106](../../../ArduinoController64.py#L106)

Set a channel to a voltage in volatile memory.

#### Arguments

- `i` *int* - index of channel to set, index defined in arduino code
- `voltage` *float* - volts

#### Signature

```python
def set_voltage(self, i, voltage): ...
```

### ArduinoController64.write_eeprom

[Show source in ArduinoController64.py:123](../../../ArduinoController64.py#L123)

Writes all voltages and calibration constants from volatile memory to EEPROM. The values stored to EEPROM will automatically be read into volatile memory on next reboot or by connection made to arduino by serial port.

#### Signature

```python
def write_eeprom(self): ...
```