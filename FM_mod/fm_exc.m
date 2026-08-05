
%  FM Modulation & Carson's Rule

clear; clc; close all;

% 1. Παράμετροι & Σήμα Πληροφορίας
fs = 20000;                     % Συχνότητα δειγματοληψίας 20 kHz
t = (0 : 1/fs : 2.5 - 1/fs)';   % Χρονικός άξονας [0, 2.5) s
N = length(t);

% Σήμα πληροφορίας m(t)
m = 0.1 * ones(size(t));
idx_up   = (t >= 0.0 & t < 1.0);
idx_down = (t >= 1.0 & t < 2.0);
m(idx_up)   = t(idx_up);
m(idx_down) = -t(idx_down) + 2.0;

% 2. FM Διαμόρφωση & Υπολογισμοί Carson
fc = 1000;                      % Συχνότητα φέροντος 1000 Hz
kf = 25;                        % Σταθερά απόκλισης 25 Hz/V
Ac = 1.0;

% Ολοκλήρωμα του σήματος μηνύματος για τη στιγμιαία φάση
int_m = cumtrapz(t, m);
s_fm = Ac * cos(2 * pi * fc * t + 2 * pi * kf * int_m);
c = Ac * cos(2 * pi * fc * t);

% Θεωρητικοί υπολογισμοί
delta_f = kf * max(abs(m));     % Μέγιστη απόκλιση συχνότητας: 25 Hz
B_m = 1.0;                      % Πρακτικό εύρος ζώνης μηνύματος: 1 Hz
beta = delta_f / B_m;           % Δείκτης διαμόρφωσης: 25
B_carson = 2 * (delta_f + B_m); % Εύρος Carson: 52 Hz

% 3. Φάσματα FFT
f = (-N/2 : N/2 - 1)' * (fs / N);
M_f  = fftshift(fft(m)) / N;
C_f  = fftshift(fft(c)) / N;
SFM_f = fftshift(fft(s_fm)) / N;

% 4. Γραφήματα Πεδίου Χρόνου
figure('Name', 'FM Time Domain Waveforms', 'Color', 'w', 'Position', [100, 100, 950, 750]);

subplot(3, 1, 1);
plot(t, m, 'b', 'LineWidth', 1.5);
title('Σήμα Πληροφορίας m(t)');
xlabel('Χρόνος (s)'); ylabel('Πλάτος (V)'); grid on;

subplot(3, 1, 2);
plot(t, c, 'g', 'LineWidth', 1.0);
title('Αδιαμόρφωτο Φέρον c(t) [Εστίαση 0.8s - 1.2s, fc = 1000 Hz]');
xlabel('Χρόνος (s)'); ylabel('Πλάτος (V)');
xlim([0.8, 1.2]); grid on;

subplot(3, 1, 3);
plot(t, s_fm, 'r', 'LineWidth', 1.0);
title('Διαμορφωμένο Σήμα s_{FM}(t) [Εστίαση 0.8s - 1.2s]');
xlabel('Χρόνος (s)'); ylabel('Πλάτος (V)');
xlim([0.8, 1.2]); grid on;

% 5. Γραφήματα Πεδίου Συχνότητας & Κανόνας Carson
figure('Name', 'FM Frequency Spectra & Carson Rule', 'Color', 'w', 'Position', [150, 150, 950, 750]);

subplot(3, 1, 1);
plot(f, abs(M_f), 'b', 'LineWidth', 1.5);
title('Φάσμα Μηνύματος |M(f)| (Baseband)');
xlabel('Συχνότητα (Hz)'); ylabel('Πλάτος');
xlim([-10, 10]); grid on;

subplot(3, 1, 2);
plot(f, abs(C_f), 'g', 'LineWidth', 1.5);
title('Φάσμα Φέροντος |C(f)| (1000 Hz)');
xlabel('Συχνότητα (Hz)'); ylabel('Πλάτος');
xlim([950, 1050]); grid on;

subplot(3, 1, 3);
plot(f, abs(SFM_f), 'r', 'LineWidth', 1.5); hold on;
xline(fc - B_carson/2, 'k--', 'LineWidth', 1.5, 'DisplayName', 'Όρια Carson (±26 Hz)');
xline(fc + B_carson/2, 'k--', 'LineWidth', 1.5);
title(sprintf('Φάσμα FM |S_{FM}(f)| & Εύρος Carson (B_{FM} \\approx %.1f Hz)', B_carson));
xlabel('Συχνότητα (Hz)'); ylabel('Πλάτος');
xlim([950, 1050]); legend; grid on;