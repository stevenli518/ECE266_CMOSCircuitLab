%% Data acquisition
clearvars
fileID = fopen('./output-freq-433.62443964140175.bin');
Data_bin_in= fread(fileID,'uint16');
Data_filt = Data_bin_in(1:4:end);
Data_bin = dec2bin(Data_filt);
%% SNDR computation
Fs=1e6;
num_segments=1;
f_signal = 433.62443964140175;
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