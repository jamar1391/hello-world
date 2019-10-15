import matplotlib.pyplot as plt
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

t_vals = [.5 / 2, .624 / 2, .75 / 2, 1 / 2, 1.25 / 2]

ideal_pipes = [[], [], [], [], [], [], []]

for i, j in enumerate(P_stat_max):
    for k in j:
        t = (k - 14.7) * (30) / (2 * .72 * 52000)
        if t <= .25:
            ideal_pipes[i].append(schedules[0]['Name'])
        elif t <= .624 / 2:
            ideal_pipes[i].append(schedules[1]['Name'])
        elif t <= .75 / 2:
            ideal_pipes[i].append(schedules[2]['Name'])
        elif t <= 1 / 2:
            ideal_pipes[i].append(schedules[3]['Name'])
        elif t <= 1.25 / 2:
            ideal_pipes[i].append(schedules[4]['Name'])
        else:
            ideal_pipes[i].append('Error: Pressure too great')

# uses itertools combinatorics to create a list of every combination of
# 3 schedules out of the 5 available (n choose k)
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
