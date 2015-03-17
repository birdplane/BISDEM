import numpy as np
import matplotlib.pyplot as plt

from BISDEM.WingSE.wingsurface import WingSurface
from BISDEM.lib.vartrees import WingPlanformVT

from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float, List, Slot, File, FileRef
from fusedwind.turbine.geometry_vt import BeamGeometryVT, BladePlanformVT
from fusedwind.lib.geom_tools import calculate_length

from os.path import expanduser
home = expanduser("~")

surface = WingSurface()
beam = BeamGeometryVT()
beam.x = np.array([0, 0.0, -0.05]);
beam.y = np.array([0, -0.01, -0.02]);
beam.z = np.array([0, 0.1, 0.2]);
beam.s = calculate_length(np.array([beam.x, beam.y, beam.z]).T)
beam.rot_x = [0, 0, 0];
beam.rot_y = [0, 0, 0];
beam.rot_z = [0, 0, 0];

# Normalize input data
beam.x = beam.x/beam.z[-1]
beam.y = beam.y/beam.z[-1]
beam.z = beam.z/beam.z[-1]
beam.s = beam.s/beam.s[-1]

surface.eqspar_geom  = [beam]

print "s: ", beam.s

planform = WingPlanformVT();
planform.blade_length = .2;
planform.chord = [1, 1, 0.5];
planform.chord = planform.chord/beam.z[-1]
planform.rthick = np.array([0.05, 0.05, 0.05])/0.05;
planform.p_le = [0.0, 0.0, 0.0];
surface.planform_in = [planform];

airfoil  = open('/home/jan/diesdas.txt', 'rw')
surface.airfoil = [airfoil];

surface.run()
surf = surface.wingsurf

# load the planform file
surf.span_ni = 20

print 'planform variables: ', surf.pf_splines.pfOut.list_vars()


b = surf.blade_surface

# distribute 200 points evenly along the airfoil sections
b.chord_ni = 200
b.base_airfoils.append(np.loadtxt(home+'/git/BISDEM/data/ffaw3241.dat'))
b.base_airfoils.append(np.loadtxt(home+'/git/BISDEM/data/ffaw3301.dat'))
b.blend_var = np.array([0.5, 1.])

surf.run()

pf = surf.pf_splines.pfOut

plt.figure()
plt.title('chord')
plt.plot(pf.s, pf.chord)
plt.savefig('chord.eps')
plt.figure()
plt.axis('equal')
for i in range(b.span_ni):
    plt.plot(b.surfout.surface[:, i, 0], b.surfout.surface[:, i, 1])
plt.savefig('lofted_blade.eps')
plt.savefig('lofted_blade.png')