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

MechInit.fGx = MechInit.bGx = -15e-3
MechInit.fGy = MechInit.bGy = -70e-3
MechInit.fRi = MechInit.bRi = 8.5e-3
MechInit.fRo = MechInit.bRo = 24e-3
MechInit.fQB = MechInit.bQB = 67e-3
MechInit.fPA = MechInit.bPA = 65e-3
MechInit.ftheta_del = MechInit.btheta_del = np.radians(60)
MechInit.fBO = MechInit.bBO = 45e-3
MechInit.fAO = MechInit.bAO = 20e-3

MechInit.fz = 0
MechInit.bz = -48.5e-3

MechInit.run()      # Run defintion. Afterwards, mdef is filled.


"""
Calculate mechanism motion
"""
MechMotion = mech_motion()

MechMotion.mdef = MechInit.mdef
 
# Define running parameters
theta = np.linspace(0, 2*np.pi, 200)
phi = np.ones(len(theta)) * np.deg2rad(3.3)
 
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
planform.chord = np.ones(10)*0.22
planform.chord = np.append(planform.chord, np.linspace(.220, .0860254, 20))
planform.rthick =  np.ones(30)*0.16
planform.p_le = np.zeros(30)
surface.planform_in = [planform]*len(WingMotion.wpos.eqspar_geom);

surface.airfoils = [home+'/git/BISDEM/data/ffaw3241.dat', home+'/git/BISDEM/data/ffaw3301.dat'];
surface.span_ni = 30

surface.run()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_aspect('equal')
ax.set_xlim(-0.1, 1.4)
ax.set_ylim(-0.5, 1.0)
ax.set_zlim(-0.5, 1.0)
ax.view_init(18, -133)

# Initialize 
lines = []
blades = []
for index in range(surface.wingsurf[0].blade_surface.span_ni):
    lobj = ax.plot([],[],[],"r",lw=2)[0]
    lines.append(lobj)

def init():
    
    for line in lines:
        line.set_data([],[])
        line.set_3d_properties([])
        
    for j, surf in enumerate(surface.wingsurf):
        print "\rCreating wing %d/%d" %(j, len(surface.wingsurf)),
        b = surf.blade_surface
        surf.run()
        blades.append(b)
    
    print
    print "Done initializing"
    return lines, blades

def animate(i):
    b=None
    if i>0 and i<199:
        b = blades[i]
    else:
        return
    
    for lnum,line in enumerate(lines):
        if lnum>=0 and lnum<30:
            line.set_data(b.surfout.surface[:, lnum, 2], -b.surfout.surface[:, lnum, 0])
            line.set_3d_properties(b.surfout.surface[:, lnum, 1])
        
            fig.canvas.draw()
        else:
            break
    return lines


# for j, surf in enumerate(surface.wingsurf):
#     print "\rCreating wing %d/%d" %(j, len(surface.wingsurf)),
    
surf = surface.wingsurf[0]


b = surf.blade_surface
surf.run()
for i in range(b.span_ni):
    ax.plot(b.surfout.surface[:, i, 2], -b.surfout.surface[:, i, 0], b.surfout.surface[:, i, 1])

#plt.savefig(home+'/results/%03d.png'%j)

plt.show()

plt.close()

# # Animation

# anim = animation.FuncAnimation(fig, animate, init_func=init, frames=198, interval=1, blit=False)
# anim.save(home+'/lorenz_attractor.mp4', fps=15, extra_args=['-vcodec', 'libx264'])

print "Done"