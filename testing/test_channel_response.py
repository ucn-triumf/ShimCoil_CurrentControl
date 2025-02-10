# test channel linearity and noise
# Derek Fujimoto
# Feb 2025

from ShimCoil import ShimController
from SiglentDevices import SDS5034
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

import matplotlib as mpl


# settings
coil = 17
npts = 20
setpoints = np.linspace(-10, 10, npts)
np.random.shuffle(setpoints)

print('Voltage setpoints')
print('\n'.join(setpoints.astype(str)))

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
read_mean = np.zeros(npts)
read_std = np.zeros(npts)

# setup connections
scope = SDS5034('tucan-scope1.triumf.ca')

with ShimController('COM4') as shim:
    for i,v in tqdm(enumerate(setpoints), desc='Setting coil voltages', total=npts):

        # set voltage and wait for scope to populate
        shim.set_voltage(coil, v)
        scope.run()
        time.sleep(5)

        # get readback
        read_mean[i] = scope.get_measure_adv_value(1)
        read_std[i]  = scope.get_measure_adv_value(2)

    shim.set_voltage(coil, 0)

# draw
plt.errorbar(setpoints, read_mean, read_std, fmt='o', fillstyle='none')
plt.xlabel('Set Voltage (V)')
plt.ylabel('Read Voltage (V)')
plt.title(f'Coil {coil}')
plt.tight_layout()
