import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from BISDEM.MechSE.init import mech_init
from BISDEM.MechSE.motion import mech_motion

from BISDEM.WingSE.init import wing_init
from BISDEM.WingSE.motion import wing_motion

from BISDEM.WingSE.aeroloads import BEM

from BISDEM.lib.geo import rotx, roty, rotz

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
f = 2   #Hz
T = 1. / f

theta = np.linspace(0,2*np.pi, T/dt)
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
WingMotion.dt = dt

WingMotion.run()

"""
Define elements along equivalent axis (P_1)
"""
Nele = 100
P_1 = np.zeros((len(theta),Nele,3))
Woc = np.linspace(0,1,Nele*(WingInit.fOC/(WingInit.fCD+WingInit.fOC))+1)
Wcd = np.linspace(0,1,Nele*(WingInit.fCD/(WingInit.fCD+WingInit.fOC))+2)

for i in range(len(theta)):
    
    C = rotx(np.radians(-90),(roty(np.radians(-90),np.array([WingMotion.wpos.front.C[0,i], WingMotion.wpos.front.C[1,i], WingMotion.wpos.front.C[2,i]]))))
    D = rotx(np.radians(-90),(roty(np.radians(-90),np.array([WingMotion.wpos.front.D[0,i], WingMotion.wpos.front.D[1,i], WingMotion.wpos.front.D[2,i]]))))
    DC = D-C

    for j in range(len(Woc)-1):
        
        P_1[i,j] = Woc[j] * C
        
    J_a = j+1

    for j in range(len(Wcd)-1):

        P_1[i,j+J_a] = C + Wcd[j] * DC

#print P_1[0,:,1][0]


"""
Find speed of elements (Vflap_1)
"""        

Vflap_1 = np.zeros_like(P_1)

for i in range(len(P_1)):
    
    for j in range(len(P_1[i])):
        
        if i == 0:
            
            Vflap_1[i,j] = -(P_1[i+1,j] - P_1[i,j]) / dt
            
        elif (i < len(P_1)-1):
            
            Vflap_1[i,j] = -(P_1[i+1,j] - P_1[i-1,j]) / (2*dt)
            
        else:
            
            Vflap_1[i,j] = -(P_1[i,j] - P_1[i-1,j]) / dt

"""
Define twist
positive twist means higher aoa
"""
twist = np.ones((len(theta),Nele))*0.

"""
Define pitch
positive pitch means higher aoa
"""
pitch = np.ones(Nele)*np.radians(5)

"""
Define chord
"""
chord = np.ones(Nele)*0.25

"""
Define p_le
"""
p_le = np.ones(Nele)*0.5

"""
Define polar
"""
Naoa = 300
caoa = np.linspace(-40, 40, Naoa)

A= 1.6
B= 0#1.135
C= 0#-1.05

cl = A * np.sin(2*np.radians(caoa))
cd = B + C * np.cos(2*np.radians(caoa))
cm = np.ones_like(cl) * -0.05

elepolar = np.array([caoa,cl,cd,cm])
polar = np.zeros((Nele,4,Naoa))

for i in range(Nele):
    
    polar[i] = elepolar
    
"""
Define free stream velocity
"""
V0_1 = np.array([-10,0,0])

# plt.figure(0)         
# plt.plot(range(len(P_1[0])),P_1[0,:,2])
# plt.plot(range(len(P_1[0])),P_1[1,:,2])
# plt.plot(range(len(P_1[0])),P_1[2,:,2])
# #plt.axis('equal')
# 
# plt.figure(1)
# plt.plot(range(len(P_1[0])),Vflap_1[0,:,2])
# plt.plot(range(len(P_1[0])),Vflap_1[1,:,2])
# plt.show()

bem = BEM()
bem.P_1 = P_1
bem.V0_1 = V0_1
bem.Vflap_1 = Vflap_1
bem.J_a = J_a
bem.Twist = twist
bem.Pitch = pitch
bem.Chord = chord
bem.PLE = p_le
bem.Polar = polar
bem.rho = 1.225
bem.dt = dt

bem.run()
F_1 = bem.F_1
F_mean = np.array([np.sum(F_1[:,:,0]),np.sum(F_1[:,:,1]),np.sum(F_1[:,:,2])])/(T/dt)

print F_mean

     
     