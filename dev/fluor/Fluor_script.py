#!usr/bin/env
"""
Created on Sat Oct  5 15:19:17 2019

@author: Joe
"""

from matplotlib import pyplot as plt
import numpy as np
from itertools import combinations


junctions = [0,
             10000,
             20000,
             30000,
             50000,
             80000,
             100000,
             110000,
             120000,
             150000,
             160000,
             180000,
             200000]

sections = []

for i in range(len(junctions) - 1):
    length = junctions[i + 1] - junctions[i]
    sections.append(length)


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

dx = 10  # size of sample along x-axis [ft]
n = (200000/dx)+1

# create n equally spaced partitions on x:
x = np.linspace(min(x1), max(x1), int(n))

# use more precise values to interpolate y and D at x:
y = np.interp(x,x1,y1)
D = np.interp(x,x1,D1)

locations = list(zip(x,y,D))  # y values are not unique but x and D are

# These pressures are generated in AFT Fathom; the first list is the pressure
# in each section if the pump were placed at junction 4, the second list is the 
# max pressures if the pump is placed at junction 5, etc...
P_stat_max = [
    [114.5, 960.2, 960.2, 1960.4, 1724.6, 1565.7,
     1373.1, 1320.1, 1288.8, 1064.9, 968.6, 408.4],

    [114.5, 960.2, 960.2, 950.5, 1724.6, 1565.7,
     1373.1, 1320.1, 1288.8, 1064.9, 968.6, 408.4],

    [114.5, 960.2, 960.2, 950.5, 714.7, 1565.7,
     1373.1, 1320.1, 1288.8, 1064.9, 968.6, 408.4],

    [114.5, 960.2, 960.2, 950.5, 714.7, 555.7,
     1373.1, 1320.1, 1288.8, 1064.9, 968.6, 408.4],

    [114.5, 960.2, 960.2, 950.5, 714.7, 555.7,
     363.2, 1320.1, 1288.8, 1064.9, 968.6, 408.4],

    [114.5, 960.2, 960.2, 950.5, 714.7, 555.7,
     363.2, 310.2, 1288.8, 1064.9, 968.6, 408.4],

    [114.5, 960.2, 960.2, 950.5, 714.7, 555.7,
     363.2, 310.2, 278.8, 1064.9, 968.6, 408.4]
]

# Define all pumps and their values--
# Can be changed for modular optimization
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

# Build list of pumps to use iteratively:
pumps = [pumpA, pumpB, pumpC, pumpD, pumpE, pumpF]

# initialize dictionaries for different soil type characteristics:
slope = {'Silty Sand': 1,
         'Stable Rock': 10,
         'Medium Dense Sand': .66667,
         'Firm Clay': 1.3333} # max slope of soil type [v/h]

b_press = {'Silty Sand': 2000,
           'Stable Rock': 6000,
           'Medium Dense Sand': 2500,
           'Firm Clay': 1500} # b_press == max soil bearing pressure [psi]

cost_multiplier = {'Silty Sand': 1,
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
          'Firm Clay': 106} # unit weight of soil [lb/ft3]

earth = []

# Assigns soil type to each discrete "chunk" along x, based on distance along pipeline:
for i in locations:
    if i[2] < 20001 or (120001 < i[2] < 150001):
        earth.append((i[2],'Silty Sand'))
    elif i[2] < 80001 or i[2] > 180001:
        earth.append((i[2],'Stable Rock'))
    elif i[2] < 120001:
        earth.append((i[2],'Medium Dense Sand'))
    else:
        earth.append((i[2],'Firm Clay'))

# initializes list of excavations based on starting location
exc = []

for i,j in enumerate(x[3000:-1050]): # for each starting location between 30000 and 189500:
    a = i + int(30000/dx)            # a = starting location index
    b = a + int(500/dx)              # b = ending location index (500 [ft] away)
    y0 = y[a]                        # the constant used as the base axis for integration
    A = 0                            # Accumulator for the area to be made flat
    B = 0                            # Accumulator for the area to be sloped based on soil type
    counter = 0
    if slope[earth[a][1]] == slope[earth[b][1]]: # if the slope stays the same, it's a 
        A = (y[b]-y[a])*500/2                    # simple triangle
        while y0 < y[b+counter]:
            B += (y[a+counter] - y0)*dx
            y0 += (slope[earth[a + counter][1]])*dx
            counter += 1
        exc.append(((A+B)*500,a)) # a 500x multiplier is applied to make the resulting flat area
                                  # 500'x500'
    else:
        for section in range(a,b):
            temp = ((1/2)*(y[section]+y[section+1])-y[a])*dx
            A += temp
        while y0 < y[a+counter]:
            B += (y[a+counter] - y0)*dx
            y0 += (slope[earth[a + counter][1]])*dx
            counter += 1
        exc.append(((A+B)*500,a))

x_locs      = []
exc_amounts = []

for i in exc:
    x_locs.append(i[1])
    exc_amounts.append(i[0])

# we consider each junction as a potential pump location:
# the first 4 indices can be thrown out; they are within 30000 [ft] of start
# the last 2 indices can be thrown out; pressure drop is too much by then (negative NPSHA)
juncs = [50000, 80000, 100000, 110000, 120000, 150000, 160000]

x_locs      = x_locs[:-2951]
exc_amounts = exc_amounts[:-2951]

plt.plot(x_locs,exc_amounts) 
for i in juncs:
    plt.axvline(x=(i/dx), color='r',linestyle=':')

# In order to overlap a junction, the cut must start within 500 feet of it.
# Ideally, for any given junction, we will select the starting location that
# yields the lowest requirement for excavation volume:

junc_ind       = [] # this will make junction indices easier to reference
cut_start_locs = []

for jx in juncs:
    junc_ind.append(int(jx/dx))

for i,jx in enumerate(junc_ind):
    temp = exc_amounts[jx-3050:jx-2999]
    a = min(temp)
    cut_start_locs.append((i+4,a))


# We still need to calculate the number of trackhoe-days and truck-days that
# will be necessary in order to excavate each of these spots. Once we do this,
# we can apply a 3x multiplier to the trackhoe costs in locations made of rock;
# this step has to wait until after calculating the costs, because the 3x
# multiplier DOES NOT apply to the dump trucks

track_hoe  = 2700 #[ft3/day], converted from [yd3/day]
cost_th    = 5000 #[$/day]
dump_truck = 810  #[ft3/day]
cost_dt    = 1000 #[$/day]

# lowest starting location that covers each junction (determined visually):
a = [4990, 7951, 10000, 11000, 11951, 14951, 15951] # in index format (reduced by factor of dx)

exc_costs = []
for i in a:
    excavation = exc[i-3000][0]  #[ft3]

    # perform floor division (can't have half a truck), factor in excavation
    # multiplier, add one (have to round up to ensure sufficient qty)
    hoe_days = (excavation//track_hoe) * cost_multiplier[earth[i][1]] + 1
    hoe_cost = hoe_days * cost_th

    truck_days = (excavation//dump_truck) + 1
    truck_cost = truck_days * cost_dt

    cost = hoe_cost + truck_cost
    exc_costs.append((cost,i))

# The variable exc_costs now contains a list of tuples, each tuple
# consisting of (excavation cost [$], junction #). This excavation cost
# does not yet take into account the construction of the pump foundation.

# now we will narrow down the pump options at each junction:
hp_req = 6545 # hp is a constant requirement, independent of pump location
npsha = [2197, 1652, 1284, 839, 717, 644, 127]
i_junc = [4, 5, 6, 7, 8, 9, 10]
viable_pumps = []

for i,j in enumerate(zip(npsha,i_junc)):
    for pump in pumps:
        if pump['NPSHA'] < j[0] and pump['hp'] > hp_req:
            viable_pumps.append((j[1],pump))

# There are 19 viable pump/junction combinations occurring over the course
# of 7 discrete junctions;
# Iterating through each combination, we can determine foundation details:

exc_costs_shifted = []
for i in range(11):
    if i < 4:
        exc_costs_shifted.append((0,0))

    else:
        exc_costs_shifted.append(exc_costs[i-5])


solution_details = [] 
unit_weight_concrete = 145  # [lb/ft3]

for jx,pump in viable_pumps:

    i = jx - 4
    type_soil = earth[a[i]][1]
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

    solution_details.append({'Junction': jx, 'Pump': pump['Name'], 'PumpCost': pump['Cost'],
                                'Vol_f': vol + (Wf*Lf*H), 'H_p': Hp, 'soil': type_soil,
                                'L_p': Lp, 'W_p': Wp, 'H_f': H, 'L_f': Lf, 'W_f': Wf,
                                'Pressures':P_stat_max[i],
                                'TotalCost': pump['Cost'] + exc_costs_shifted[jx][0]})

    # the above variable, foundation_details, yields a list of 19 dictionaries

# Finally, we use the 19 dictionaries to test possible pipe configs:

schedules = [{'Name': 'Schedule 5', 'ID': 29.5, 't': .5 / 2,
              'Area': ((15 ** 2) - ((29.5 / 2) ** 2)) * np.pi},
             {'Name': 'Schedule 10', 'ID': 29.376, 't': .624 / 2,
              'Area': ((15 ** 2) - ((29.376 / 2) ** 2)) * np.pi},
             {'Name': 'STD', 'ID': 29.25, 't': .75 / 2,
              'Area': ((15 ** 2) - ((29.25 / 2) ** 2)) * np.pi},
             {'Name': 'Schedule 20', 'ID': 29, 't': 1 / 2,
              'Area': ((15 ** 2) - ((29 / 2) ** 2)) * np.pi},
             {'Name': 'Schedule 30', 'ID': 28.75, 't': 1.25 / 2,
              'Area': ((15 ** 2) - ((28.75 / 2) ** 2)) * np.pi}]

# Create every possible combination of three pipe schedules from the five available;
# this is known as 'n choose k' combinatorics
# combined = list(combinations(schedules, 3))

t_vals = [.5 / 2, .624 / 2, .75 / 2, 1 / 2, 1.25 / 2]

combined = list(combinations(t_vals, 3))

final_list = []

for h, i in enumerate(P_stat_max):
    final_list.append([])
    for j in i:
        for k in combined:
            for m in range(3):
                if k[m] >= (((j - 14.7) * 30) / (2 * .72 * 52000)):
                    final_list[h].append(k)
                    break

seen = [{}, {}, {}, {}, {}, {}, {}]
dupes = []

for i in range(len(final_list)):
    for x in final_list[i]:
        if x not in seen[i]:
            seen[i][x] = 1
        else:
            if seen[i][x] == 1:
                dupes.append(x)
            seen[i][x] += 1

working_list = []

for i, j in enumerate(seen):
    for x in j:
        if j[x] == 12:
            working_list.append((x, i + 4))

pipe_vols = []

for group in working_list:
    for i in range(len(P_stat_max)):
        vol = 0
        for section, pressure in zip(sections, P_stat_max[i]):
            for thickness in group[0]:
                if (pressure - 14.7) < 2496 * thickness:
                    Area_in2 = ((15 ** 2) - ((15 - thickness) ** 2)) * np.pi
                    Area_ft2 = Area_in2 / 144
                    vol_ft3 = Area_ft2 * section
                    break
                # else:

            vol += vol_ft3
        pipe_vols.append((vol, group))

pipe_vols = sorted(pipe_vols)

pipe_costs = []
pipe_weights = []

for i in pipe_vols:
    cost = (i[0] * 490 * 3)
    weight = (i[0] * 490 / 2000)  # [tons]
    pipe_costs.append((cost, i[1]))
    pipe_weights.append((weight, i[1]))

# for i in solution_details:
#     for p in i['Pressures']:
#         for j,k in enumerate(p):
#             for m in combined:
#                 for n in range(3):
#                     if m[n]['t'] < (.0004006 * k):
#                         pass