#!usr/bin/env
"""
Created on Sat Oct  5 15:19:17 2019

@author: Joe
"""

from matplotlib import pyplot as plt
import numpy as np

# Distance between junctions:
D = [0, 10000, 20000, 30000, 
	 50000, 80000, 100000, 110000, 
	 120000, 150000, 160000, 180000, 200000]

# Elevation at each junction:
y1 = [2000, 2000, 0, 0, 
	  500, 800, 1200, 1300, 
	  1350, 1800, 2000, 3250, 4000]

# Initial x-value at start:
x1 = [0]

n = 20001 # num. of iterations == (factor of 200000) + 1
dx = (max(x1) - min(x1))/n

pumpA = {'Weight': 4500, 'Length': 7, 'Width': 9, 'Cost': 3000000}
pumpB = {'Weight': 7000, 'Length': 10, 'Width': 12, 'Cost': 4250000}
pumpC = {'Weight': 8500, 'Length': 12, 'Width': 14, 'Cost': 2400000}
pumpD = {'Weight': 7500, 'Length': 10, 'Width': 10, 'Cost': 2250000}
pumpE = {'Weight': 10000, 'Length': 15, 'Width': 15, 'Cost': 3600000}
pumpF = {'Weight': 4000, 'Length': 6, 'Width': 8, 'Cost': 2000000}

pumps = [pumpA, pumpB, pumpC, pumpD, pumpE, pumpF]

# Derive x-values at junctions based on D and y:
for i in range(len(D)-1):
    x_i = ((D[i+1]-D[i])**2 - (y1[i+1]-y1[i])**2)**(1/2) + x1[i]
    x1.append(x_i)

#print(x1)

# create n equally spaced partitions on x:
x = np.linspace(min(x1), max(x1), n)

# use more precise values to interpolate y at x:
y = np.interp(x,x1,y1)

# initialize dictionaries:
slope = {'Silty Sand': 1, 
		 'Stable Rock': 10, 
		 'Medium Dense Sand': .66667, 
		 'Firm Clay': 1.3333} # max slope of soil type [v/h]

b_press = {'Silty Sand': 2000, 
		   'Stable Rock': 6000, 
		   'Medium Dense Sand': 2500, 
		   'Firm Clay': 1500} # b_press == max soil bearing pressure [psi]

exc_cost = {'Silty Sand': 1, 
			'Stable Rock': 3, 
			'Medium Dense Sand': 1, 
			'Firm Clay': 1} # Excavation cost [$]

fnd_depth = {'Silty Sand': 4, 
			 'Stable Rock': 2, 
			 'Medium Dense Sand': 3, 
			 'Firm Clay': 3} # Foundation Depth [ft]

weight = {'Silty Sand': 99, 
		  'Stable Rock': 167, 
		  'Medium Dense Sand': 116, 
		  'Firm Clay': 106} # unit weight of soil [lb]

plt.plot(x,y)

earth = []

# Assigns soil type to each discrete "chunk" along x:
for i in x:
    if i < 20001 or (i > 120001 and i < 150001):
        earth.append((i,'Silty Sand'))
    elif i < 80001 or i > 180001:
        earth.append((i,'Stable Rock'))
    elif i < 120001:
        earth.append((i,'Medium Dense Sand'))
    else:
        earth.append((i,'Firm Clay'))

exc = []

for i,j in enumerate(x[3000:-1050]):
	a = x[i]
	b = x[i+500]
	y0 = y[i]
#	yb = y[i+500]
	A = 0
	B = 0
	counter = 0
	if slope[earth[i][1]] == slope[earth[i+500][1]]:
		A = (y[i+500]-y[i])*500/2
		while y0 < y[i+counter]:			 
			B += (y[i+counter] - y0)*dx
			y0 += (slope[earth[i + counter][1]])*dx
			counter += 1
		exc.append((i+3000,A+B))
	
	else:
		pass
		