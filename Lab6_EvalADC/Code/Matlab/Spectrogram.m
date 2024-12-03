%% Data acquisition
fileID = fopen('C:\Users\steve\OneDrive\Documents\GitHub\ECE266_CMOSCircuitLab\Lab6_EvalADC\Data\output-freq-94015.07732715982.bin');
Data_bin_in= fread(fileID,'uint16');
Data_filt = Data_bin_in(1:4:end);
%% SNDR computation
Fs=1e6;
num_segments=1;
f_signal =94015.07732715982;
f_s = Fs;
BW =500e3;
sample_size=2^18;
periodogram_length = sample_size / num_segments;
fbin = f_s / periodogram_length;
plotYN = 1; plotAll = 0; plotHold = 0; plotLin = 0; datNorm = 1;
[sinusoid_power, data_minus_sinusoid_in_BW_power, SNDR, ENOB,HD2,HD3, SNR, SFDR] = ...
    plot_periodogram_SFDR(Data_filt, periodogram_length, num_segments, f_signal, ...
    f_s, BW, plotAll, plotHold, plotYN, plotLin,datNorm);
fprintf('SNDR calculated within %d kHz bandwidth = %.3f dB, HD2 = %.3f and HD3 = %.3f\n', BW/1000, SNDR, HD2,HD3);
set(gcf,'color','w')
%% 
fs = 1e6;                 % Sampling rate in Hz
N = length(Data_filt);                  % Number of samples
bit_depth = 16;            % ADC bit resolution
V_min = 0;              % Minimum input voltage
V_max = 5;               % Maximum input voltage

% Map codes to voltage
voltages = ((Data_filt / (2^bit_depth - 1)) * (V_max - V_min)) + V_min;

% Create time axis
t = (0:N-1) / fs;

% Plot the reconstructed waveform
figure;
plot(t, voltages, 'b');
title('Reconstructed Time-Domain Waveform');
xlabel('Time (s)');
ylabel('Amplitude (V)');
grid on;