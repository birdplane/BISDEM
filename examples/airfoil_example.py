import os
import numpy as np
import matplotlib.pyplot as plt
from fusedwind.turbine.configurations import configure_bladesurface
from fusedwind.turbine.geometry import read_blade_planform
from openmdao.main.api import Assembly

from os.path import expanduser
home = expanduser("~")

def lofted_blade_shape_example():

    top = Assembly()

    configure_bladesurface(top, home+'/git/BISDEM/data/DTU_10MW_RWT_blade_axis_prebend.dat', planform_nC=2)

    # load the planform file
    top.blade_length = 86.366
    top.span_ni = 50

    print 'planform variables: ', top.pf_splines.pfOut.list_vars()
    print top.pf_splines.pfOut.s

    b = top.blade_surface

    # distribute 200 points evenly along the airfoil sections
    b.chord_ni = 200

    # load the airfoil shapes defining the blade
    for f in [home+'/git/BISDEM/data/ffaw3241.dat',
              home+'/git/BISDEM/data/ffaw3301.dat']:

        b.base_airfoils.append(np.loadtxt(f))

    b.blend_var = np.array([0.5, 1.])

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

    return top
