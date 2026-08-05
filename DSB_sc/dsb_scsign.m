% dsbsc_modulation.m
% Complete MATLAB Solution for Exercise 4: DSB-SC Modulation & Zero-Phase Filtering

clear; clc; close all;

%1. Παράμετροι και Σήμα Πληροφορίας m(t)
fs = 10000;                     % Συχνότητα δειγματοληψίας 10 kHz
t = (0 : 1/fs : 2.5 - 1/fs)';   % Χρονικός άξονας [0, 2.5) s
N = length(t);

% Τμηματικά γραμμικό τρίγωνο m(t)
m = zeros(size(t));
idx_ramp_up   = (t >= 0.0 & t < 1.0);
idx_ramp_down = (t >= 1.0 & t < 2.0);
m(idx_ramp_up)   = t(idx_ramp_up);
m(idx_ramp_down) = -t(idx_ramp_down) + 2.0;

% 2. Φέρον Σήμα & Διαμόρφωση DSB-SC
fc = 35;                        % Συχνότητα φέροντος 35 Hz
c = cos(2 * pi * fc * t);
s = m .* c;                     % Διαμορφωμένο σήμα DSB-SC

% 3. Αποδιαμόρφωση (Σύμφωνος Φωρατής) & Φιλτράρισμα Zero-Phase
v = s .* c;                     % Πολλαπλασιασμός με το τοπικό φέρον

% Σχεδιασμός Βαθυπερατού Φίλτρου Butterworth 4ης τάξης (cutoff στα 5 Hz)
[b, a] = butter(4, 5 / (fs / 2), 'low');

% Φιλτράρισμα μηδενικής φάσης (0 ms καθυστέρηση) και ενίσχυση x2
m_rec = 2 * filtfilt(b, a, v);

% 4. Υπολογισμός Φασμάτων (FFT)
f = (-N/2 : N/2 - 1)' * (fs / N);
M_f = fftshift(fft(m)) / N;
C_f = fftshift(fft(c)) / N;
S_f = fftshift(fft(s)) / N;

% 5. Γραφήματα Πεδίου Χρόνου
figure('Name', 'DSB-SC Time Domain & Demodulation', 'Color', 'w', 'Position', [100, 100, 950, 750]);

subplot(3, 1, 1);
plot(t, m, 'b', 'LineWidth', 1.5);
title('Σήμα Πληροφορίας m(t)');
xlabel('Χρόνος (s)'); ylabel('Πλάτος (V)'); grid on;

subplot(3, 1, 2);
plot(t, s, 'r', 'LineWidth', 1.2); hold on;
plot(t, m, 'b--', 'LineWidth', 1.0);
plot(t, -m, 'b--', 'LineWidth', 1.0);
title('Διαμορφωμένο Σήμα DSB-SC s(t) με Περιβάλλουσα');
xlabel('Χρόνος (s)'); ylabel('Πλάτος (V)'); grid on;

subplot(3, 1, 3);
plot(t, m, 'b--', 'LineWidth', 1.5); hold on;
plot(t, m_rec, 'g', 'LineWidth', 1.5);
title('Ανακτημένο Σήμα m_{rec}(t) (Zero-Phase Filtering: 0 ms Καθυστέρηση)');
xlabel('Χρόνος (s)'); ylabel('Πλάτος (V)');
legend('Αρχικό m(t)', 'Ανακτημένο m_{rec}(t)'); grid on;

% 6. Γραφήματα Πεδίου Συχνότητας
figure('Name', 'DSB-SC Frequency Domain Spectra', 'Color', 'w', 'Position', [150, 150, 950, 750]);

subplot(3, 1, 1);
plot(f, abs(M_f), 'b', 'LineWidth', 1.5);
title('Φάσμα Σήματος Πληροφορίας |M(f)|');
xlabel('Συχνότητα (Hz)'); ylabel('Πλάτος');
xlim([-100, 100]); grid on;

subplot(3, 1, 2);
plot(f, abs(C_f), 'k', 'LineWidth', 1.5);
title('Φάσμα Φέροντος |C(f)| (±35 Hz)');
xlabel('Συχνότητα (Hz)'); ylabel('Πλάτος');
xlim([-100, 100]); grid on;

subplot(3, 1, 3);
plot(f, abs(S_f), 'r', 'LineWidth', 1.5);
title('Φάσμα Διαμορφωμένου Σήματος |S(f)| (Πλευρικές Ζώνες γύρω από ±35 Hz)');
xlabel('Συχνότητα (Hz)'); ylabel('Πλάτος');
xlim([-100, 100]); grid on;