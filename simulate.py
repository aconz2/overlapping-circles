#!/usr/bin/env python

import shapely.geometry as geo
import shapely.affinity as aff
import matplotlib.pyplot as plt
import numpy as np
from descartes import PolygonPatch
from matplotlib import animation

# radius of rotation
R = 5
# radius of circle
r = 2
# buffer resolution (segments used to approximate circle)
res = 500

################################################################################
# Simulation by rotation #
##########################

# degree step
d_steps = 300
# degree "linspace"
d_space = np.linspace(0, np.pi, d_steps)

# stationary/reference circle, (the hole)
circ_ref = geo.Point(0, R).buffer(r, resolution=res)
# the rotating circle
circ_rot = geo.Point(R, 0).buffer(r, resolution=res)

circ_mover_rotations = [aff.rotate(circ_rot, d, origin=(0,0), use_radians=True) for d in d_space]

# calculate percent intersection area for each rotation of the circle
intersect_areas_rot = [circ_ref.intersection(c).area / circ_ref.area for c in circ_mover_rotations]

################################################################################
# Simulation by translation #
##########################
# the translating circle
circ_trans = geo.Point(R * np.pi / 2, R).buffer(r, resolution=res)

# generate (lazily) all translations of circle from leftmost to rightmost
circ_mover_translations = [aff.translate(circ_trans, xoff=-x) for x in R * d_space]

# calculate intersection area for each rotation of the circle
intersect_areas_trans = [circ_ref.intersection(c).area / circ_ref.area for c in circ_mover_translations]

################################################################################
# Animation #
##########################
fig = plt.figure()
ax_up = fig.add_subplot(121)
ax_up.set_xlim(-R - 1.2 * r, R + 1.2 * r)
ax_up.set_ylim(-R - 1.2 * r, R + 1.2 * r)
ax_up.set_aspect(1)

ax_down = fig.add_subplot(122)
ax_down.set_xlim(0, np.pi)
ax_down.set_xticks(np.linspace(0, np.pi, 8))
ax_down.set_ylim(0, 1)
ax_down.set_aspect(np.pi)

def frame(n):
	ax_up.cla()
	ax_up.add_patch(PolygonPatch(circ_ref, fc='gray', alpha=0.25))
	ax_up.add_patch(PolygonPatch(circ_mover_rotations[n], fc='gray', alpha=0.25))
	if circ_ref.intersection(circ_mover_rotations[n]).geom_type == 'Polygon':
		ax_up.add_patch(PolygonPatch(circ_ref.intersection(circ_mover_rotations[n]), fc='blue', alpha=0.5))

	ax_up.add_patch(PolygonPatch(circ_mover_translations[n], fc='gray', alpha=0.25))
	if circ_ref.intersection(circ_mover_translations[n]).geom_type == 'Polygon':
		ax_up.add_patch(PolygonPatch(circ_ref.intersection(circ_mover_translations[n]), fc='red', alpha=0.5))
	
	ax_down.cla()
	ax_down.plot(d_space, intersect_areas_rot, 'b')
	ax_down.plot(d_space[n], intersect_areas_rot[n], 'bo')

	ax_down.plot(d_space, intersect_areas_trans, 'r')
	ax_down.plot(d_space[n], intersect_areas_trans[n], 'ro')

anim = animation.FuncAnimation(fig, frame, frames=d_steps)
anim.save('rotating_circle.mp4', writer='ffmpeg', fps=30, dpi=200)

# and finally the percent of circle's area
#percent_intersect_rot = [a / circ_ref.area for a in intersect_areas]

#plt.figure()
#plt.plot(d_space, percent_intersect_rot, label='rotated')
#plt.legend()

#plt.figure()
#plt.plot(x_space, percent_intersect_tran, label='translated')
#plt.legend()
#plt.show()

################################################################################
# Calculation #
###############
# formula for percent overlap
# [arctan(sqrt(r - (r*sin(d))^2) / r*sin(d)) - r*sin(d)*sqrt(r - (r*sin(d))^2)] / pi

#d_space_ = np.linspace(0, np.pi * 2, 720)
#d_space_ = np.linspace(7 * np.pi / 8, 9 * np.pi / 8, d_steps / 2)
#r_sin_d = r * np.sin(d_space_)
#r_sin_2_d = r_sin_d * r_sin_d

#percent_intersect_calc_1 = (np.arctan(np.sqrt(r - r_sin_2_d) / r_sin_d) - r_sin_d * np.sqrt(r - r_sin_2_d)) / np.pi
# reverse array
#percent_intersect_calc_2 = percent_intersect_calc_1[::-1].copy()
#percent_intersect_calc = np.concatenate(percent_intersect_calc_1, percent_intersect_calc_2)
#percent_intersect_calc = (np.arctan(np.sqrt(r - r_sin_2_d) / r_sin_d) - r_sin_d * np.sqrt(r - r_sin_2_d)) / np.pi
