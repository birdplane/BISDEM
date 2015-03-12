import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from BISDEM.lib.plot import mechanimation2D, mechplot2D

from BISDEM.MechSE.init import mech_init
from BISDEM.MechSE.motion import mech_motion

from BISDEM.WingSE.init import wing_init
from BISDEM.WingSE.motion import wing_motion
from BISDEM.WingSE.speeds import wing_speed
from BISDEM.WingSE.twist import wing_twist

"""
Example for how to define mechanism and wing and run and visualize the behavior for given conditions

"""

"""
Define mechanism
"""
MechInit = mech_init()

MechInit.fGx = MechInit.bGx = -16e-3
MechInit.fGy = MechInit.bGy = -70e-3
MechInit.fRi = MechInit.bRi = 9e-3
MechInit.fRo = MechInit.bRo = 25e-3
MechInit.fQB = MechInit.bQB = 65e-3
MechInit.fPA = MechInit.bPA = 65e-3
MechInit.ftheta_del = MechInit.btheta_del = np.radians(60)
MechInit.fBO = MechInit.bBO = 45e-3
MechInit.fAO = MechInit.bAO = 16e-3

MechInit.fz = 0
MechInit.bz = -30e-3

MechInit.run()      # Run defintion. Afterwards, mdef is filled.


"""
Calculate mechanism motion
"""
MechMotion = mech_motion()

MechMotion.mdef = MechInit.mdef
 
# Define running parameters
f= 5 #Hz flapping frequency
T= 1./f # s flapping period
dt= 0.001 # the timestep


numsteps = T/dt #the number of points that will be evaluated
tsteps = np.linspace(0,T,numsteps+1)
tsteps = tsteps[0:-1]
omega = np.ones(numsteps)*f*2*np.pi # angular velocity (nof for constant rotational speed)
theta = tsteps*omega
phi = np.ones(len(theta)) * np.radians(-10)

MechMotion.phi = phi
MechMotion.theta = theta
MechMotion.run()


"""
Define Wing
"""
WingInit = wing_init()

WingInit.fAE = WingInit.bAE = 0.235
WingInit.fEC = WingInit.bEC = 0.016
WingInit.fOC = WingInit.bOC = 0.235
WingInit.fCD = WingInit.bCD = 0.470
WingInit.fED = WingInit.bED = 0.455
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



"""
Calculate the speed of point C and D
"""

WingSpeed = wing_speed()

WingSpeed.wpos= WingMotion.wpos
WingSpeed.dt=dt

WingSpeed.run()

plt.plot(theta[0:-1],WingSpeed.wspd.front.C[1],'r--',theta[0:-1],WingSpeed.wspd.front.D[1],'b--')
plt.show()


"""
Calculate wing twist angle from phaselag
"""

WingTwist = wing_twist()

WingTwist.wpos = WingMotion.wpos
WingTwist.bz = MechInit.bz

WingTwist.run()

plt.figure(2)
plt.plot(theta,WingTwist.wtwist.C,'r--',theta,WingTwist.wtwist.D,'b--')
plt.show()