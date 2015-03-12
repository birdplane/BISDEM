import numpy as np
import matplotlib.pyplot as plt

from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float,VarTree

from BISDEM.lib.vartrees import WingPosVT, WingSpdVT, WingPhlVT
from BISDEM.lib.geo import triangle

class wing_twist(Component):
    
    # Inputs
    wpos = VarTree(WingPosVT(), iotype='in', desc='Wing position')
    bz = Float(iotype='in', desc='back leg: z-position')
        
    # Outputs
    wtwist = VarTree(WingPhlVT(), iotype='out', desc='Wing speeds')
    
    def execute(self):
        
        dyc = self.wpos.front.C[1]-self.wpos.back.C[1]
        self.wtwist.C = np.arctan(dyc/self.bz)
        
        dyd = self.wpos.front.D[1]-self.wpos.back.D[1]
        self.wtwist.D = np.arctan(dyd/self.bz)
        