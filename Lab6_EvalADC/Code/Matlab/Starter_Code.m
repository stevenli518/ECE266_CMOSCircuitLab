%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Drew Hall (drewhall@ucsd.edu)
%
% ECE 266 - Starter code for instrument control
%
% Notes:
%   - Requires instrument control toolbox
%   - Requiers VISA (NI or Keysight)
%   - Requires MATLAB 2021b (if you get an error about visadev not being 
%     defined, this is why)
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Instrument set up
INSTRUMENT_ID = "GPIB0::11::INSTR";
SETTLING_TIME = 10;
SOURCE_FILE = "C:\USERS\PUBLIC\Public Documents\Texas Instruments\Plabs-SAR-EVM/Device Files\AD8860\Formatted Rx Data\Formatted Data RX File_0.bin";
DEST_PATH = fullfile(pwd, 'Data');

% Test parameters
freq_start = 1e3;
freq_end = 100e3;
samples_per_decade = 10;
offset = 2.5;
amp = 4;
   
% Connect tot he function generator via GPIB
func_gen = FuncGenConnect(INSTRUMENT_ID);

% Set up the function generator
FuncGenSetup(func_gen, 1);

% Generate the frequency vector
freqs = [1 10]

% Sweep the frequency
for freq = freqs
    fprintf('Measuring %d Hz...', freq))
    FuncGenSinusoid(func_gen, 1, offset, amp, freq);
    pause(SETTLING_TIME);

    if ~GetADCData(SOURCE_FILE, DEST_PATH, freq)
        disp('Error copying file, aborting...')
        clear func_gen
        return
    end
end

clear func_gen
disp('Done!')

%%    Connect to the function generator
%
%    Parameters:
%    - rm: Resource manager handle
%    - instrument_id: String of instrument id
%
%    Returns:
%    - func_gen: Handle of function generator
function func_gen = FuncGenConnect(instrument_id)
    visadevlist
    func_gen = visadev(instrument_id);
    
    writeline(func_gen, '*IDN?');
    resp = readline(func_gen);
    disp(resp)

    writeline(func_gen, '*RST');
end

%%    Set up the function generator    
%
%    Parameters:
%    - func_gen: VISA handle to the instrument
%    - channel: 1 or 2
%    - minV: Minimum voltage (limit)
%    - maxV: Maximum voltage (limit)
function FuncGenSetup(func_gen, channel, minV, maxV)
    ;
end

%%    Output a sinusoid from the function generator
%
%    Parameters:
%    - freq: frequency (Hz)
%    - offset: offset voltage (V)
%    - phase: phase (degrees)
function FuncGenSinusoid(func_gen, channel, offset, amp, frequency, phase)
    ;
end

%%    Wait for the PLabs EVM software to write the file and then copy it
%
%    Parameters:
%    - src_path: Path to binary ADC data from PLabs software
%    - dest_path: Path to location to save data. Path will be appended with freq to create a unique filenmae.
%    - freq: frequency of sweep
%
%    Returns:
%    - Status: True if successful
function status = GetADCData(src_filename, dest_path, freq)
    % Set up the paths
    mkdir(dest_path); 
    dest = fullfile(dest_path, sprintf('output-freq-%d.bin', freq));

    % Wait for the file to exist
    while ~isfile(src_filename)
        ;
    end

    % Copy the file
    status = copyfile(src_filename, dest);
end