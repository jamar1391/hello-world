#!usr/bin/env
"""
Created on Sat Oct  5 15:19:17 2019

@author: Joe
"""

from matplotlib import pyplot as plt
import numpy as np

D = [0, 10000, 20000, 30000, 50000, 80000, 100000, 110000, 120000, 150000, 160000, 180000, 200000]
y1 = [2000, 2000, 0, 0, 500, 800, 1200, 1300, 1350, 1800, 2000, 3250, 4000]
x1 = [0]

for i in range(len(D)-1):
    x_i = ((D[i+1]-D[i])**2 - (y1[i+1]-y1[i])**2)**(1/2) + x1[i]
    x1.append(x_i)

print(x1)

x = np.linspace(0, max(x1), 20001)
y = np.interp(x,x1,y1)

plt.plot(x,y)

# earth = []

# for i in x:
#     if i < 20001 or (i > 120000 and i < 150000):
#         earth.append((i,'Silty Sand'))
#     elif i < 80000 or i > 180000:
#         earth.append((i,'Stable Rock'))
#     elif i <= 120000:
#         earth.append((i,'Medium Dense Sand'))
#     else:
#         earth.append((i,'Firm Clay'))