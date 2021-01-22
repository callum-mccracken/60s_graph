import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import MultipleLocator
from scipy import interpolate

# various formatting parameters
label_fontsize = 10
tick_fontsize = 10
linewidth = 1
major_xtick_length = 15
minor_xtick_length = 7
major_ytick_length = 7
minor_ytick_length = 0

mpl.rcParams['font.weight'] = 'normal'
mpl.rcParams['axes.linewidth'] = linewidth
mpl.rcParams['lines.linewidth'] = linewidth
mpl.rcParams['xtick.labelsize'] = tick_fontsize
mpl.rcParams['xtick.labelsize'] = tick_fontsize
mpl.rcParams['xtick.major.width'] = linewidth
mpl.rcParams['ytick.major.width'] = linewidth
mpl.rcParams['xtick.minor.width'] = linewidth
mpl.rcParams['ytick.minor.width'] = linewidth


# get data, one extra point for fitting the last spline segment
depth_meters = np.array([0, 5, 19, 33, 41, 57, 65, 150])  # x
zenith_degrees = np.array([24, 27, 25, 23, 16, 10, 5, 0])  # y

# spline plotting, 300 = number of internal points
xnew = np.linspace(depth_meters.min(), depth_meters.max(), 300)
tck = interpolate.splrep(depth_meters, zenith_degrees, s=0)
smooth = interpolate.splev(xnew, tck, der=0)

# this is how it looks on the graph, not sure if this is the real conversion
depth_attenuation = depth_meters / 5

# create figure
fig, ax1 = plt.subplots(figsize=(5,5))

# make smooth line
# plot as solid line between 2nd and 2nd last data point
xnew_solid = [x for x in xnew if x >= depth_meters[1] and x <= depth_meters[-2]]
smooth_solid = [s for s, x in zip(smooth, xnew) if x >= depth_meters[1] and x <= depth_meters[-2]]
ax1.plot(xnew_solid, smooth_solid, c='k')
xnew_dashed_1= [x for x in xnew if x < depth_meters[1]]
smooth_dashed_1 = [s for s, x in zip(smooth, xnew) if x < depth_meters[1]]
ax1.plot(xnew_dashed_1, smooth_dashed_1, 'k--', dashes=(10,2))
xnew_dashed_2= [x for x in xnew if x > depth_meters[-2]]
smooth_dashed_2 = [s for s, x in zip(smooth, xnew) if x > depth_meters[-2]]
ax1.plot(xnew_dashed_2, smooth_dashed_2, 'k--', dashes=(15,3))

# make dots
ax1.scatter(depth_meters, zenith_degrees, s=30, edgecolors='k', clip_on=False, facecolors='w', zorder=10)


# labels
ax1.set_xlabel('D E P T H   ( M E T E R S )', fontsize=label_fontsize, labelpad=10)
ax1.set_ylabel('Z E N I T H   A N G L E   ( D E G R E E S )', fontsize=label_fontsize)

# ticks
ax1.tick_params('x', which='both', bottom=True, top=False, direction='in', labelsize=tick_fontsize)
ax1.tick_params('y', left=True, right=True, direction='in', labelsize=tick_fontsize)
ax1.tick_params('x', which='major', length=major_xtick_length)
ax1.tick_params('x', which='minor', length=minor_xtick_length)
ax1.tick_params('y', which='major', length=major_ytick_length)
ax1.tick_params('y', which='minor', length=minor_ytick_length)
ax1.xaxis.set_major_locator(MultipleLocator(20))
ax1.xaxis.set_minor_locator(MultipleLocator(10))
ax1.yaxis.set_major_locator(MultipleLocator(5))

# second x axis
ax2 = ax1.twiny()
ax2.set_xlabel('D E P T H   ( A T T E N U A T I O N   L E N G T H S )', fontsize=label_fontsize, labelpad=15)
ax2.tick_params('x', which='both', bottom=False, top=True, direction='in', labelsize=tick_fontsize)
ax2.tick_params('x', which='major', length=major_xtick_length)
ax2.tick_params('x', which='minor', length=minor_xtick_length)
ax2.tick_params('y', which='major', length=major_ytick_length)
ax2.tick_params('y', which='minor', length=minor_ytick_length)
ax2.xaxis.set_major_locator(MultipleLocator(4))
ax2.xaxis.set_minor_locator(MultipleLocator(1))

# plot limits
ax1.set_xlim(0,120)
ax1.set_ylim(0,29)
ax2.set_xlim(0,24)

plt.savefig('60s.png')
