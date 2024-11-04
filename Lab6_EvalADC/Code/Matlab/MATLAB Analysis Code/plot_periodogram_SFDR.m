% This function takes a data sequence assumed to be of the form
% x[n] = A*sin(2*pi*f_signal/f_s*n + initial_phase) + e[n],
% where e[n] is noise, plots discrete-time PSD estimates of its
% sinusoid and noise components using the averaged periodograms
% method, and returns the estimated mean squared values of these two
% components. The spectral estimation is performed by partitioning the
% data sequence into segments, generating a periodogram for each segment
% using the Hanning window, and averaging the periodograms. The extraction
% of the sinusoid and noise components of the signal is performed with
% the sinusoidal minimum error method.
% The function takes as inputs the data sequence, the periodogram length,
% the number of segments to use, f_signal, and f_s.
%
% Source: ECE 264C HW#1 http://eceweb.ucsd.edu/courses/ECE264/FA_2017/
% User Name: ECE264C
% Password:ADCs_2017

function [sinusoid_power, data_minus_sinusoid_in_BW_power, SNDR, ENOB,HD2,HD3] = ...
    plot_periodogram(data, ...
    periodogram_length, ...
    num_segments, ...
    f_signal, ...
    f_s, ...
    BW, ...
    plotAll, ...
    plotHold,...
    plotYN,...
    plotLin,...
    datNorm)

window = hanning(periodogram_length);
fft_of_window = fft(window);

psd_of_data_minus_sinusoid = zeros(periodogram_length, 1);
psd_of_sinusoid = zeros(periodogram_length, 1);
psd_of_sinusoid_HD2 = zeros(periodogram_length, 1);
psd_of_sinusoid_HD3 = zeros(periodogram_length, 1);

U = mean(window.^2);
f_normalized = f_signal / f_s;
f_normalized_HD2 = 2*f_signal / f_s;
f_normalized_HD3 = 3*f_signal / f_s;

% Average num_segments periodograms of length periodogram_length to
% estimate PSDs of data
for k = 1: num_segments 
    
    data_segment = data(1+(k-1)*periodogram_length : k*periodogram_length);
    
    [windowed_sinusoid, windowed_data_minus_sinusoid] =...
        remove_sinusoid(data_segment, window, f_normalized);
    
    fft_of_sinusoid = fft(windowed_sinusoid);
    fft_of_data_minus_sinusoid = fft(windowed_data_minus_sinusoid);
    
    data_minus_sinusoid_periodogram = abs((fft_of_data_minus_sinusoid).^2)...
        / (U * periodogram_length);
    sinusoid_periodogram = abs((fft_of_sinusoid).^2) / (U * periodogram_length);
    
    psd_of_data_minus_sinusoid = psd_of_data_minus_sinusoid + ...
        data_minus_sinusoid_periodogram;
    psd_of_sinusoid = psd_of_sinusoid + sinusoid_periodogram;
    
end
for k = 1: num_segments 
    
    data_segment = data(1+(k-1)*periodogram_length : k*periodogram_length);
    
    [windowed_sinusoid_HD2] =...
        remove_sinusoid(data_segment, window, f_normalized_HD2);
    
    fft_of_sinusoid_HD2 = fft(windowed_sinusoid_HD2);
    
    sinusoid_periodogram_HD2 = abs((fft_of_sinusoid_HD2).^2) / (U * periodogram_length);
    
    psd_of_sinusoid_HD2 = psd_of_sinusoid_HD2 + sinusoid_periodogram_HD2;
    
end
for k = 1: num_segments 
    
    data_segment = data(1+(k-1)*periodogram_length : k*periodogram_length);
    
    [windowed_sinusoid_HD3] =...
        remove_sinusoid(data_segment, window, f_normalized_HD3);
    
    fft_of_sinusoid_HD3 = fft(windowed_sinusoid_HD3);
    
    sinusoid_periodogram_HD3 = abs((fft_of_sinusoid_HD3).^2) / (U * periodogram_length);
    
    psd_of_sinusoid_HD3 = psd_of_sinusoid_HD3 + sinusoid_periodogram_HD3;
    
end
f_index=round(f_signal/f_s*periodogram_length+1);
% Compute signal power
sinusoid_power = sum(psd_of_sinusoid(1:periodogram_length/2) / (periodogram_length/2));
sinusoid_power_HD2 = sum(psd_of_sinusoid_HD2(1:periodogram_length/2) / (periodogram_length/2));
sinusoid_power_HD3 = sum(psd_of_sinusoid_HD3(1:periodogram_length/2) / (periodogram_length/2));
data_minus_sinusoid_power = sum(...
    (psd_of_data_minus_sinusoid(1:periodogram_length/2)) / (periodogram_length/2));

% Convert PSDs to units of dB / Hz (note that it is only necessary to plot
% half of the PSD)
epsilon = 1e-20;    % A really tiny number to avoid taking log of zero when
                    % converting to dB
sinusoid_spectrum = 10*log10(psd_of_sinusoid(1:periodogram_length/2) + epsilon);
data_minus_sinusoid_spectrum =...
    10*log10(psd_of_data_minus_sinusoid(1: periodogram_length/2) + epsilon);

% SUPPLEMENTALS
% Compute SNDR, ENOB*
BW_normalized = BW / f_s;
periodogram_length_BW = floor(periodogram_length * BW_normalized);
data_minus_sinusoid_in_BW_power = ...
   (sum(psd_of_data_minus_sinusoid(1:periodogram_length_BW)))/ (periodogram_length/2);
SNDR = 10*log10(sinusoid_power/data_minus_sinusoid_in_BW_power);
HD2 = 10*log10(sinusoid_power/sinusoid_power_HD2);
HD3 = 10*log10(sinusoid_power/sinusoid_power_HD3);
ENOB = (SNDR-1.76)/6.02;

% Total spectrum*
data_spectrum = 10*log10(psd_of_sinusoid(1:periodogram_length/2) + ...  
    psd_of_data_minus_sinusoid(1: periodogram_length/2) + epsilon);
if (datNorm==1)
data_spectrum = data_spectrum - max(sinusoid_spectrum);
end
% Plot
% Generate a frequency array to plot the PSDs against
f = zeros(1, periodogram_length/2);
for k = 1:periodogram_length/2
    f(k) = (k-1)/(periodogram_length);
end
f = f .* f_s;   % Un-normalized frequency

% Plot the PSDs
if plotYN == 1
    if plotAll == 1
        figure
        subplot(1,3,1)
        semilogx(f, sinusoid_spectrum)
        grid;
        zoom;
        title('Sinusoid Spectrum')
        ylabel('dB/Hz')
        xlabel('Frequency (Hz)')
        
        subplot(1,3,2)
        semilogx(f, data_minus_sinusoid_spectrum)
        grid;
        zoom;
        title('Data Minus Sinusoid Spectrum')
        ylabel('dB/Hz')
        xlabel('Frequency (Hz)')
        
        subplot(1,3,3)
        semilogx(f, data_spectrum)
        grid;
        zoom;
        title('Data Spectrum')
        ylabel('dB/Hz')
        xlabel('Frequency (Hz)')
    else
        if plotHold == 1
            if plotLin ==1
                plot(f, data_spectrum,'LineWidth',1.5)
                 grid on
                zoom;
            else
            semilogx(f, data_spectrum,'LineWidth',1.5)
            hold on
            grid on
            zoom;
            end
        else
             if plotLin ==1
             plot(f, data_spectrum,'LineWidth',1.5)
             grid on
             zoom;
             else
            figure
            semilogx(f, data_spectrum)
            grid on
            zoom;
             end
        end
        title('Data Spectrum','FontSize',20)
        ylabel('dB/Hz','FontSize',16)
        xlabel('Frequency (Hz)','FontSize',16)
    end
end
