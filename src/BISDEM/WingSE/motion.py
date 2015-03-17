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
    dt = Float(iotype='in', desc='Timestep')
    
    # Outputs
    wpos = VarTree(WingPosVT(), iotype='out', desc='Position of the points O, A, C, D, E for each time step')
    wspeed = VarTree(WingSpdVT(), iotype='out', desc='Wing speeds')
    wtwist = VarTree(WingPhlVT(), iotype='out', desc='Wing speeds')
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

    def wingspeed(self):
        """
        Calculates the wing speeds of all wing segments
        """
        for spos, sspd in zip([self.wpos.front, self.wpos.back], [self.wspd.front, self.wspd.back]):
            
            C=spos.C
            C_1=C[:,0:-1]
            C_2=C[:,1:]
            sspd.C=(C_2-C_1)/self.dt
                                    
            D=spos.D
            D_1=D[:,0:-1]
            D_2=D[:,1:]
            sspd.D=(D_2-D_1)/self.dt
            
    def wingtwist(self):
        """
        Calculates the wing twist of all wing segments
        """
        dyc = self.wpos.front.C[1]-self.wpos.back.C[1]
        self.wtwist.C = np.arctan(dyc/self.bz)
        
        dyd = self.wpos.front.D[1]-self.wpos.back.D[1]
        self.wtwist.D = np.arctan(dyd/self.bz)