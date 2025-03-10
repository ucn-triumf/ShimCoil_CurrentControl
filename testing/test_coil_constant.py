# get coil constants of each coil
# Derek Fujimoto
# March 2025

from ShimCoil import ShimController
from SiglentDevices import SDS5034
import time
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from tqdm import tqdm
import matplotlib as mpl

# settings
coil = 37
npts = 5
sleep_duration = 2 # seconds
setpoints = np.linspace(-10, 10, npts) # voltages to set
V2nT = 1e4 # multiply this to get nT from volts output of fluxgate
gain = 50
outfile = 'coil_const/coil_constants.csv' # save coil constants here

# 35; fixed pin; no current
# 34; fixed solder; current ok
# 33; fixed solder; current ok; shorted?
# 6;  ch ok; pin ok; solder ok; roomc ok; no current

np.random.shuffle(setpoints)
plt.close('all')

#print('Voltage setpoints')
#print('\n'.join(setpoints.astype(str)))

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
        time.sleep(0.25)
        scope.run()
        time.sleep(sleep_duration)

        # get readback
        read_mean[i] = scope.get_measure_adv_value(1)
        read_std[i]  = scope.get_measure_adv_value(2)

    shim.set_voltage(coil, 0)

# convert units to nT
read_mean *= V2nT/gain
read_std *= V2nT/gain

# fit - b assumed to be true background + internal offset
fitfn = lambda x, a, b: a*x+b
par, cov = curve_fit(fitfn, setpoints, read_mean, sigma=read_std, absolute_sigma=True)
std = np.diag(cov)**0.5

# draw
plt.figure()
plt.errorbar(setpoints, read_mean, read_std, fmt='o', fillstyle='none')
plt.plot(setpoints, fitfn(setpoints, *par))
plt.xlabel('Set Voltage (V)')
plt.ylabel('Read Field (nT)')
plt.title(f'Coil {coil}')
plt.tight_layout()
plt.savefig(f'coil_const/coil_const_{coil}.pdf')

# save output

# read header
with open(outfile, 'r') as fid:
    header = [line.strip() for line in fid if line[0] == '#']

# read file
df = pd.read_csv(outfile, comment='#')

df = pd.concat((df, pd.DataFrame({'coil':[coil],
                        'slope':[1/par[0]],
                        'offset':[-par[1]/par[0]],
                        'dslope':[std[0]/par[0]**2],
                        'doffset':[par[1]/par[0]*((std[1]/par[1])**2 + \
                                                 (std[0]/par[0])**2)**0.5],
                                 })
              ))

# write file
with open(outfile, 'w') as fid:
    fid.write('\n'.join(header))
    fid.write('\n')
df.to_csv(outfile, mode='a', index=False)