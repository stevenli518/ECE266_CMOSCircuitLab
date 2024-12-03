""" 
    For use in ECE266B
    Author: Chengming Li
    Date: 11/21/2024
    Use: Keysight_E36311A Triple Output Power Supply
    All rights reserved
"""


import pyvisa as pv
#python -m pyvisa info

rm = pv.ResourceManager()
instrs = rm.list_resources()

def PowerSupply_Connect(address):
    ks = rm.open_resource(address)
    print(ks.query("*IDN?"))
    return ks

def Channel_Select(inst, channel = -1):
    """
    :INSTrument:SELect CH1
    """
    ch_lsit = [1, 2, 3]
    command = ""
    if channel not in ch_lsit:
        raise Exception("Sorry, incorrected channel is selected")
    else:
        command = ":INSTrument:SELect CH" + str(channel)
        inst.write(command)

def Voltage_Setup(inst, channel = -1, voltage = 0):
    """
    :SOURce:VOLTage:LEVel:IMMediate:AMPLitude 5,(1)
    """
    ch_lsit = [1, 2, 3]
    command = ""
    if channel not in ch_lsit:
        raise Exception("Sorry, incorrected channel is selected")
    else:
        command = ":SOURce:VOLTage:LEVel:IMMediate:AMPLitude " + str(voltage) + ",(@" + str(channel) + ")"
        inst.write(command)

def Current_Setup(inst, channel = -1, current = 0):
    """
    :SOURce:CURRent:LEVel:IMMediate:AMPLitude 1,(1)
    """
    ch_lsit = [1, 2, 3]
    command = ""
    if channel not in ch_lsit:
        raise Exception("Sorry, incorrected channel is selected")
    else:
        command = ":SOURce:CURRent:LEVel:IMMediate:AMPLitude " + str(current)+ ",(@" + str(channel) + ")"
        inst.write(command)



def Output_ON(inst, channel = -1,):
    """
    :OUTPut:STATe 1,(@1)
    """
    ch_lsit = [1, 2, 3]
    command = ""
    result = 0
    if channel not in ch_lsit:
        raise Exception("Sorry, incorrected channel is selected")
    else:
        command = ":OUTPut:STATe 1,(@" + str(channel) + ")"
        inst.write(command)

def Output_OFF(inst, channel = -1,):
    """
    :OUTPut:STATe 0,(@1)
    """
    ch_lsit = [1, 2, 3]
    command = ""
    result = 0
    if channel not in ch_lsit:
        raise Exception("Sorry, incorrected channel is selected")
    else:
        command = ":OUTPut:STATe 0,(@" + str(channel) + ")"
        inst.write(command)
    