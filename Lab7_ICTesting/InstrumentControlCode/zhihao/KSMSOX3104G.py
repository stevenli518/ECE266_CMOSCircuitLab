""" 
    For use in ECE266B
    Author: Chengming Li
    Date: 11/21/2024
    Use: Keysight_InfiniiVision MSOX3104G Oscilloscope
    All rights reserved
"""

import pyvisa as pv
#python -m pyvisa info

rm = pv.ResourceManager()
instrs = rm.list_resources()

def Oscilloscope_Connect(address):
    ks = rm.open_resource(address)
    print(ks.query("*IDN?"))
    return ks

def Oscilloscope_Stop(inst):
    inst.write(":STOP")

def Oscilloscope_Single(inst):
    inst.write(":SINGle")

def Oscilloscope_RUN(inst):
    inst.write(":RUN")

def Oscilloscope_TimeBase(inst, div):
    command = ":TIMebase:SCALe "+str(div)
    inst.write(command)

def Oscilloscope_Trigger(inst):
    inst.write(":TRIGger:MODE EDGE")
    inst.write(":TRIGger:EDGE:SLOPe POSitive")
    inst.write(":TRIGger:EDGE:SOURce DIGital11")

def Oscilloscope_SetBUS(inst):
    inst.write(":BUS1:BITS (@0:15),0")
    inst.write(":BUS1:BITS (@0:8,11),1")

def Oscilloscope_WGen_Square(inst,clk_freq, clk_amp, clk_offset,clk_duty):
    # inst.write(":WGEN1:OUTPut:LOAD ONEMeg")
    inst.write(":WGEN1:OUTPut:LOAD FIFTY")
    inst.write(":WGEN1:FUNCtion SQUare")

    command = ":WGEN1:FREQuency " + str(clk_freq)
    inst.write(command)
    command = ":WGEN1:VOLTage:HIGH " + str(clk_amp)
    inst.write(command)
    command = ":WGEN1:VOLTage:LOW 0" 
    inst.write(command)
    command = ":WGEN1:VOLTage:OFFSet " + str(clk_offset)
    inst.write(command)
    command = ":WGEN1:FUNCtion:SQUare:DCYCle " + str(clk_duty)
    inst.write(command)

def DigitalDisplay_ON(inst, on):
    for i in range(16):
        command = ":DIGital"+str(i)+":DISPlay 0"
        inst.write(command)
    mydigi_ch = list(range(9))
    mydigi_ch.append(11)
    if on == 1:
        for i in mydigi_ch:
            command = ":DIGital"+str(i)+":DISPlay 1"
            inst.write(command)

def SetDigital_Threshold(inst, th):
    for i in range(16):
        command = ":DIGital"+str(i)+":THReshold " + str(th)
        inst.write(command)

def Digitalizer_ON_OFF(inst, on):
    if on == 1:
        command = "ACQuire:DIGitizer 1"
        inst.write(command)
    else:
        command = "ACQuire:DIGitizer 0"
        inst.write(command)    

def Save_waveform(inst, source:str):
    """
    :WAVeform:SOURce CHANnel1
    CHANnel1|2|3|4
    FUNCtion1|2|3|4
    MATH1|2|3|4
    FFT
    POD1|2
    BUS1|2
    SBUS1|2
    WMEMory1|2|3|4
    """
    command = ":WAVeform:SOURce " + source
    inst.write(command)
    command = ":WAVeform:BYTeorder MSBFirst"
    inst.write(command)
    command = ":WAVeform:FORMat ASCii"
    inst.write(command)
    command = ":WAVeform:POINts MAXimum"
    inst.write(command)

    command = ":WAVeform:PREamble?"
    preamble = inst.query(command)
    command = ":WAVeform:DATA?"
    data = inst.query(command)
    # with open(filename, "wb") as f:
    #     f.write(data)
    return preamble, data

def Oscilloscope_WGen_Square_ON(inst):
    command = ":WGEN:OUTPut 1"
    inst.write(command)

def Oscilloscope_WGen_Square_OFF(inst):
    command = ":WGEN:OUTPut 0"
    inst.write(command)