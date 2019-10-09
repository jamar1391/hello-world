#!usr/bin/env

# Euler, Heun,and 4th order Runge-Kutta

# Euler's Method

import numpy as np
from matplotlib import pyplot as plt

m = 10e24
G = 6.67e-11
grav = G

# y' = -y + sin(x), y(0) = 1
# y' is first derivative, i.e. slope

x0 = 0
y0 = 1
xf = 10
n = 101
dx = (xf-x0)/(n-1)

x = np.linspace(x0,xf,n)
y = np.zeros([n])

y[0] = y0

for i in range(1,n):
    # y[i] = y[i-1] + (slope * dx)
    y[i] = y[i-1] + (np.sin(x[i-1])-y[i-1])*dx


