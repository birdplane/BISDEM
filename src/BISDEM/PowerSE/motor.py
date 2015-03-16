import numpy as np

from BISDEM.lib.vartrees import MotorVT, PowerSupplyVT

from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float, VarTree


# Make sure that your class has some kind of docstring. Otherwise
# the descriptions for your variables won't show up in the
# source ducumentation.
class TorqueAtRPM(Component):
    """
    Calculates the output torque of the motor for a required rpm. 
    """
    
    # Inputs
    motor = VarTree(MotorVT(), iotype='in', desc='Full Motor description')
    power = VarTree(PowerSupplyVT(), iotype='in', desc='Full PowerSupply description')
    n  = Float(iotype='in', desc='Rotation speed in rpm')
    
    
    # Outputs
    torque = Float(iotype='out', desc='Torque at n rpm')

    def execute(self):
        # Motor constant
        kM = 1/self.motor.kV * 30/np.pi
        # Current at given speed
        I = (self.power.voltage - self.n/self.motor.kV)/self.motor.Rm
        # Output torque
        self.torque = I * kM
        
        
