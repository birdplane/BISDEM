import numpy as np
import matplotlib.pyplot as plt

from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float,VarTree, Int

from BISDEM.lib.vartrees import WingDefVT, WingPosVT, MechPosVT, WingSpdVT, WingPhlVT
from BISDEM.lib.geo import triangle

from fusedwind.turbine.geometry_vt import BeamGeometryVT
from fusedwind.lib.geom_tools import calculate_length

class wing_motion(Component):
    
    """
    1. Calculates wing position according to given mechanism motion and wing definition (wingpos) 
    2. Calculates velocity over wingspan with given discretization for an equivalent spar
    
    """
    
    # Inputs
    wdef = VarTree(WingDefVT(), iotype='in', desc='Wing definition')
    mpos = VarTree(MechPosVT(), iotype='in', desc='Mech position')
    dt = Float(iotype='in', desc='Timestep')
    n  = Int(iotype='in', desc='Number of sections to describe the wing')
    
    # Outputs
    wpos = VarTree(WingPosVT(), iotype='out', desc='Position of the points O, A, C, D, E for each time step')
    wspeed = VarTree(WingSpdVT(), iotype='out', desc='Wing speeds')
    wtwist = VarTree(WingPhlVT(), iotype='out', desc='Wing speeds')
    Dymax = Float(iotype='out', desc='Highest wing tip location')
    AD = Float(iotype='out', desc='Area encircled by D')

    def execute(self):
        
        # Calculate position of hinge points on the wing for all time steps
        self.wingpos()
        
        # Create an equivalent beam description of the wing for all time steps
        self.createEquivalentBeam()
        
        self.Dymax = np.max(self.wpos.front.D[1])
        
    def wingpos(self):
        """
        Calculates wing position according to given mechanism motion and wing definition
        """
        
        # hand over interface hinge positions from mechanism
        self.wpos.front.A = self.mpos.front.A
        self.wpos.back.A = self.mpos.back.A
        self.wpos.front.O = self.mpos.front.O
        self.wpos.back.O = self.mpos.back.O
        
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

    def createEquivalentBeam(self):
        """ 
        Takes the wing positions at every time step and creates an equivalent beam description 
        """
        
        # distance following the form of the wing
        r_OC = np.linspace(0.0, self.wdef.front.OC, np.round(self.n*self.wdef.front.OC/(self.wdef.front.OC+self.wdef.front.CD)))
        r_CD = np.linspace(0.0, self.wdef.front.CD, np.round(self.n*self.wdef.front.CD/(self.wdef.front.OC+self.wdef.front.CD))+1)
        
        # calculate vector from O to C and from C to D for angular step of the mechanism
        OCf_vec = (self.wpos.front.C-self.wpos.front.O).T
        CDf_vec = (self.wpos.front.D-self.wpos.front.C).T
        OCb_vec = (self.wpos.back.C-self.wpos.back.O).T
        CDb_vec = (self.wpos.back.D-self.wpos.back.C).T
        
        for ocf, cdf, ocb, cdb in zip(OCf_vec, CDf_vec, OCb_vec, CDb_vec):
            
            # make unit vectors
            ocf = ocf/np.linalg.norm(ocf)
            cdf = cdf/np.linalg.norm(cdf)
            
            ocb = ocb/np.linalg.norm(ocb)
            cdb = cdb/np.linalg.norm(cdb)
            
            # beam position
            beam_pos = np.array([[0.0, 0.0, 0.0]])
            for r in r_OC[1:]:
                beam_pos = np.vstack((beam_pos, [ocf*r]))
                beam_pos[-1][2] = self.wpos.front.O[2][0]
            for r in r_CD[1:]:
                beam_pos = np.vstack((beam_pos, [beam_pos[len(r_OC)-1]+cdf*r]))
                beam_pos[-1][2] = self.wpos.front.O[2][0]
            
            # put position into correct structure
            beam = BeamGeometryVT()
            beam.x = beam_pos.T[2]
            beam.y = beam_pos.T[1]
            beam.z = beam_pos.T[0]
            
            # beam twist
            beam_pos_back = np.array([[0.0, 0.0, self.wpos.back.O[2][0]]])
            
            z = np.array([0, 0, 1])
            x = np.array([ocf])
            for r in r_OC[1:]:
                beam_pos_back = np.vstack((beam_pos_back, [ocb*r]))
                # Assumption: no taper, no sweep
                beam_pos_back[-1][2] = self.wpos.back.O[2][0]
                #rot_x.append(np.rad2deg(np.arccos(np.dot(ocf, np.array([1, 0, 0]))/np.linalg.norm(ocf))))
                z = np.vstack((z, [0, 0, 1]))
                x = np.vstack((x, [ocf]))

            for r in r_CD[1:]:
                beam_pos_back = np.vstack((beam_pos_back, [beam_pos_back[len(r_OC)-1]+cdb*r]))
                # Assumption: no taper, no sweep
                beam_pos_back[-1][2] = self.wpos.back.O[2][0]
                #rot_x.append(np.rad2deg(np.arccos(np.dot(cdf, np.array([1, 0, 0]))/np.linalg.norm(cdf))))
                z = np.vstack((z, [0, 0, 1]))
                x = np.vstack((x, [cdf]))

            y = np.cross(x, z)
            y = y/((y*y).sum(axis=1)**0.5)[:, np.newaxis]
            
            

            v = beam_pos-beam_pos_back
            v_y = (v*y).sum(axis=1)
            v_x = (v*x).sum(axis=1)
            v_z = (v*z).sum(axis=1)
            
            #v_z = beam_pos-beam_pos_back
            #v_z[:,1] = np.zeros(len(v_z))
            #v_z = v_z/((v_z*v_z).sum(axis=1)**0.5)[:,np.newaxis]
            
            beam.rot_x = np.zeros(len(beam_pos.T[0])) #np.array(rot_x)
            beam.rot_y = np.zeros(len(beam_pos.T[0])) #np.rad2deg(np.arctan((beam_pos.T[0]-beam_pos_back.T[0])/(beam_pos.T[2]-beam_pos_back.T[2])))
            beam.rot_z = -np.rad2deg(np.arctan(v_y/v_z)) #np.sign(v[:,1])*np.rad2deg(np.arccos((v*v_z).sum(axis=1)/(v*v).sum(axis=1)**0.5))   # np.rad2deg(np.arctan((beam_pos.T[1]-beam_pos_back.T[1])/(beam_pos.T[2]-beam_pos_back.T[2])))
            beam.s = calculate_length(np.array([beam.x, beam.y, beam.z]).T)
            
            print beam.rot_z[20]
            
            # beam speed
            if len(self.wpos.eqspar_geom)>0:
                beam_previous = self.wpos.eqspar_geom[-1]
                beam_previous.vel_x = (beam.x-beam_previous.x)/self.dt
                beam_previous.vel_y = (beam.y-beam_previous.y)/self.dt
                beam_previous.vel_z = (beam.z-beam_previous.z)/self.dt
                self.wpos.eqspar_geom[-1] = beam_previous
            
            self.wpos.eqspar_geom.append(beam)
        
        self.wpos.eqspar_geom.pop()
