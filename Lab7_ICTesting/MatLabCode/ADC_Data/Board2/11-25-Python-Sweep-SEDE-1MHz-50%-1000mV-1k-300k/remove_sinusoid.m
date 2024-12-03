% This function takes a data sequence assumed to be of the form
% x[n] = A*sin(2*pi*f_normalized*n + initial_phase) + e[n],
% where e[n] is noise, a window sequence of the same length, and
% f_normalized, and extracts the windowed sinusoid and a DC-free
% version of the windowed noise sequences based on the sinusoidal minimum
% error method (see ?Simulating and Testing Oversampled Analog-to-Digital
% Converters? by Bernhard Boser et al.)
%
% Source: ECE 264C HW#1 http://eceweb.ucsd.edu/courses/ECE264/FA_2017/
% User Name: ECE264C
% Password:ADCs_2017

function [windowed_signal_component, windowed_noise_component] = ...
    remove_sinusoid(data_segment, window, f_normalized)

n = 0:(length(data_segment) - 1);
W = exp(1j * 2 * pi * f_normalized);
windowed_data_segment = data_segment .* window;
denominator = ...
    (mean(window))^2 - mean(window'.*(W.^(-2 .* n))) * mean(window'.*(W.^(2 .* n)));

Y1 = (mean(windowed_data_segment .* (W.^(-n))') * mean(window) -...
    mean(windowed_data_segment .* (W.^(n))') * mean(window' .* (W.^(-2 .* n)))) /...
    denominator;

Ym1 = (mean(windowed_data_segment .* (W.^(n))') * mean(window) -...
    mean(windowed_data_segment .* (W.^(-n))') * mean(window' .* (W.^(2 .* n)))) /...
    denominator;

windowed_signal_component = window .* (Y1 * (W.^n)' + Ym1 *(W.^(-n)'));

windowed_noise_component_with_DC = windowed_data_segment - windowed_signal_component;

windowed_noise_component = ...
    windowed_noise_component_with_DC - window .* mean(windowed_data_segment) / mean(window);

end