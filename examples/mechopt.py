import numpy as np

from openmdao.main.api import Assembly, set_as_top
from openmdao.lib.drivers.api import SLSQPdriver, CONMINdriver, NEWSUMTdriver, COBYLAdriver

from BISDEM.WingSE.init import wing_init
from BISDEM.MechSE.init import mech_init

from BISDEM.WingSE.motion import wing_motion
from BISDEM.MechSE.motion import mech_motion

class optimize(Assembly):
    
    """ Example optimization of mechanism in respect to varying objectives """

    def configure(self):
        
        # create Optimizer instance
        self.add('driver', SLSQPdriver())
        
        # Add components
        self.add('mech', mech_motion())
        self.add('wing', wing_motion())

        # Add components to workflow
        self.driver.workflow.add(['mech', 'wing'])
        
        # Add parameters to driver
        self.driver.add_parameter(('mech.mdef.front.Ri'), low = 5.e-3, high = 9.e-3)
        self.driver.add_parameter(('mech.mdef.front.Ro'), low = 20.e-3, high = 25.e-3)
        self.driver.add_parameter(('mech.mdef.front.theta_del'), low = np.radians(30), high = np.radians(180))
        
        # Make all connections
        self.connect('mech.mpos','wing.mpos')
        
        # Add constrains to inner optimizer
        self.driver.add_constraint('mech.mdef.front.Ri <= 1')

        # Outer optimization parameters
        self.driver.add_objective('-wing.Dymax')
        
        #Driver settings
        
#         self.driver.itmax = 300
#         self.driver.fdch = 0.00000001
#         self.driver.fdchm = 0.000000001
#         self.driver.ctlmin = 0.00001
#         self.driver.delfun = 0.000001
#         self.driver.conmin_diff = True
        

        
        
if __name__ == "__main__": # pragma: no cover

    import time

    opt = set_as_top(optimize())
    opt.name = "top"
    
    # Define mechanism
    
    MechInit = mech_init()

    MechInit.fGx = MechInit.bGx = -16e-3
    MechInit.fGy = MechInit.bGy = -70e-3
    MechInit.fRi = MechInit.bRi = 9e-3
    MechInit.fRo = MechInit.bRo = 24e-3
    MechInit.fQB = MechInit.bQB = 65e-3
    MechInit.fPA = MechInit.bPA = 65e-3
    MechInit.ftheta_del = MechInit.btheta_del = np.radians(60)
    MechInit.fBO = MechInit.bBO = 45e-3
    MechInit.fAO = MechInit.bAO = 16e-3
    
    MechInit.fz = 0
    MechInit.bz = -30e-3
    
    MechInit.run()
    opt.mech.mdef = MechInit.mdef
    
    
    # Define wing
    
    WingInit = wing_init()

    WingInit.fAE = WingInit.bAE = 0.235
    WingInit.fEC = WingInit.bEC = 0.016
    WingInit.fOC = WingInit.bOC = 0.235
    WingInit.fCD = WingInit.bCD = 0.470
    WingInit.fED = WingInit.bED = 0.455
    WingInit.fz = 0.
    WingInit.bz = MechInit.bz
    
    WingInit.run()
    opt.wing.wdef = WingInit.wdef
    
    
    # Define running parameters
    
    theta = np.linspace(0, 2*np.pi, 200)
    phi = np.ones(len(theta)) * np.radians(0)
    
    opt.mech.theta = theta
    opt.mech.phi = phi
    
    
    opt.mech.run()
    opt.wing.mpos = opt.mech.mpos  
    opt.wing.run()

    
    
    
    tt = time.time()
    opt.run()
    print "\n"
    print "Minimum found at (%f,%f,%f)" % (opt.mech.mdef.front.Ri,opt.mech.mdef.front.Ro,np.degrees(opt.mech.mdef.front.theta_del))
    print opt.wing.Dymax

    print "Elapsed time: ", time.time()-tt, "seconds"