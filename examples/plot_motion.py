import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from BISDEM.lib.plot import mechanimation2D, mechplot2D

from BISDEM.MechSE.init import mech_init
from BISDEM.MechSE.motion import mech_motion

from BISDEM.WingSE.init import wing_init
from BISDEM.WingSE.motion import wing_motion

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
MechInit.bz = -65e-3

MechInit.run()      # Run defintion. Afterwards, mdef is filled.


"""
Calculate mechanism motion
"""
MechMotion = mech_motion()

MechMotion.mdef = MechInit.mdef
 
# Define running parameters
dt = 0.01
f = 2.   #Hz
T = 1. / f

theta = np.linspace(0,2*np.pi, 200)
phi = np.ones(len(theta)) * np.radians(0)
 
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

WingMotion.run()

mechanimation2D(MechMotion.mpos.front,WingMotion.wpos.front, 20)
mechplot2D(MechMotion.mpos,WingMotion.wpos,2)   
