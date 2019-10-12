#!usr/bin/env
"""
Created on Sat Oct  5 15:19:17 2019

@author: Joe
"""

from matplotlib import pyplot as plt
import numpy as np

# Distance between junctions:
D1 = [0, 10000, 20000, 30000,
	 50000, 80000, 100000, 110000, 
	 120000, 150000, 160000, 180000, 200000]

# Elevation at each junction:
y1 = [2000, 2000, 0, 0, 
	  500, 800, 1200, 1300, 
	  1350, 1800, 2000, 3250, 4000]

# Initial x-value at start:
x1 = [0]

# Derive x-values at junctions based on D and y:
for i in range(len(D1)-1):
	x_i = ((D1[i+1]-D1[i])**2 - (y1[i+1]-y1[i])**2)**(1/2) + x1[i]
	x1.append(x_i)

# print(x1)

dx = 10  # size of sample along x-axis [ft]
n = (200000/dx)+1

pumpA = {'Name': 'A', 'Weight': 4500, 'Length': 7,
		 'Width': 9, 'Cost': 3000000,
		 'NPSHA': 400, 'hp': 7000}

pumpB = {'Name': 'B', 'Weight': 7000, 'Length': 10,
		 'Width': 12, 'Cost': 4250000,
		 'NPSHA': 200, 'hp': 8000}

pumpC = {'Name': 'C', 'Weight': 8500, 'Length': 12,
		 'Width': 14, 'Cost': 2400000,
		 'NPSHA': 50, 'hp': 4000}

pumpD = {'Name': 'D', 'Weight': 7500, 'Length': 10,
		 'Width': 10, 'Cost': 2250000,
		 'NPSHA': 100, 'hp': 6500}

pumpE = {'Name': 'E', 'Weight': 10000, 'Length': 15,
		 'Width': 15, 'Cost': 3600000,
		 'NPSHA': 100, 'hp': 7500}

pumpF = {'Name': 'F', 'Weight': 4000, 'Length': 6,
		 'Width': 8, 'Cost': 2000000,
		 'NPSHA': 50, 'hp': 3500}

pumps = [pumpA, pumpB, pumpC, pumpD, pumpE, pumpF]

# create n equally spaced partitions on x:
x = np.linspace(min(x1), max(x1), int(n))

# use more precise values to interpolate y and D at x:
y = np.interp(x,x1,y1)
D = np.interp(x,x1,D1)

locations = list(zip(x,y,D))  # y values are not unique but x and D are

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

# plt.plot(x,y)

earth = []

# Assigns soil type to each discrete "chunk" along x, based on distance along pipeline:
for i in locations:
	if i[2] < 20001 or (120001 < i[2] < 150001):
		earth.append((i,'Silty Sand'))
	elif i[2] < 80001 or i[2] > 180001:
		earth.append((i,'Stable Rock'))
	elif i[2] < 120001:
		earth.append((i,'Medium Dense Sand'))
	else:
		earth.append((i,'Firm Clay'))

# initializes list of excavations based on starting location
exc = []


for i,j in enumerate(x[3000:-1050]): # for each starting location between 30000 and 189500:
	a = i + int(30000/dx)            # a = starting location index
	b = a + int(500/dx)              # b = ending location index (500 [ft] away)
	y0 = y[a]                        # the constant used as the base axis for integration
#	yb = y[i+500]
	A = 0                            # Accumulator for the area to be made flat
	B = 0                            # Accumulator for the area to be sloped based on soil type
	counter = 0
	if slope[earth[a][1]] == slope[earth[b][1]]:
		A = (y[b]-y[a])*500/2
		if earth[a][1] == 'Stable Rock':
			A *= 3
		while y0 < y[b+counter]:
			temp = (y[a+counter] - y0)*dx
			if earth[a+counter][1] == 'Stable Rock':
				temp *= 3
			B += temp
			y0 += (slope[earth[a + counter][1]])*dx
			counter += 1
		exc.append((A+B,a))

	else:
		for section in range(a,b):
			temp = ((1/2)*(y[section]+y[section+1])-y[a])*dx
			if earth[section][1] == 'Stable Rock':
				temp *= 3
			A += temp
		while y0 < y[a+counter]:
			temp = (y[a+counter] - y0)*dx
			if earth[a+counter][1] == 'Stable Rock':
				temp *= 3
			B += temp
			y0 += (slope[earth[a + counter][1]])*dx
			counter += 1
		exc.append((A+B,a))

x_new = []    # initialize truncated list for x range [ft]
y_new = []    # initialize list of excavation values [ft2]

for i in exc:
	x_new.append(i[1])
	y_new.append(i[0])

#plt.plot(x_new,y_new)

# now I need to throw out all the values that occur between junctions,
# since the only viable pump location (currently) is at a junction

# Junctions occur at D1 locations:
# D1 = [0, 10000, 20000, 30000,
# 	 50000, 80000, 100000, 110000,
# 	 120000, 150000, 160000, 180000, 200000]

# we consider each junction as a potential pump location:
# the first 4 indices can be thrown out; they are within 30000 [ft] of start
# the last 2 indices can be thrown out; pressure drop is too much by then (negative NPSHA)

track_hoe  = 2700 #[ft3/day]
cost_th    = 5000 #[$/day]
dump_truck = 810  #[ft3/day]
cost_dt    = 1000 #[$/day]


juncs = [50000, 80000, 100000, 110000, 120000, 150000, 160000]

# lowest starting location that touches each junction (determined visually):
a = [4990, 7974, 10000, 11000, 11950, 14950, 15950]
jxdex = [5000, 8000, 10000, 11000, 12000, 15000, 16000] # index at which junction lives


npsha = [2197, 1652, 1284, 839, 717, 644, 127] # npsha for pump at given junction
hp_req = 6545  # one pump system, hp requirement is constant

temp_list = list(zip(juncs,npsha))
n_juncs = [] # initialize enumerated list of each junction and the corresponding npsha

for i,j in enumerate(temp_list):
	n_juncs.append((i+4, j[0], j[1])) # (i+4) because the first available junction is #4

viable_pumps = []

for junction in n_juncs:
	for pump in pumps:
		if pump['NPSHA'] < junction[2] and pump['hp'] > hp_req:
			viable_pumps.append((junction[0],pump))

exc_costs = []		
for i in a:
	excavation = exc[i-3000][0] * 500  #[ft3]

	if (excavation % track_hoe) != 0:
		hoe_days = (excavation//track_hoe) + 1
	else:
		hoe_days = excavation/track_hoe

	hoe_cost = hoe_days * cost_th

	if (excavation % dump_truck) != 0:
		truck_days = (excavation//dump_truck) + 1
	else:
		truck_days = excavation/dump_truck

	truck_cost = truck_days * cost_dt
	cost = hoe_cost + truck_cost
	exc_costs.append((cost,i))

pedestal_dimensions = [] # list of dicts with jx, pump, Hp, Lp, Wp, H, Lf, Wf
unit_weight_concrete = 145 # [lb/ft3]

for jx,pump in viable_pumps:
	i = jx - 4
	type_soil = earth[jxdex[i]][1]
	unit_weight_soil = weight[type_soil]
	H = 1.5
	found_depth = fnd_depth[type_soil]
	pump_weight = pump['Weight']
	Lp = pump['Length'] + 1
	Wp = pump['Width'] + 1
	Hp = found_depth - .5
	Wf = Wp  # initializing value (guess) for footing width
	Lf = Lp  # initializing value (guess) for footing length
	vol_footing  = Wf * Lf * H
	vol_pedestal = Wp * Lp * Hp
	Ap = Wp * Lp # Area of pedestal also represents volume of exposed pedestal (height = 1)
	weight_soil = (vol_footing + vol_pedestal - Ap) * unit_weight_soil
	Af = Wf*Lf
	weight_foundation = (pump_weight + (vol_footing * unit_weight_concrete) +
						 (vol_pedestal * unit_weight_concrete) - weight_soil)

	while (weight_foundation/Af) > b_press[type_soil]:
		Wf += .01
		Lf += .01

	if (Wf - 1) < Wp:
		Lp = Lf
		Wp = Wf
		H = 0
		Hp += 1.5
		vol = Wp * Lp * Hp

		while (weight_foundation/Af) > b_press[type_soil]:
			vol = Wp * Lp * Hp
			weight_foundation = pump_weight + (vol * unit_weight_concrete)
			Wp += .01
			Lp += .01

	pedestal_dimensions.append({'Junction': jx, 'Pump': pump['Name'], 'Vol_f': vol + (Wf*Lf*H), 'H_p': Hp,
								'L_p': Lp, 'W_p': Wp, 'H_f': H, 'L_f': Lf, 'W_f': Wf})

vol_exc = []



accrued_list = [] # list of tuples: (jx, pump, v_f, v_e, v_moved, v_trucked, cost_cum)