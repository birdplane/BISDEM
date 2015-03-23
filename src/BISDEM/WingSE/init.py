
from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float, VarTree

from BISDEM.lib.vartrees import SparDefVT, WingDefVT, MechPosVT
from docutils import frontend


# Make sure that your class has some kind of docstring. Otherwise
# the descriptions for your variables won't show up in the
# source ducumentation.
class wing_init(Component):
    """ 
    
    Initializes/ defines wing:
    1. Sorts all geometrical input parameters in WingDef VarTree 
    
    """
    # declare inputs and outputs here, for example:
    fAE = Float(iotype='in', desc='front spar: distance between point A and E')
    fEC = Float(iotype='in', desc='front spar: distance between point E and C')
    fOC = Float(iotype='in', desc='front spar: distance between point O and C')
    fCD = Float(iotype='in', desc='front spar: distance between point C and D')
    fED = Float(iotype='in', desc='front spar: distance between point E and D')
    fz = Float(iotype='in', desc='front spar: z position')
    
    bAE = Float(iotype='in', desc='back spar: distance between point A and E')
    bEC = Float(iotype='in', desc='back spar: distance between point E and C')
    bOC = Float(iotype='in', desc='back spar: distance between point O and C')
    bCD = Float(iotype='in', desc='back spar: distance between point C and D')
    bED = Float( iotype='in', desc='back spar: distance between point E and D')
    bz = Float(iotype='in', desc='back spar: z position')

    nS = Float(iotype='in', desc='Number of wing sections')
    mpos = VarTree(MechPosVT(), iotype='in', desc='Mech position')
    
    wdef = VarTree(WingDefVT(), iotype='out', desc='wing definition')

    def execute(self):
        
        front = SparDefVT()
        
        front.AE = self.fAE 
        front.EC = self.fEC
        front.OC = self.fOC
        front.CD = self.fCD
        front.ED = self.fED
        front.z = self.fz
        
        back = SparDefVT()
        
        back.AE = self.bAE 
        back.EC = self.bEC
        back.OC = self.bOC
        back.CD = self.bCD
        back.ED = self.bED
        front.z = self.bz
        
        wdef = WingDefVT()
        wdef.front = front
        wdef.back = back
        
        self.wdef = wdef
