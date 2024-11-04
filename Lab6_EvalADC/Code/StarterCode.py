########################################################################################################
#
# Drew Hall (drewhall@ucsd.edu)
#
# ECE 266 - Starter code for instrument control
#
# Notes:
#  - https://pyvisa.readthedocs.io/en/latest/index.html 
# - Install pyvisa, pyvisa-py, gpib-ctypes
#
########################################################################################################
import pyvisa
import numpy as np
from math import log10
from pathlib import Path
import shutil
from time import sleep
import matplotlib.pyplot as plt

# Global variables
INSTRUMENT_ID = 'GPIB0::11::INSTR'
SETTLING_TIME = 10
SOURCE_FILE = 'C:/USERS/PUBLIC/Public Documents/Texas Instruments/Plabs-SAR-EVM/Device Files/AD8860/Formatted Rx Data/Formatted Data RX File_0.bin'
DEST_PATH = Path.cwd() / 'Data'


def FuncGenConnect(rm, instrument_id):
    ''' 
    Connect to the function generator

    Parameters:
    - rm: Resource manager handle
    - instrument_id: String of instrument id

    Returns:
    - func_gen: Handle of function generator
    '''
    func_gen = rm.open_resource(instrument_id)
    func_gen.write('*IDN?')
    resp = func_gen.read()
    print(resp)

    return func_gen

def FuncGenSetup(func_gen, channel, minV=0, maxV=5):
    '''
    Set up the function generator    

    Parameters:
    - func_gen: VISA handle to the instrument
    - channel: 1 or 2
    - minV: Minimum voltage (limit)
    - maxV: Maximum voltage (limit)
    '''
    pass

def FuncGenSinusoid(func_gen, channel, offset, amp, frequency, phase=0):
    '''
    Output a sinusoid from the function generator

    Parameters:
    - freq: frequency (Hz)
    - offset: offset voltage (V)
    - phase: phase (degrees)
    '''
    pass

def GetADCData(src_filename, dest_path, freq):
    '''
    Wait for the PLabs EVM software to write the file and then copy it

    Parameters:
    - src_path: Path to binary ADC data from PLabs software
    - dest_path: Path to location to save data. Path will be appended with freq to create a unique filenmae.
    - freq: frequency of sweep

    Returns:
    - Status: True if successful
    '''

    # Set up the paths
    src = Path(src_filename)
    Path(dest_path).mkdir(parents=True, exist_ok=True)
    dest = Path(dest_path) / f'output-freq-{freq}.bin'

    # Wait for the file to exist
    while not src.is_file():
        pass

    # Copy the file
    return shutil.copy(str(src), str(dest)) == str(dest)

def main():
    # Test parameters
    freq_start = 1e3
    freq_end = 100e3
    samples_per_decade = 10
    offset = 2.5
    amp = 4
    
    # Setup GPIB subsystem        
    pyvisa.log_to_screen()          # Useful for debugging
    rm = pyvisa.ResourceManager()
    print(rm.list_resources())

    # Connect to the function generator via GPIB
    func_gen = FuncGenConnect(rm, INSTRUMENT_ID)
    if not func_gen:
        print('Could not find instrument, aborting...')
        quit()

    # Set up the function generator
    FuncGenSetup(func_gen, 1)

    # Generate the frequency vector
 
    # Sweep the frequency
    for freq in freqs:
        print(f'Measuring {freq} Hz...')
        FuncGenSinusoid(func_gen, 1, offset, amp, freq)
        sleep(SETTLING_TIME)

        if not GetADCData(SOURCE_FILE, DEST_PATH, freq):
            print('Error copying file, aborting...')
            quit()

    print('Done!')

if __name__ == '__main__':
    main()