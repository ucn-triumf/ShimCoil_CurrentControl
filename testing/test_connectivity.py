# Test power supply connectivity
# Derek Fujimoto
# Feb 2025

"""
Connect scope to output of power supply and run this code. Look for even steps in voltage across a resistive load.
"""

from ShimCoil import ShimController
import time

s = ShimController('COM4')

for i in range(54):
    s.set_voltage(i, 5)
    print(f'Loop {i} ON')
    input('Next?')
    s.set_voltage(i, 0)
    print(f'Loop {i} OFF')
    time.sleep(0.2)

s.close()

"""
Broken channels
0 - works!
1 - no offset, high freq white noise for some voltages, not all, 10V works
2 - no offset, high freq white noise for some voltages, not all, 10V works
3 - works!
4 - no offset, high freq white noise for some voltages, not all, 10V works
16 - works!
17 - no offset, high freq white noise for some voltages, not all, 10V works
"""
