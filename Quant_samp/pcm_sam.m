
% Complete MATLAB Solution for Exercise 6: A-Law, mu-Law, DPCM & Uniform PCM

clear; clc; close all;

% 1. Φόρτωση Αρχείου Ήχου (ή Συνθετικό Σήμα Test)
wav_filename = 'speech.wav';
if exist(wav_filename, 'file')
    [x, fs] = audioread(wav_filename);
    x = x(:, 1);                % Μετατροπή σε Mono αν είναι Stereo
else
    fs = 8000;
    t = (0 : 1/fs : 1.0)';
    x = 0.5 * sin(2*pi*300*t) .* exp(-2*t) + 0.3 * sin(2*pi*800*t) + 0.1 * randn(size(t));
end
x = x / max(abs(x));            % Κανονικοποίηση στο [-1, 1]
N = 256;                        % 8-bit κβάντιση (256 επίπεδα)

% 2. Uniform PCM (N = 256)
[x_unif, e_unif, sqnr_unif] = uniform_pcm(x, N);

% 3.  A-Law PCM (alpha = 87.6, N = 256)
alpha = 87.6;
[sqnr_alaw, a_quan, code, x_alaw] = alaw_pcm(x, N, alpha);
e_alaw = x - x_alaw;

%4. mu-Law PCM (mu = 255, N = 256)
mu = 255;
y_mu = compand(x, mu, max(abs(x)), 'mu/compressor');
[y_mu_q, ~, ~] = uniform_pcm(y_mu, N);
x_mulaw = compand(y_mu_q, mu, max(abs(x)), 'mu/expander');
e_mulaw = x - x_mulaw;
sqnr_mulaw = 10 * log10(sum(x.^2) / sum(e_mulaw.^2));

% 5.  Differential PCM (DPCM - 1ης Τάξης Προβλέπτης)
[x_dpcm, e_dpcm, sqnr_dpcm] = dpcm_quantize(x, N);

% 6. Εκτύπωση Συγκριτικού Πίνακα SQNR

fprintf(' SQNR COMPARISON (N = 256)   \n');

fprintf(' (α) Differential PCM (DPCM):     %6.2f dB\n', sqnr_dpcm);
fprintf(' (β) mu-Law PCM (mu = 255):   %6.2f dB\n', sqnr_mulaw);
fprintf(' (γ) A-Law PCM (alpha = 87.6):  %6.2f dB\n', sqnr_alaw);
fprintf(' (δ) Uniform PCM (N = 256):   %6.2f dB\n', sqnr_unif);


%7. Γραφήματα Σφάλματος Κβάντισης e[n]
t_plot = (0 : length(x) - 1) / fs;
idx = 1 : min(800, length(x));

figure('Name', 'Quantization Error Waveforms', 'Color', 'w', 'Position', [100, 100, 950, 800]);

subplot(4, 1, 1);
plot(t_plot(idx), e_dpcm(idx), 'r');
title(sprintf('(α) DPCM Error Waveform (SQNR = %.2f dB)', sqnr_dpcm));
ylabel('Error e[n]'); grid on;

subplot(4, 1, 2);
plot(t_plot(idx), e_mulaw(idx), 'b');
title(sprintf('(β) \\mu-Law Error Waveform (SQNR = %.2f dB)', sqnr_mulaw));
ylabel('Error e[n]'); grid on;

subplot(4, 1, 3);
plot(t_plot(idx), e_alaw(idx), 'g');
title(sprintf('(γ) A-Law Error Waveform (SQNR = %.2f dB)', sqnr_alaw));
ylabel('Error e[n]'); grid on;

subplot(4, 1, 4);
plot(t_plot(idx), e_unif(idx), 'm');
title(sprintf('(δ) Uniform PCM Error Waveform (SQNR = %.2f dB)', sqnr_unif));
xlabel('Χρόνος (s)'); ylabel('Error e[n]'); grid on;



%%
function [sqnr, a_quan, code, x_rec] = alaw_pcm(a, n, alpha)
    y = zeros(size(a));
    thresh = 1 / alpha;
    idx1 = abs(a) < thresh;
    idx2 = abs(a) >= thresh;
    y(idx1) = sign(a(idx1)) .* (alpha * abs(a(idx1))) / (1 + log(alpha));
    y(idx2) = sign(a(idx2)) .* (1 + log(alpha * abs(a(idx2)))) / (1 + log(alpha));
    
    [a_quan, ~, ~] = uniform_pcm(y, n);
    code = a_quan;
    x_rec = invalaw(a_quan, alpha);
    sqnr = 10 * log10(sum(a.^2) / sum((a - x_rec).^2));
end
%%
function x = invalaw(y, alpha)
    x = zeros(size(y));
    thresh = 1 / (1 + log(alpha));
    idx1 = abs(y) < thresh;
    idx2 = abs(y) >= thresh;
    x(idx1) = sign(y(idx1)) .* (abs(y(idx1)) * (1 + log(alpha))) / alpha;
    x(idx2) = sign(y(idx2)) .* (exp(abs(y(idx2)) * (1 + log(alpha)) - 1)) / alpha;
end
%%
function [x_rec, e, sqnr] = uniform_pcm(x, N)
    step = 2 / N;
    levels = -1 + step/2 : step : 1 - step/2;
    idx = round((x + 1) / step) + 1;
    idx = max(min(idx, N), 1);
    x_rec = levels(idx)';
    e = x - x_rec;
    sqnr = 10 * log10(sum(x.^2) / sum(e.^2));
end
%%
function [x_rec, e, sqnr] = dpcm_quantize(x, N)
    L = length(x);
    x_rec = zeros(L, 1);
    pred = 0;
    e = zeros(L, 1);
    
    step = 1 / N; 
    levels = -0.5 + step/2 : step : 0.5 - step/2;
    
    for k = 1:L
        diff = x(k) - pred;
        idx = round((diff + 0.5) / step) + 1;
        idx = max(min(idx, N), 1);
        dq = levels(idx);
        x_rec(k) = pred + dq;
        pred = x_rec(k);
        e(k) = x(k) - x_rec(k);
    end
    sqnr = 10 * log10(sum(x.^2) / sum(e.^2));
end