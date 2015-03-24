import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

from BISDEM.WingSE.wingsurface import WingSurface
from BISDEM.lib.vartrees import WingPlanformVT

from BISDEM.lib.plot import mechanimation2D, mechplot2D

from BISDEM.MechSE.init import mech_init
from BISDEM.MechSE.motion import mech_motion

from BISDEM.WingSE.init import wing_init
from BISDEM.WingSE.motion import wing_motion

from os.path import expanduser
home = expanduser("~")

"""
Example for how to define mechanism and wing and run and visualize the behavior for given conditions

"""

"""
Define mechanism
"""
MechInit = mech_init()

MechInit.fGx = MechInit.bGx = -16e-3
MechInit.fGy = MechInit.bGy = -70e-3
MechInit.fRi = MechInit.bRi = 8.5e-3
MechInit.fRo = MechInit.bRo = 24e-3
MechInit.fQB = MechInit.bQB = 67e-3
MechInit.fPA = MechInit.bPA = 65e-3
MechInit.ftheta_del = MechInit.btheta_del = np.radians(60)
MechInit.fBO = MechInit.bBO = 45e-3
MechInit.fAO = MechInit.bAO = 20e-3

MechInit.fz = 0
MechInit.bz = -100e-3

MechInit.run()      # Run defintion. Afterwards, mdef is filled.


"""
Calculate mechanism motion
"""
MechMotion = mech_motion()

MechMotion.mdef = MechInit.mdef
 
# Define running parameters
theta = np.linspace(0, 2*np.pi, 200)
phi = np.ones(len(theta)) * np.radians(15)
 
MechMotion.phi = phi
MechMotion.theta = theta
 
MechMotion.run()


"""
Define Wing
"""
WingInit = wing_init()

WingInit.fAE = WingInit.bAE = 0.294
WingInit.fEC = WingInit.bEC = 0.02
WingInit.fOC = WingInit.bOC = 0.294
WingInit.fCD = WingInit.bCD = 0.3825
WingInit.fED = WingInit.bED = 0.364
WingInit.fz = 0.
WingInit.bz = MechInit.bz

WingInit.run()


"""
Calculate wing motion
"""
WingMotion = wing_motion()

# Hand over definition and positions of mechanism
WingMotion.wdef = WingInit.wdef
WingMotion.mpos = MechMotion.mpos 
WingMotion.n = 30
WingMotion.dt = 0.001

WingMotion.run()

#mechanimation2D(MechMotion.mpos.front,WingMotion.wpos.front, 20)
#mechplot2D(MechMotion.mpos,WingMotion.wpos,2)   

surface = WingSurface()
surface.eqspar_geom = WingMotion.wpos.eqspar_geom
planform = WingPlanformVT();
planform.blade_length = .2;
planform.chord = np.ones(30)
planform.rthick =  np.ones(30)*0.05
planform.p_le = np.zeros(30)
surface.planform_in = [planform]*len(WingMotion.wpos.eqspar_geom);

surface.airfoils = [home+'/git/BISDEM/data/ffaw3241.dat', home+'/git/BISDEM/data/ffaw3301.dat'];
surface.span_ni = 30

surface.run()
surf = surface.wingsurf
b = surf.blade_surface
surf.run()

pf = surf.pf_splines.pfOut

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_aspect('equal')
MAX = 1.2
for direction in (-1, 1):
    for point in np.diag(direction * MAX * np.array([1,1,1])):
        ax.plot([point[0]], [point[1]], [point[2]], 'w')
for i in range(b.span_ni):
    ax.plot(b.surfout.surface[:, i, 0], b.surfout.surface[:, i, 1], b.surfout.surface[:, i, 2])
plt.show()
plt.figure()
plt.axis('equal')
plt.xlim(-1.2, 1.2)
plt.ylim(-1.2, 1.2)
for i in range(b.span_ni):
    plt.plot(b.surfout.surface[:, i, 0], b.surfout.surface[:, i, 1])
plt.show()
plt.figure()
plt.axis('equal')
plt.xlim(-1.2, 1.2)
plt.ylim(-1.2, 1.2)
for i in range(b.span_ni):
    plt.plot(b.surfout.surface[:, i, 2], b.surfout.surface[:, i, 0])
plt.show()
plt.figure()
plt.axis('equal')
plt.xlim(-1.2, 1.2)
plt.ylim(-1.2, 1.2)
for i in range(b.span_ni):
    plt.plot(b.surfout.surface[:, i, 2], b.surfout.surface[:, i, 1])
plt.show()

