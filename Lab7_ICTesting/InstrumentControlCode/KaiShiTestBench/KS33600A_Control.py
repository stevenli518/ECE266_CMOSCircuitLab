""" 
    For use in ECE266B
    Author: Chengming Li
    Date: 11/21/2024
    Use: Keysight_E33600 Function Generator
    All rights reserved
"""


import pyvisa as pv
#python -m pyvisa info

rm = pv.ResourceManager()
instrs = rm.list_resources()

def FuncGenConnect(address):
    adg = rm.open_resource(address)
    print(adg.query("*IDN?"))
    return adg

def UnitVpp_setup(inst, channel = -1):
    """
    :SOURce1:VOLTage:UNIT VPP
    """
    ch_lsit = [1, 2]
    command = ""
    if channel not in ch_lsit:
        raise Exception("Sorry, incorrected channel is selected")
    else:
        command = ":SOURce"  + str(channel) +  ":VOLTage:UNIT VPP"
        inst.write(command)

def Sin_setup(inst, channel, freq, amp, offset):
    """
    :SOURce1:APPLy:SINusoid 2000,1,0.5
    Channel: 1
    Freq: 2000
    Amplitude: 1
    Offset: 0.5
    """
    ch_lsit = [1, 2]
    command = ""
    if channel not in ch_lsit:
        raise Exception("Sorry, incorrected channel is selected")
    else:
        command = ":SOURce" + str(channel) + ":APPLy:SINusoid " + str(freq) +"," + str(amp) + " VPP" + "," + str(offset)
        inst.write(command)

def PWM_setup(inst, channel, freq, amp, offset, duty):
    """
    :SOURce1:APPLy:SQUare 1000000,1 VPP,0.5
    Channel: 1
    Freq: 2000
    Amplitude: 1
    Offset: 0.5

    :SOURce1:FUNCtion:SQUare:DCYCle 50
    Channel: 1
    Duty: 50    
    """
    ch_lsit = [1, 2]
    command = ""
    if channel not in ch_lsit:
        raise Exception("Sorry, incorrected channel is selected")
    else:
        command = ":SOURce" + str(channel) + ":APPLy:SQUare " + str(freq) +"," + str(amp) + " VPP" +"," + str(offset)
        inst.write(command)
        command = ":SOURce" + str(channel) + ":FUNCtion:SQUare:DCYCle " + str(duty)
        inst.write(command)

def Load__setup (inst, channel, HighZ):
    """
    :OUTPut1:LOAD INFinity
    :OUTPut2:LOAD INFinity
    Channel: 1
    LOAD_Termination: INF | 50
    """
    ch_lsit = [1, 2]
    if channel not in ch_lsit:
        raise Exception("Sorry, incorrected channel is selected")
    else:
        set_HighZ_command = "OUTPut" + str(channel) + ":LOAD INFinity"
        set_50_command = "OUTPut" + str(channel) + ":LOAD 50"
        if HighZ == 1:
            inst.write(set_HighZ_command)
        else:
            inst.write(set_50_command)

def Polarity_invert(inst, channel, invert):
    """
    :OUTPut2:SYNC:POLarity INVerted
    :OUTPut2:POLarity NORMal
    """
    ch_lsit = [1, 2]
    if channel not in ch_lsit:
        raise Exception("Sorry, incorrected channel is selected")
    else:
        set_invert_command = ":OUTPut" + str(channel) + ":POLarity INVerted"
        set_normal_command = ":OUTPut" + str(channel) + ":POLarity NORMal"
        if invert == 1:
            inst.write(set_invert_command)
        else:
            inst.write(set_normal_command)

def Sync_phase(inst):
    """
    :SOURce:PHASe:SYNChronize
    """
    sync_command = ":SOURce:PHASe:SYNChronize"
    inst.write(sync_command)

def Voltage_coupling(inst, on = -1):
    """
    :SOURce:VOLTage:COUPle:STATe 1    
    """
    couplingON_command = ":SOURce:VOLTage:COUPle:STATe 1"
    couplingOFF_command = ":SOURce:VOLTage:COUPle:STATe 0"
    if on == 1:
        inst.write(couplingON_command)
    else:
        inst.write(couplingOFF_command)

def Freq_coupling(inst, on = -1):
    """
    :SOURce:FREQuency:COUPle:STATe 1    
    """
    couplingON_command = ":SOURce:FREQuency:COUPle:STATe 1"
    couplingOFF_command = ":SOURce:FREQuency:COUPle:STATe 0"
    if on == 1:
        inst.write(couplingON_command)
    else:
        inst.write(couplingOFF_command)

def output_ON(inst,channel):
    """
    :OUTPut1 1
    Channel: 1
    STATE: 1(ON)
    """
    ch_lsit = [1, 2]
    command = ""
    if channel not in ch_lsit:
        raise Exception("Sorry, incorrected channel is selected")
    else:
        command = ":OUTPut" + str(channel) + " 1"
        inst.write(command)

def output_OFF(inst,channel):
    """
    :OUTPut1 0
    Channel: 1
    STATE: 0(OFF)
    """
    ch_lsit = [1, 2]
    command = ""
    if channel not in ch_lsit:
        raise Exception("Sorry, incorrected channel is selected")
    else:
        command = ":OUTPut" + str(channel) + " 0"
        inst.write(command)
