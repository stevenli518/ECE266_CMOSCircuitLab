from pathlib import Path
import shutil

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
    print("Here")
    # Set up the paths
    # SOURCE_FILE = 'C:/USERS/PUBLIC/Public Documents/Texas Instruments/Plabs-SAR-EVM/Device Files/AD8860/Formatted Rx Data/Formatted Data RX File_0.bin'
    # DEST_PATH = Path.cwd() / 'Data'
    src = Path(src_filename)
    Path(dest_path).mkdir(parents=True, exist_ok=True)
    dest = Path(dest_path) / f'output-freq-{freq}.bin'
    
    # Wait for the file to exist
    while not src.is_file():
        pass
    
    # Copy the file
    return shutil.copy(str(src), str(dest)) == str(dest)