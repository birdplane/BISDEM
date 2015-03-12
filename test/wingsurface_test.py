import numpy as np
import matplotlib.pyplot as plt

from BISDEM.WingSE.wingsurface import WingSurface

from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float, List, Slot, File, FileRef
from fusedwind.turbine.geometry_vt import BeamGeometryVT, BladePlanformVT

surface = WingSurface()
beam = BeamGeometryVT()
beam.x = [0, 0.1, 0.2];
beam.y = [0, 0.1, 0.2];
beam.z = [0, 0.1, 0.2];
beam.rot_x = [0, 0, 0];
beam.rot_y = [0, 0, 0];
beam.rot_z = [0, 0, 0];
surface.eqspar_geom  = [beam];

planform = BladePlanformVT();
planform.blade_length = 0.75;
planform.chord = [0.2, 0.2, 0.1];
planform.rthick = [0.05, 0.05, 0.05];
planform.athick = [0.05, 0.05, 0.05];
planform.p_le = [0.07, 0.05, 0.03];
surface.eqspar_pf = [planform];

airfoil  = open('/home/jan/diesdas.txt', 'rw')
surface.airfoil = [airfoil];

surface.run()