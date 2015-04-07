
from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float,Array

from BISDEM.lib.geo import rotx, roty, rotz

import matplotlib.pyplot as plt
import numpy as np

# Make sure that your class has some kind of docstring. Otherwise
# the descriptions for your variables won't show up in the
# source ducumentation.

class BEM(Component):
    """
    """
    # Input
    P_1 = Array(iotype='in', desc='Element positions over time')
    V0_1 = Array(iotype='in', desc='Flight velocity vector')
    Vflap_1 = Array(iotype='in', desc='Velocity induced through flapping')
    J_a = Float(iotype='in', desc='hinge element number')
    Twist = Array(iotype='in', desc='twist distribution over time')
    Pitch = Array(iotype='in', desc='pitch distribution')
    Chord = Array(iotype='in', desc='chord distribution')
    PLE = Array(iotype='in', desc='distance from leading edge to axis')
    Polar = Array(iotype='in', desc='polar matrix')
    rho = Float(iotype='in', desc='air density')
    dt = Float(iotype='in', desc='time step')
    
    # declare inputs and outputs here, for example:
    F_1 = Array(iotype='out', desc='force vector')
    M_1 = Array(iotype='out', desc='moment')

    

    def execute(self):

        Vi_1 = np.array([0,0,0])
         
        self.F_1 = bet(self.P_1,self.V0_1,Vi_1,self.Vflap_1,self.J_a,self.Twist,self.Pitch,self.Chord,self.PLE,self.Polar,self.rho,self.dt)
        
#        meanF_1 = np.array([np.sum(self.F_1[:,:,0]),np.sum(self.F_1[:,:,1]),np.sum(self.F_1[:,:,2])])/ len(self.F_1)
#        print mt(self.P_1,self.V0_1,meanF_1,self.rho)

#         while True:
#                 
#                 
#             self.F_1 = bet(self.P_1,self.V0_1,Vi_1,self.Vflap_1,self.J_a,self.Twist,self.Pitch,self.Chord,self.PLE,self.Polar,self.rho,self.dt)
#             meanF_1 = np.array([np.sum(self.F_1[:,:,0]),np.sum(self.F_1[:,:,1]),np.sum(self.F_1[:,:,2])])/ len(self.F_1)
#                 
#             print 'induced velocity: %f' %Vi_1[0], Vi_1[1], Vi_1[2]
#             print 'mean force magnitude: %f' %meanF_1[0],meanF_1[1],meanF_1[2]
#     
#             Vi_1new = mt(self.P_1,self.V0_1,meanF_1,self.rho)
#                  
#             if np.linalg.norm(Vi_1new-Vi_1)<0.0001:
#                 break
#                  
#             Vi_1 = Vi_1new
        
    
    
def bet(P_1,V0_1,Vi_1,Vflap_1,J_a,Twist,Pitch,Chord,PLE,Polar,rho,dt):
    
    """ Blade Element Theory according to B. Parslew
    
    in general for state matrices:
    i - moment in time, where 0 is the first moment and end the last moment in time
    j - blade element, where 0 is the shoulder hinge-element and end is the wing tip-element
    k - vector component, where 0 is the x-, 1 the y- and 2 the z-component
        
    """
    Phi = np.zeros_like(Twist)
    V_4 = np.zeros_like(P_1)
    dV_4 = np.zeros_like(P_1)
    F_5 = np.zeros_like(P_1)
    F_4 = np.zeros_like(P_1)
    F_1 = np.zeros_like(P_1)
    l = np.zeros_like(Twist)
    d = np.zeros_like(Twist)
    m = np.zeros_like(Twist)
    aoa = np.zeros_like(Twist)
    daoa = np.zeros_like(Twist)
    cl = np.zeros_like(Twist)
    cd = np.zeros_like(Twist)
    cm = np.zeros_like(Twist)
    w = np.zeros_like(Chord)
    wy = np.zeros_like(Twist)
    S = np.zeros_like(Twist)
    
    Vflap_1[np.abs(Vflap_1) < 1e-8] = 0
    
    for i in range(len(P_1)):
        
        for j in range(len(P_1[i])):
            
            # Calculate wing element elevation angle
    
            if j <= J_a:
                
                dz = P_1[i,J_a,2]
                dy = P_1[i,J_a,1]

                Phi[i,j] = np.arctan(dz/dy)
                
            else:
                
                dz = P_1[i,-1,2]-P_1[i,J_a+1,2]
                dy = P_1[i,-1,1]-P_1[i,J_a+1,1]
                
                Phi[i,j] = np.arctan(dz/dy)
                
            # Calculate local flow velocity
            V_4[i,j] = roty((Twist[i,j]+Pitch[j]), rotx(-Phi[i,j],(V0_1 + Vi_1 + Vflap_1[i,j]))) 
            V_4[np.abs(V_4) < 1e-12] = 0

            # Calculate angle of attack
            aoa[i,j] = np.arctan(-V_4[i,j,2]/V_4[i,j,0])

            # Find cl,cd,cm from polars with linear interpolation
            cl[i,j] = np.interp(np.degrees(aoa[i,j]),Polar[j,0],Polar[j,1])
            cd[i,j] = np.interp(np.degrees(aoa[i,j]),Polar[j,0],Polar[j,2])
            cm[i,j] = np.interp(np.degrees(aoa[i,j]),Polar[j,0],Polar[j,3])

            # Calculate element width
            if j < len(P_1[i])-1:
                wy[i,j] = P_1[i,j+1,1]-P_1[i,j,1]
            else:
                wy[i,j] = P_1[i,j,1]-P_1[i,j-1,1]
    
            # Calculate element surface area
            S[i,j] = Chord[j] * wy[i,j]
            
            # Calculate aerodynamic forces
            l[i,j] = 0.5 * rho * np.linalg.norm(V_4[i,j])**2 * S[i,j] * cl[i,j]
            d[i,j] = 0.5 * rho * np.linalg.norm(V_4[i,j])**2 * S[i,j] * cd[i,j]
            m[i,j] = 0.5 * rho * np.linalg.norm(V_4[i,j])**2 * S[i,j] * cm[i,j]
            
            # Force vector in Blade Element local axes
            F_5[i,j] = np.array([-d[i,j], 0, l[i,j]])
                
            # Force vector in Blade local axes
            F_4[i,j] = roty(aoa[i,j],F_5[i,j])
            
    
    
    """
    Add mass effect and rotate to stroke plane axes
    """
    for i in range(len(P_1)):
         
        for j in range(len(P_1[i])):
            # Add mass effects
            if i==0:
                daoa[i,j] = (aoa[1,j]-aoa[0,j])/dt
                dV_4[i,j] = (V_4[1,j]-V_4[0,j])/dt
    
            elif i < len(P_1)-1:
                daoa[i,j] = (aoa[i+1,j]-aoa[i-1,j])/(2*dt)
                dV_4[i,j] = (V_4[i+1,j]-V_4[i-1,j])/(2*dt)
                 
            else:
                daoa[i,j] = (aoa[i,j]-aoa[i-1,j])/dt
                dV_4[i,j] = (V_4[i,j]-V_4[i-1,j])/dt
                    
 
            F_4[i,j,0] = F_4[i,j,0] - 0.25 * rho * np.pi * Chord[j] * S[i,j] * V_4[i,j,2] * daoa[i,j]
            F_4[i,j,2] = F_4[i,j,2] + 0.25 * rho * np.pi * Chord[j] * S[i,j] * dV_4[i,j,2]
             
            # Tranform to Stroke Plane Axes
            F_1[i,j] = rotx(Phi[i,j],roty(-(Twist[i,j]+Pitch[j]),F_4[i,j]))

    return F_1
            
def mt(P_1,V0_1,meanF_1,rho):            
    """ Momentum Theory according to B. Parslew
    
    in general for state matrices:
    i - moment in time, where 0 is the first moment and end the last moment in time
    j - blade element, where 0 is the shoulder hinge-element and end is the wing tip-element
    k - vector component, where 0 is the x-, 1 the y- and 2 the z-component
        
    """            
    psi = np.arctan2(V0_1[2],-V0_1[0])
    
    # Find swept ares
    idx_zmax = np.argmax(P_1[:,-1,2])
    idx_ymax = np.argmax(P_1[:,-1,1])
    idx_zmin = np.argmin(P_1[:,-1,2])
    
    Ad = np.linalg.norm(P_1[idx_zmax,-1,2]-P_1[idx_zmin,-1,2])*P_1[idx_ymax,-1,1]
    print P_1[idx_zmax,-1,2]
    V0 = np.linalg.norm(V0_1)
    
    Vi_1new = np.zeros_like(V0_1,dtype=float)

    while True:
        Vi_1 = Vi_1new
        
        Vi_1new[0] = meanF_1[0] / (2 * rho * Ad * np.sqrt(   (V0*np.cos(psi)+Vi_1[0])**2  +   (-V0*np.sin(psi)+Vi_1[2])**2 )) 
        Vi_1new[2] = meanF_1[2] / (2 * rho * Ad * np.sqrt(   (V0*np.cos(psi)+Vi_1[0])**2  +   (-V0*np.sin(psi)+Vi_1[2])**2 )) 
    
        if np.linalg.norm(Vi_1-Vi_1new) < 0.001:
            break

    return -Vi_1 
    
            