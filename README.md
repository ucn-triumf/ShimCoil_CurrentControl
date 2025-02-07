# ShimCoil_CurrentControl

This repository was formerly named `current_control` and was imported from [J. Martin's repository](https://github.com/jmartin1454/current_control).

This repository defines a GUI to control the power supply and do measurements with a fluxgate to test coil winding direction. It is expected to run by sending serial commands to an arduino using the code found [here](https://github.com/ucn-triumf/ShimCoil_SerialArduino).

Full documentation [here](docs/README.md)

## Installation and setup

To install on the python path first clone this directory

```
git clone git@github.com:ucn-triumf/ShimCoil_CurrentControl.git
```

Then navigate to this directory and run the following:

```
pip install -e .
```

Note the period at the end of that line. Also, while the `-e` flag will cause edits made to the code (either through `git pull` or directly editing) to be immediately implemented, not all systems like this. If this fails run without the `-e` flag and return the above command every time the code is update to see changes in execution.


## Contents and Usage

This repository defines three objects of note:

1. [`ArduinoControllerCS`](docs/ArduinoControllerCS.md): Base-level controller for the arduino via [serial connection](https://github.com/ucn-triumf/ShimCoil_SerialArduino).
2. [`ArduinoController64`](docs/ArduinoController64.md): Similar to `ArduinoControllerCS`, but abstracts the circuit select/channel ID method out to a 0-63 indexing. Also allows for setting volatile memory on the arduino and eeprom.
3. [`ShimController`](docs/ShimController.md): Top-level controller, this should be the thing you mostly interact with.