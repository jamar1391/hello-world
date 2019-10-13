import matplotlib.pyplot as plt
import numpy as np

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

for i in range(len(junctions)-1):
	length = junctions[i+1]-junctions[i]
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

schedules = [{'Name': 'Schedule 5',  'ID': 29.5,   't': .5/2,
			  'Area': ((15**2)-((29.5/2)**2))*np.pi},
			 {'Name': 'Schedule 10', 'ID': 29.376, 't': .624/2,
			  'Area': ((15**2)-((29.376/2)**2))*np.pi},
			 {'Name': 'STD',         'ID': 29.25,  't': .75/2,
			  'Area': ((15**2)-((29.25/2)**2))*np.pi},
			 {'Name': 'Schedule 20', 'ID': 29,     't': 1/2,
			  'Area': ((15**2)-((29/2)**2))*np.pi},
			 {'Name': 'Schedule 30', 'ID': 28.75,  't': 1.25/2,
			  'Area': ((15**2)-((28.75/2)**2))*np.pi}]

pipes = [[],[],[],[],[],[],[]]

for i,j in enumerate(P_stat_max):
	for k in j:
		t = k * (30) / (2 * .72 * 55000)
		if t <= .25:
			pipes[i].append(schedules[0]['Name'])
		elif t <= .624/2:
			pipes[i].append(schedules[1]['Name'])
		elif t <= .75/2:
			pipes[i].append(schedules[2]['Name'])
		elif t <= 1/2:
			pipes[i].append(schedules[3]['Name'])
		elif t <= 1.25/2:
			pipes[i].append(schedules[4]['Name'])
		else:
			pipes[i].append('Error: Pressure too great')
		
		