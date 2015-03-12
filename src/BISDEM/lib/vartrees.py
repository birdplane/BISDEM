"""
Collection of all VarTrees
"""

from openmdao.main.api import VariableTree
from openmdao.lib.datatypes.api import Float, VarTree, Array

# Mechanism VarTrees

class MechLegDefVT(VariableTree):
    
    """
    
    Carries definition of a single (front or back) mechanism leg.
    
    """
    
    G = Array(units='m',  desc='gear center xyz position')
    theta_del = Float(units='rad',  desc='phase difference between inner and outer gear mount (counter clockwise positive)')
    Ri = Float(units='m',  desc='inner gear radius')
    Ro = Float(units='m',  desc='outer gear radius')
    
    QB = Float(units='m',  desc='length of rod between outer gear mount and point B')
    PA = Float(units='m',  desc='length of rod between inner gear mount and point A')
    BO = Float(units='m',  desc='length of rod between point B and point O')
    AO = Float(units='m',  desc='length of rod between point A and point O')
    
    z =  Float(units='m',  desc='z coordinate defining the back mechanism leg plane x-y plane')
    
class MechDefVT(VariableTree):
    
    """
    
    Consists of the definitions of both mechanism legs
    
    """
    
    front = VarTree(MechLegDefVT(),  desc='front leg definition')
    bach = VarTree(MechLegDefVT(),  desc='back leg definition')

    
class MechLegPosVT(VariableTree):
    
    """
    
    Carries the hinge position information of one mechanism leg over time.
    
    Explanation:
        
    P[i,j]: i stands for the time step and j for x (0), y (1) or z (2) coordinate
    
    Example: 
    In order to find the xyz-position of point A after 3 time steps:
    
    A_x = A[3,0]
    A_y = A[3,1]
    A_z = A[3,2]
    
    """
    
    O = Array(units='m',  desc='point O xyz position over time')  
    A = Array(units='m',  desc='point A xyz position over time')    
    B = Array(units='m',  desc='point B xyz position over time') 
    P = Array(units='m',  desc='inner gear mount point P x,y,z position over time')
    Q = Array(units='m',  desc='outer gear mount point Po x,y,z position over time') 
    
class MechPosVT(VariableTree):
    
    """
    
    Carries the position information of both mechanisms.
    
    """
    
    front = VarTree(MechLegPosVT(),  desc='front leg posotions')
    back = VarTree(MechLegPosVT(),  desc='back leg positions')
    
# Wing VarTrees
    
class SparDefVT(VariableTree):
    
    """
    
    Carries definition of a single (front or back) wing spar.
   
    """
    
    # Spar definition
    
    AE = Float(units='m',  desc='length of rod between point A and point E')
    EC = Float(units='m',  desc='length of rod between point E and point C')
    OC = Float(units='m',  desc='length of rod between point O and point C')
    CD = Float(units='m',  desc='length of rod between point C and point D')
    ED = Float(units='m',  desc='distance between point E and point D')
    
    z = Float(units='m',  desc='z coordinate defining the spar plane x-y plane')
    
class WingDefVT(VariableTree):
    
    """
    
    Carries definition of both wing spars.
   
    """
    
    front = VarTree(SparDefVT(),  desc='front spar definition')
    back = VarTree(SparDefVT(),  desc='back spar definition')

class SparPosVT(VariableTree):
    
    """
    
    Carries the hinge position information of one wing spar over time.
    
    Explanation:
        
    P[i,j]: i stands for the time step and j for x (0), y (1) or z (2) coordinate
    
    Example: 
    In order to find the xyz-position of point A after 3 time steps:
    
    A_x = A[3,0]
    A_y = A[3,1]
    A_z = A[3,2]
    
    """
    
    O = Array(units='m',  desc='point O xyz position over time')
    A = Array(units='m',  desc='point A xyz position over time')  
    C = Array(units='m',  desc='point C xyz position over time')  
    D = Array(units='m',  desc='point D xyz position over time')  
    E = Array(units='m',  desc='point E xyz position over time')  
    
    
class WingPosVT(VariableTree):
    
    """
    
    Carries the position information of both wing spars.
    
    """
      
    front = VarTree(SparPosVT(),  desc='front spar positon over time')
    back = VarTree(SparPosVT(),  desc='back spar position over time')
    
    
class SparSpdVT(VariableTree):
    
    C = Array(units='m',  desc='point C speeds over time')
    D = Array(units='m',  desc='point C speeds over time')
    
class WingSpdVT(VariableTree):
    
    """
    
    Carries the speed of positions on the wing
    
    """
      
    front = VarTree(SparSpdVT(),  desc='front spar positon over time')
    back = VarTree(SparSpdVT(),  desc='back spar position over time')
    
class WingPhlVT(VariableTree):
    
    C = Array(units='m',  desc='point C speeds over time')
    D = Array(units='m',  desc='point C speeds over time')