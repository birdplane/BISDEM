import numpy as np

from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Array, VarTree

from BISDEM.lib.vartrees import MechDefVT, MechPosVT
from BISDEM.lib.geo import triangle

class mech_motion(Component):
    
    """
    
    Calculates positions of points A,B,P,Q based on mechanism definition for given set of theta and phi
    
    """
    
    # Inputs
    mdef = VarTree(MechDefVT(), iotype='in', desc='Mechanism definition')
    theta = Array(iotype='in', desc='Array with angular positions of outer front gear mount')
    phi = Array(iotype='in', desc='Array with phase lag of rear leg compared to front leg')
    
    # Outputs
    mpos = VarTree(MechPosVT(), iotype='out', desc='Mechanism description')

    def execute(self):
        """ do your calculations here """

        
        for ldef, lpos, phi in zip([self.mdef.front, self.mdef.back],[self.mpos.front,self.mpos.back], [np.zeros(len(self.theta)), self.phi]):
                
            # Position of origin hinge
            O_x = np.zeros(len(self.theta))
            O_y = np.zeros(len(self.theta))
            O_z = np.ones(len(self.theta)) * ldef.z
            
            lpos.O = np.array([O_x, O_y, O_z])
                
                
            # Position of outer gear mount
            Q_x = ldef.G[0] + ldef.Ro * np.cos(self.theta - phi)
            Q_y = ldef.G[1] + ldef.Ro * np.sin(self.theta - phi)
            Q_z = ldef.z * np.ones(len(self.theta))
            
            lpos.Q = np.array([Q_x, Q_y, Q_z])
                      
                      
            # Position of inner gear mount
            P_x = ldef.G[0] + ldef.Ri * np.cos(self.theta + ldef.theta_del - phi)
            P_y = ldef.G[1] + ldef.Ri * np.sin(self.theta + ldef.theta_del - phi)
            P_z = ldef.z * np.ones(len(self.theta))
            
            lpos.P = np.array([P_x, P_y, P_z])
            
            
            # Position of point A
            lpos.A,dum = triangle(lpos.P,lpos.O,ldef.AO,ldef.PA,np.linalg.norm(lpos.P[0:2],axis=0))
              
              
            # Position of point B
            dum,lpos.B = triangle(lpos.Q,lpos.O,ldef.BO,ldef.QB,np.linalg.norm(lpos.Q[0:2],axis=0))

            

            