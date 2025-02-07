# Arduinocontrollercs

[Shimcoil Index](./README.md#shimcoil-index) / Arduinocontrollercs

> Auto-generated documentation for [ArduinoControllerCS](../../../ArduinoControllerCS.py) module.

- [Arduinocontrollercs](#arduinocontrollercs)
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
  - [ArduinoControllerCS](#arduinocontrollercs)
    - [ArduinoControllerCS._readuntil](#ArduinoControllerCS_readuntil)
    - [ArduinoControllerCS._set](#ArduinoControllerCS_set)
    - [ArduinoControllerCS.disconnect](#ArduinoControllerCSdisconnect)
    - [ArduinoControllerCS.pwr_down](#ArduinoControllerCSpwr_down)
    - [ArduinoControllerCS.set_mux](#ArduinoControllerCSset_mux)
    - [ArduinoControllerCS.setv](#ArduinoControllerCSsetv)
    - [ArduinoControllerCS.zero](#ArduinoControllerCSzero)

## ArduinoController64

[Show source in ArduinoControllerCS.py:139](../../../ArduinoControllerCS.py#L139)

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

- [ArduinoControllerCS](#arduinocontrollercs)

### ArduinoController64.neg

[Show source in ArduinoControllerCS.py:153](../../../ArduinoControllerCS.py#L153)

Turns on all currents to the negative of the values stored in volatile memory.

#### Signature

```python
def neg(self): ...
```

### ArduinoController64.off

[Show source in ArduinoControllerCS.py:157](../../../ArduinoControllerCS.py#L157)

Turns on all currents to zero, but does not delete the values stored in volatile memory.

#### Signature

```python
def off(self): ...
```

### ArduinoController64.on

[Show source in ArduinoControllerCS.py:161](../../../ArduinoControllerCS.py#L161)

Turns on all currents to the values stored in volatile memory.

#### Signature

```python
def on(self): ...
```

### ArduinoController64.print

[Show source in ArduinoControllerCS.py:165](../../../ArduinoControllerCS.py#L165)

Prints all the voltages, currents, and calibration constants in volatile memory.

#### Signature

```python
def print(self): ...
```

### ArduinoController64.read_eeprom

[Show source in ArduinoControllerCS.py:169](../../../ArduinoControllerCS.py#L169)

Reads all voltages and calibration constants from EEPROM into volatile memory.

#### Signature

```python
def read_eeprom(self): ...
```

### ArduinoController64.reset_eeprom

[Show source in ArduinoControllerCS.py:173](../../../ArduinoControllerCS.py#L173)

Resets all voltages to zero, all calibration constants to default, and writes them all to the EEPROM. Obviously this means that everything that was in the EEPROM is lost.

#### Signature

```python
def reset_eeprom(self): ...
```

### ArduinoController64.set_current

[Show source in ArduinoControllerCS.py:177](../../../ArduinoControllerCS.py#L177)

Set a channel to a current

#### Arguments

- `i` *int* - index of channel to set, index defined in arduino code
- `current` *float* - amps

#### Signature

```python
def set_current(self, i, current): ...
```

### ArduinoController64.set_offset

[Show source in ArduinoControllerCS.py:193](../../../ArduinoControllerCS.py#L193)

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

[Show source in ArduinoControllerCS.py:207](../../../ArduinoControllerCS.py#L207)

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

[Show source in ArduinoControllerCS.py:221](../../../ArduinoControllerCS.py#L221)

Set a channel to a current and immediately turn on only that channel. Does not update voltage in volatile memory

#### Arguments

- `i` *int* - index of channel to set, index defined in arduino code
- `voltage` *float* - volts

#### Signature

```python
def set_temp_voltage(self, i, voltage): ...
```

### ArduinoController64.set_voltage

[Show source in ArduinoControllerCS.py:236](../../../ArduinoControllerCS.py#L236)

Set a channel to a voltage in volatile memory.

#### Arguments

- `i` *int* - index of channel to set, index defined in arduino code
- `voltage` *float* - volts

#### Signature

```python
def set_voltage(self, i, voltage): ...
```

### ArduinoController64.write_eeprom

[Show source in ArduinoControllerCS.py:253](../../../ArduinoControllerCS.py#L253)

Writes all voltages and calibration constants from volatile memory to EEPROM. The values stored to EEPROM will automatically be read into volatile memory on next reboot or by connection made to arduino by serial port.

#### Signature

```python
def write_eeprom(self): ...
```



## ArduinoControllerCS

[Show source in ArduinoControllerCS.py:10](../../../ArduinoControllerCS.py#L10)

Arduino Current Controller. Opens a connection to the arduino to set
currents on the coils. This version provides the simplest low-level access

#### Arguments

- `device` *str* - name of the device to connect to
- `baudrate` *int* - 9600|115200
- `quiet` *bool* - if true, don't print message to stdout

#### Signature

```python
class ArduinoControllerCS(object):
    def __init__(self, device, baudrate=115200, quiet=True): ...
```

### ArduinoControllerCS._readuntil

[Show source in ArduinoControllerCS.py:38](../../../ArduinoControllerCS.py#L38)

Read output from arduino until stop string is found

#### Arguments

- `stopchar` *str* - stopping condition

#### Returns

- `str` - output message read from arduino

#### Signature

```python
def _readuntil(self, stopchar): ...
```

### ArduinoControllerCS._set

[Show source in ArduinoControllerCS.py:73](../../../ArduinoControllerCS.py#L73)

Base function for sending commands

#### Arguments

- `command` *str* - of the format <command>. See commands listed [here](https://github.com/ucn-triumf/ShimCoil_SerialArduino)
- `read_until` *str* - end of readback
- `doprint` *bool* - if true print readback to stdout

#### Signature

```python
def _set(self, command, read_until=".", do_print=False): ...
```

### ArduinoControllerCS.disconnect

[Show source in ArduinoControllerCS.py:91](../../../ArduinoControllerCS.py#L91)

Close the connection to the arduino

#### Signature

```python
def disconnect(self): ...
```

### ArduinoControllerCS.pwr_down

[Show source in ArduinoControllerCS.py:95](../../../ArduinoControllerCS.py#L95)

Powers down all channels on a CSbar

#### Arguments

- `cs` *int* - chip select bar 10|9|8|7

#### Signature

```python
def pwr_down(self, cs): ...
```

### ArduinoControllerCS.set_mux

[Show source in ArduinoControllerCS.py:103](../../../ArduinoControllerCS.py#L103)

Sets the MUX on CSbar cs to ch. The MUX is an output pin to readback the voltage set by the current supply.

#### Arguments

- `cs` *int* - chip select bar 10|9|8|7
- `ch` *int* - channel number on that chip select [0, 15]

#### Signature

```python
def set_mux(self, cs, ch): ...
```

### ArduinoControllerCS.setv

[Show source in ArduinoControllerCS.py:112](../../../ArduinoControllerCS.py#L112)

Set voltage based on hardware indexing and turn on that channel. Does not adjust volatile memory.

#### Arguments

- `cs` *int* - chip select bar 10|9|8|7
- `ch` *int* - channel number on that chip select [0, 15]
- `voltage` *float* - volts

#### Signature

```python
def setv(self, cs, ch, voltage): ...
```

### ArduinoControllerCS.zero

[Show source in ArduinoControllerCS.py:129](../../../ArduinoControllerCS.py#L129)

Sets all 64 voltages to zero, does not adjust volatile memory.

#### Signature

```python
def zero(self): ...
```