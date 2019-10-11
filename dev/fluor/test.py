#! python3
"""
Created on Thu Oct 10 21:31:04 2019

@author: Joe
"""

import matplotlib.pyplot as plt
import numpy as np

n = 20001

x1 = [0, 10000, 20000]
y1 = [0, 1000, 2500]

x = np.linspace(0,max(x1),n)
y = np.interp(x,x1,y1)

dx = (max(x) - min(x))/n

#plt.plot(x,y)
e = 0
f = 0

for i,j in enumerate(x):
	a = j
	b = j + 500
	try:
		if (y[i+1]-y[i])/(x[i+1]-x[i]) == (y[i+500]-y[i+499])/(x[i+500]-x[i+499]):
			A = (y[i+500] - y[i])*500/2
			yb = y[i+500]
			y0 = y[i]
			while yb > y0:
				yb1 = yb + m1*dx
				 
	except IndexError:
		A += 0
	
	