import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import analyzer
import datetime

def data_getn():
	None

def init():
	None

def run():
	None


fig, ax = plt.subplots()
lines = []

#line1, = ax.plot([],[],lw=2)
#line2, = ax.plot([], [], lw=2)

ax.grid()
xdata, ydata = [], []
top_limit = 1100
time_window = 60

def init():
	ax.set_ylim(0, top_limit)
	ax.set_xlim(0, time_window)
	del xdata[:]
	del ydata[:]

#init()


raw_data = analyzer.get_data('10.0.0.171', 'apache2.log')

dados = {}

lx = []
ly = []

x_minimum = raw_data[0].hora.hour * 60 * 60 + raw_data[0].hora.minute*60 + raw_data[0].hora.second
x_maximum = raw_data[0].hora.hour * 60 * 60 + raw_data[0].hora.minute*60 + raw_data[0].hora.second

seconds_interval = 5
min_hash = x_minimum / seconds_interval

# Y = maior resolucão pedida
# resumindo os dados para periodos de <seconds_interval> segundos
dados = {}
for info in raw_data:
	print info

	if info.resolution is None:
		continue

	vx = info.hora.hour * 60 * 60 + info.hora.minute*60 + info.hora.second
	interval = vx/seconds_interval
	if interval not in dados:
		dados[ interval ] = {}

	if info.resolution not in dados[interval]:
		dados[interval][info.resolution] = 1
	else:
		dados[interval][info.resolution] += 1

	if x_minimum > vx:
		x_minimum = vx
		min_hash = x_minimum / 5
	if x_maximum < vx:
		x_maximum = vx

for time in dados:
	vx = time*seconds_interval
	#print '%s -> %s' % (vx, dados[time])

	for resolution in lines:
		lines[resolution][0].append(vx)
		
		if resolution in dados[time]:
			lines[resolution][1].append(dados[time][resolution])
		else:
			lines[resolution][1].append(0)

line, = ax.plot([], [], lw=2)
line.set_data(, )

	#print '%s -> %s' % (lines[key][0], lines[key][1])


ax.set_ylim(0, 10)
ax.set_xlim( (x_minimum/seconds_interval) * seconds_interval, (x_maximum/seconds_interval) * seconds_interval)


plt.show()
