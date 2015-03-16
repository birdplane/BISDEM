
from openmdao.main.api import Component, Assembly
from openmdao.lib.datatypes.api import Float, List, Slot, File, Instance
from fusedwind.turbine.geometry_vt import BeamGeometryVT, BladePlanformVT
from fusedwind.turbine.geometry import SplinedBladePlanform, read_blade_planform


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
    wingsurf = Instance(Assembly(), iotype="out", desc="Complete 3D descrpition of the wing surface")
    
    def execute(self):
        """ Calculate the wingsurface from the spar geometry """
        
        # Make sure that input data has the same length
        self.verify_input()
        
        # Add a splined blade planform from the input data
        self.wingsurf.add('pf_splines', SplinedBladePlanform())
        self.wingsurf.driver.workflow.add('pf_splines')
        self.wingsurf.pf_splines.nC = 3
        self.wingsurf.pf_splines.pfIn = self.eqspar_pf[0]
        self.wingsurf.pf_splines.configure_splines()
        
        cls.add('blade_surface', LoftedBladeSurface())
        cls.driver.workflow.add('blade_surface')

    def verify_input(self):
        """ Verify that the input data is in the correct format """
        
        # Make sure that the two input arrays have the same length
        if not len(self.eqspar_geom)==len(self.eqspar_pf):
            raise(Exception("eqspar_geom and eqspar_pf need to have the same length (amount of segments)"))
        
        
        
        print self.eqspar_geom[0].x
        
