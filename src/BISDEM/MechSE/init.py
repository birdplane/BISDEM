import numpy as np

from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float, VarTree

from BISDEM.lib.vartrees import MechLegDefVT, MechDefVT

class mech_init(Component):
    """ 
    
    Initializes/ defines mechanism:
    1. Sorts all geometrical input parameters in MechDef VarTree 
    
    """
    
    # Inputs:
    fGx = Float(iotype='in', desc='front leg: gear x-position')
    fGy = Float(iotype='in', desc='front leg: gear y-position')
    fRi = Float(iotype='in', desc='front leg: gear inner radius')
    fRo = Float(iotype='in', desc='front leg: gear outer radius')
    fQB = Float(iotype='in', desc='front leg: length of rod between outer gear mount and point B')
    fPA = Float(iotype='in', desc='front leg: length of rod between inner gear mount and point A')
    ftheta_del = Float(iotype='in', desc='front leg: phase difference (inner gear theta - outer gear theta)')
    fBO = Float(iotype='in', desc='front leg: length of rod between point B and O')
    fAO = Float(iotype='in', desc='front leg: length of rod between point A and O')
    fz = Float(iotype='in', desc='front leg: z-position') 
    
    bGx = Float(iotype='in', desc='back leg: gear x-position')
    bGy = Float(iotype='in', desc='back leg: gear y-position')
    bRi = Float(iotype='in', desc='back leg: gear inner radius')
    bRo = Float(iotype='in', desc='back leg: gear outer radius')
    bQB = Float(iotype='in', desc='back leg: length of rod between outer gear mount Q and point B')
    bPA = Float(iotype='in', desc='back leg: length of rod between inner gear mount P and point A')
    btheta_del = Float(iotype='in', desc='back leg: phase difference between inner and outer gear mount')
    bBO = Float(iotype='in', desc='back leg: length of rod between point B and O')
    bAO = Float(iotype='in', desc='back leg: length of rod between point A and O')
    bz = Float(iotype='in', desc='back leg: z-position')
    
    # Output    
    mdef = VarTree(MechDefVT(), iotype='out', desc='mechanism definition definition')
    
    
    def execute(self):
        
        # define front mechanism leg
        
        front = MechLegDefVT()
        
        front.z =  self.fz    # front leg is always in xy origin plane
        
        fG = np.array([self.fGx, self.fGy, front.z])
        front.G = fG
        front.theta_del = self.ftheta_del
        front.Ri = self.fRi
        front.Ro = self.fRo
        
        front.QB = self.fQB
        front.PA = self.fPA
        front.BO = self.fBO
        front.AO = self.fAO
        
        
        
        # define back mechanism leg
        
        back = MechLegDefVT()
        
        back.z =  self.bz
        
        bG = np.array([self.bGx, self.bGy, back.z])
        back.G = bG
        back.theta_del = self.btheta_del
        back.Ri = self.bRi
        back.Ro = self.bRo
        
        back.QB = self.bQB
        back.PA = self.bPA
        back.BO = self.bBO
        back.AO = self.bAO
        

        
        # safe in 

        self.mdef.front = front 
        self.mdef.back = back
        
