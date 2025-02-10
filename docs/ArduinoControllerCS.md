# Arduinocontrollercs

[Shimcoil Index](./README.md#shimcoil-index) / Arduinocontrollercs

> Auto-generated documentation for [ArduinoControllerCS](../../../ArduinoControllerCS.py) module.

- [Arduinocontrollercs](#arduinocontrollercs)
  - [ArduinoControllerCS](#arduinocontrollercs)
    - [ArduinoControllerCS._readuntil](#ArduinoControllerCS_readuntil)
    - [ArduinoControllerCS._set](#ArduinoControllerCS_set)
    - [ArduinoControllerCS.disconnect](#ArduinoControllerCSdisconnect)
    - [ArduinoControllerCS.pwr_down](#ArduinoControllerCSpwr_down)
    - [ArduinoControllerCS.set_mux](#ArduinoControllerCSset_mux)
    - [ArduinoControllerCS.setv](#ArduinoControllerCSsetv)
    - [ArduinoControllerCS.zero](#ArduinoControllerCSzero)

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