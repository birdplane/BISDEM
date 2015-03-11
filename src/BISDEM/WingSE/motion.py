import numpy as np
import matplotlib.pyplot as plt

from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float,VarTree

from BISDEM.lib.vartrees import WingDefVT, WingPosVT, MechPosVT
from BISDEM.lib.geo import triangle


class wing_motion(Component):
    
    """
    
    1. Calculates wing position according to given mechanism motion and wing definition (wingpos)
    
    2. Calculates velocity over wingspan with given discretization for an equivalent spar
    
    
    """
    
    # Inputs
    wdef = VarTree(WingDefVT(), iotype='in', desc='Wing definition')
    mpos = VarTree(MechPosVT(), iotype='in', desc='Mech position')
    
    # Outputs
    wpos = VarTree(WingPosVT(), iotype='out', desc='Wing position')
    Dymax = Float(iotype='out', desc='Highest wing tip location')
    AD = Float(iotype='out', desc='Area encirceld by D')

    def execute(self):
        
        # hand over interface hinge positions from mechanism
        self.wpos.front.A = self.mpos.front.A
        self.wpos.back.A = self.mpos.back.A
        self.wpos.front.O = self.mpos.front.O
        self.wpos.back.O = self.mpos.back.O
        
        self.wingpos()
        
        self.Dymax = np.max(self.wpos.front.D[1])
        
    def wingpos(self):
        
        """
        
        Calculates wing position according to given mechanism motion and wing definition
        
        """
        
        for sdef, spos, A, B, O in zip([self.wdef.front, self.wdef.back],[self.wpos.front,self.wpos.back], [self.mpos.front.A, self.mpos.back.A],[self.mpos.front.B, self.mpos.back.B],[self.mpos.front.O, self.mpos.back.O]):
        
            OA = np.mean(np.linalg.norm((A[0:2]-O[0:2]), axis=0))
            OB = np.mean(np.linalg.norm((B[0:2]-O[0:2]), axis=0))
            
            Cx = O[0] + (O[0]-B[0]) / OB * sdef.OC
            Cy = O[1] + (O[1]-B[1]) / OB * sdef.OC
            Cz = O[2]
            spos.C = np.array([Cx, Cy, Cz])
            
            E1 , E2 = triangle(A,spos.C,sdef.EC,sdef.AE,np.linalg.norm(spos.C[0:2]-A[0:2],axis=0))
            spos.E = E1
                        
            D1, D2 = triangle(spos.E,spos.C,sdef.CD,sdef.ED,sdef.EC)
            spos.D = D1

            

    
