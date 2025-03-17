# test channel linearity and noise
# Derek Fujimoto
# Feb 2025

from ShimCoil import ShimController
from SiglentDevices import Keithley_DMM6500
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from scipy.optimize import curve_fit
import matplotlib as mpl


# settings
coil = 17
npts = 50
setpoints = np.linspace(-10, 10, npts)
np.random.shuffle(setpoints)
plt.close('all')

# working: 60,61,62, 63

# print('Voltage setpoints')
# print('\n'.join(setpoints.astype(str)))

# drawing style
mpl.rcParams['axes.linewidth'] = 1.5
mpl.rcParams['axes.grid'] = True
mpl.rcParams['axes.labelsize'] = 'medium'

mpl.rcParams['xtick.top'] = True
mpl.rcParams['xtick.bottom'] = True
mpl.rcParams['xtick.major.size'] = 5
mpl.rcParams['xtick.minor.size'] = 3
mpl.rcParams['xtick.major.width'] = 1.5
mpl.rcParams['xtick.minor.width'] = 1.5
mpl.rcParams['xtick.color'] = 'k'
mpl.rcParams['xtick.direction'] = 'in'

mpl.rcParams['ytick.left'] = True
mpl.rcParams['ytick.right'] = True
mpl.rcParams['ytick.major.size'] = 5
mpl.rcParams['ytick.minor.size'] = 3
mpl.rcParams['ytick.major.width'] = 1.5
mpl.rcParams['ytick.minor.width'] = 1.5
mpl.rcParams['ytick.color'] = 'k'
mpl.rcParams['ytick.direction'] = 'in'

mpl.rcParams['grid.color'] = 'b0b0b0'
mpl.rcParams['grid.linestyle'] = '-'
mpl.rcParams['grid.linewidth'] = 0.8
mpl.rcParams['grid.alpha'] = 0.5

mpl.rcParams['errorbar.capsize'] = 0
mpl.rcParams['font.size'] = 16.0


# save results
measurements = np.zeros(npts)

# setup connections
dmm = Keithley_DMM6500()

with ShimController('COM4', debug=True) as shim:
    for i,v in tqdm(enumerate(setpoints), desc='Setting coil voltages', total=npts):

        # set voltage and wait for scope to populate
        shim.set_voltage(coil, v)

        # get a bunch of measurements
        measurements[i] = dmm.get_volt_dc()

    shim.set_voltage(coil, 0)

# fit
fn = lambda x, a, b: a*x+b
par, cov = curve_fit(fn, setpoints, measurements)

print(f'slope: {par[0]}')

# draw
plt.plot(setpoints, measurements, '.')
plt.plot(setpoints, fn(setpoints, *par))
plt.xlabel('Set Voltage (V)')
plt.ylabel('Read Voltage (V)')
plt.title(f'Coil {coil}')
plt.tight_layout()
