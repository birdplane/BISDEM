import numpy as np
import matplotlib.pyplot as plt

from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float,VarTree

from BISDEM.lib.vartrees import WingPosVT, WingSpdVT
from BISDEM.lib.geo import triangle

class wing_speed(Component):
    
    # Inputs
    wpos = VarTree(WingPosVT(), iotype='in', desc='Wing position')
    dt = Float(iotype='in', desc='Timestep')
        
    # Outputs
    wspd = VarTree(WingSpdVT(), iotype='out', desc='Wing speeds')
    
    def execute(self):
        for spos, sspd in zip([self.wpos.front, self.wpos.back], [self.wspd.front, self.wspd.back]):
            dt=self.dt
            
            C=spos.C
            C_1=C[:,0:-1]
            C_2=C[:,1:]
            sspd.C=(C_2-C_1)/dt
                                    
            D=spos.D
            D_1=D[:,0:-1]
            D_2=D[:,1:]
            sspd.D=(D_2-D_1)/dt
                  