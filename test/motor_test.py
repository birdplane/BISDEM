import numpy as np

from BISDEM.lib.vartrees import MotorVT, PowerSupplyVT
from BISDEM.PowerSE.motor import TorqueAtRPM

motor = MotorVT()
motor.kV = 1000
motor.A_max = 35 
motor.P_max = 550
motor.I_0 = 1.8
motor.Rm = 0.03
power = PowerSupplyVT()
power.voltage = 11.1

torque = TorqueAtRPM()
torque.motor = motor
torque.power = power
torque.n = 9000
torque.run()

print torque.torque