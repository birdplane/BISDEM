
from openmdao.main.api import Component, Assembly
from openmdao.lib.datatypes.api import Float, List, Slot, File, Instance
from fusedwind.turbine.geometry_vt import BeamGeometryVT, BladePlanformVT


class WingSurface(Component):
    """
    This class carries a full description of the wing surface at any time-step. 
    The definition is based of the fusedwind framework definitions. http://www.fusedwind.org
    """
    
    # Inputs
    eqspar_geom = List(BeamGeometryVT(), iotype='in', desc='Position and twist of the equivalent(discrete) beam of the wing, fusedwind definition'
                          'per timestep, type is BeamGeometryVT')
    eqspar_pf = List(BladePlanformVT(), iotype='in', desc='Wing planform definition along beam(discrete), needs to be same length'
                      'as eqspar_geom, also per time step. Type is BeamPlanformVT')
    airfoil = List(File(), iotype="in", desc='List of airfoil description files')
    
    # Outputs
    wingsurf = Instance(Assembly, iotype="out", desc="Complete 3D descrpition of the wing surface")
    
    def execute(self):
        """ Calculate the wingsurface from the spar geometry """
        
        print self.eqspar_geom[0].x
        
