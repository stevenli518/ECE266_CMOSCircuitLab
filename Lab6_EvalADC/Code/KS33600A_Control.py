import pyvisa as pv
#python -m pyvisa info

rm = pv.ResourceManager()
instrs = rm.list_resources()

def FuncGenConnect(address):
    adg = rm.open_resource(address)
    print(adg.query("*IDN?"))
    return adg

def voltage_setup(inst, ch = 2,minV = 0, maxV = 5):
    '''
    Set up the function generator    

    Parameters:
    - func_gen: VISA inst to the instrument
    - channel: 1 or 2
    - minV: Minimum voltage (limit)
    - maxV: Maximum voltage (limit)
    '''

    set_high_command = 'SOURce'+str(ch)+':VOLTage:LIMit:HIGH ' + "+"+str(maxV)
    set_low_command = 'SOURce'+str(ch)+':VOLTage:LIMit:LOW ' + str(minV)
    inst.write(set_high_command)
    inst.write(set_low_command)
    return

def sinusoid_setup(inst, channel, offset, amp, frequency, phase=0):
    '''
    Output a sinusoid from the function generator

    Parameters:
    - freq: frequency (Hz)
    - offset: offset voltage (V)
    - phase: phase (degrees)
    '''
    # Set the HIgh Z
    set_HighZ = "OUTPut1:LOAD INF"
    inst.write(set_HighZ)
    set_HighZ = "OUTPut2:LOAD INF"
    inst.write(set_HighZ)

    # Set the output shape
    set_shape = 'FUNCtion:SIN'
    inst.write(set_shape)

    # Set the phase
    set_phase = 'PHASe: +' + str(phase)
    inst.write(set_phase)

    # Set the frequency mode
    # E.g.SOURce1:FREQuency:MODE CW|FIXed|SWEep
    set_mode = 'FREQuency:MODE FIXed' 
    inst.write(set_mode)

    # Set the freq
    # E.g. SOURce1:FREQuency:FIXed 500kHz
    set_freq = 'FREQuency +' + str(frequency)
    inst.write(set_freq)

    # Set the offset 
    # E.g. SOURce1:VOLTage:LEVel:IMMediate:OFFSet 500mV
    # set_offset = 'VOLT:OFFS ' + str(2.52)
    # inst.write(set_offset)

    # Set the unit to Vpp
    # E.g. SOURce1:VOLTage:UNIT VPP
    set_unit = 'VOLT:UNIT VPP'
    inst.write(set_unit)


    # Set the Amplitude
    # E.g. SOURce1:VOLTage:LEVel:IMMediate:AMPLitude 1V
    set_amp = 'VOLTage:HIGH +' + str(amp)
    inst.write(set_amp)
    set_amp = 'VOLTage:LOW +' + str(0)
    inst.write(set_amp)
    return

def freq_setup(inst, freq):
    set_freq = 'FREQuency +' + str(freq)
    inst.write(set_freq)

def output_ON(inst,ch = 2):
    # Enable Output at channel 1|2
    # OUTPUT1:STATE ON
    # 'OUTPut2 ON'
    output_en_command = 'OUTPut' + str(ch) + ' ON'
    inst.write(output_en_command)
    return

def output_OFF(inst,ch = 2):
    # Enable Output at channel 1|2
    # OUTPUT1:STATE ON
    output_en_command = 'OUTPut' + str(ch) + ' OFF'
    inst.write(output_en_command)
    return

