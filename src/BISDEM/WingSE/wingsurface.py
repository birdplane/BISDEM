import numpy as np

from BISDEM.lib.vartrees import WingPlanformVT
from openmdao.main.api import Component, Assembly
from openmdao.lib.datatypes.api import Float, List, Slot, File, Instance, Str, Int
from fusedwind.turbine.geometry_vt import BeamGeometryVT, BladePlanformVT
from fusedwind.turbine.geometry import SplinedBladePlanform, read_blade_planform, LoftedBladeSurface


class WingSurface(Component):
    """
    This class carries a full description of the wing surface at any time-step. 
    The definition is based of the fusedwind framework definitions. http://www.fusedwind.org
    """
    
    # Inputs
    eqspar_geom = List(BeamGeometryVT(), iotype='in', desc='Position and twist of the equivalent(discrete) beam of the wing, fusedwind definition'
                          'per timestep, type is BeamGeometryVT')
    planform_in = List(WingPlanformVT(), iotype='in', desc='Wing planform definition along beam(discrete), needs to be same length'
                      'as eqspar_geom, also per time step. Type is BeamPlanformVT')
    span_ni = Int(iotype='in', desc='Number of sections for the aerodynamic calculation')
    airfoils = List(Str, iotype="in", desc='List of airfoil description files')
    
    # Outputs
    wingsurf = List(Assembly(), iotype="out", desc="Complete 3D descrpition of the wing surface")
    
    def execute(self):
        """ Calculate the wingsurface from the spar geometry """
        
        # Make sure that input data has the same length
        self.verify_input()
        
        for beam in self.eqbeams:
            a = Assembly()
        
            # Add a splined blade planform from the input data
            a.add('pf_splines', SplinedBladePlanform(True))
            a.driver.workflow.add('pf_splines')
            a.pf_splines.nC = 3
            a.pf_splines.pfIn = beam
            a.pf_splines.configure_splines()
            
            a.create_passthrough('pf_splines.blade_length')
            a.create_passthrough('pf_splines.span_ni')
            
            a.add('blade_surface', LoftedBladeSurface())
            a.driver.workflow.add('blade_surface')
            
            a.connect('pf_splines.pfOut', 'blade_surface.pf')
            a.connect('span_ni', 'blade_surface.span_ni')
            
            # load the planform file
            a.span_ni = self.span_ni
            
            b = a.blade_surface
            
            # distribute 200 points evenly along the airfoil sections
            b.chord_ni = 200
            for f in self.airfoils:
                b.base_airfoils.append(np.loadtxt(f))
            b.blend_var = np.array([0.25, 0.75])
            
            self.wingsurf.append(a)
        

    def verify_input(self):
        """ Verify that the input data is in the correct format """
        
        # Make sure that the two input arrays have the same length
        if not len(self.eqspar_geom)==len(self.planform_in):
            print "length of eqspar_geom: ", len(self.eqspar_geom)
            print "length of planform: ", len(self.planform_in)
            raise(Exception("eqspar_geom and eqspar_pf need to have the same length (amount of segments)"))
        
        self.eqbeams = []
        for pf, spar in zip(self.planform_in, self.eqspar_geom):
            spar.__class__ = BladePlanformVT
            b = spar
            b.blade_length = pf.blade_length
            b.athick = pf.athick
            b.p_le = pf.p_le
            
            # Normalize input data
            b.x = b.x/b.z[-1]
            b.y = b.y/b.z[-1]
            b.z = b.z/b.z[-1]
            b.s = b.s/b.s[-1]
            b.chord = pf.chord/b.z[-1]
            b.rthick  = pf.rthick/np.max(pf.rthick)
            
            self.eqbeams.append(b)
        