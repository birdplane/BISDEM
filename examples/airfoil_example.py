import os
import numpy as np
from fusedwind.turbine.configurations import configure_bladesurface
from fusedwind.turbine.geometry import read_blade_planform
from openmdao.main.api import Assembly

top = Assembly()

configure_bladesurface(top, '../../git/BISDEM/data/DTU_10MW_RWT_blade_axis_prebend.dat', planform_nC=6)

# load the planform file
top.blade_length = 86.366
top.span_ni = 50

print 'planform variables: ', top.pf_splines.pfOut.list_vars()

b = top.blade_surface

# distribute 200 points evenly along the airfoil sections
b.chord_ni = 200

# load the airfoil shapes defining the blade
for f in ['../../git/BISDEM/data/ffaw3241.dat',
          '../../git/BISDEM/data/ffaw3301.dat',
          '../../git/BISDEM/data/ffaw3360.dat',
          '../../git/BISDEM/data/ffaw3480.dat' ,
          '../../git/BISDEM/data/tc72.dat' ,
          '../../git/BISDEM/data/cylinder.dat']:

    b.base_airfoils.append(np.loadtxt(f))

b.blend_var = np.array([0.241, 0.301, 0.36, 0.48, 0.72, 1.])
top.pf_splines.s = 1.0
top.run()

pf = top.pf_splines.pfOut

plt.figure()
plt.title('chord')
plt.plot(pf.s, pf.chord)
plt.savefig('chord.eps')
plt.figure()
plt.title('twist')
plt.plot(pf.s, pf.rot_z)
plt.savefig('twist.eps')
plt.figure()
plt.title('relative thickness')
plt.plot(pf.s, pf.rthick)
plt.savefig('rthick.eps')
plt.figure()
plt.title('pitch axis aft leading edge')
plt.plot(pf.s, pf.p_le)
plt.savefig('p_le.eps')

plt.figure()
plt.axis('equal')
for i in range(b.span_ni):
    plt.plot(b.surfout.surface[:, i, 0], b.surfout.surface[:, i, 1])
plt.savefig('lofted_blade.eps')
plt.savefig('lofted_blade.png')