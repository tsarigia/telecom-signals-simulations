
% Uniform Quantizer & SQNR Evaluation

clear; clc; close all;

% 1. Ορισμός Σήματος & Setup Δειγματοληψίας
fs = 10000;                     % Συχνότητα δειγματοληψίας 10 kHz
t = (0 : 1/fs : 2 - 1/fs)';     % Μία πλήρης περίοδος T = 2.0 s
N = length(t);

% Περιοδικό Τριγωνικό Σήμα x(t) στο εύρος [0, 1] V
x = zeros(size(t));
idx1 = (t >= 0.0 & t < 1.0);
idx2 = (t >= 1.0 & t < 2.0);
x(idx1) = t(idx1);
x(idx2) = -t(idx2) + 2.0;

% Υπολογισμός Ισχύος Σήματος
Px_sim = sum(x.^2) / N;
Px_theo = 1/3;

% 2. Αξιολόγηση για Πολλαπλά Επίπεδα Κβάντισης M = [8, 16, 32, 64, 128]
M_values = [8, 16, 32, 64, 128];
num_M = length(M_values);

sqnr_sim = zeros(num_M, 1);
sqnr_theo = zeros(num_M, 1);

fprintf(' UNIFORM QUANTIZER SQNR ANALYSIS (T = 2s, [0,1]) \n');
fprintf('  M   | Bits (R)  | Step Size (Delta)  |  Simulated  | Theoretical \n');

for k = 1:num_M
    M = M_values(k);
    R = log2(M);
    delta = 1.0 / M;
    
    % Mid-rise ομοιόμορφος κβαντιστής για το εύρος [0, 1]
    levels = (0.5 : 1 : M - 0.5) * delta;
    bin_idx = floor(x / delta) + 1;
    bin_idx = max(min(bin_idx, M), 1);
    
    xq = levels(bin_idx)';
    error = x - xq;
    
    % Υπολογισμοί SQNR
    Pe_sim = sum(error.^2) / N;
    sqnr_sim(k) = 10 * log10(Px_sim / Pe_sim);
    sqnr_theo(k) = 10 * log10(4 * M^2);
    
    fprintf(' %3d   |  %3d bits  |      %.6f V      |  %6.2f dB  |  %6.2f dB  \n', ...
            M, R, delta, sqnr_sim(k), sqnr_theo(k));
end

% 3. Γραφήματα Ανάλυσης για M = 8 
M8 = 8;
delta8 = 1 / M8;
bin8 = max(min(floor(x / delta8) + 1, M8), 1);
xq8 = ((0.5 : 1 : M8 - 0.5) * delta8);
xq8_sig = xq8(bin8)';
e8 = x - xq8_sig;

figure('Name', ' Quantizer Analysis for M = 8', 'Color', 'w', 'Position', [100, 100, 950, 750]);

subplot(3, 1, 1);
plot(t, x, 'b--', 'LineWidth', 1.5); hold on;
plot(t, xq8_sig, 'r', 'LineWidth', 1.5);
title('Αρχικό Σήμα x(t) και Κβαντισμένη Έξοδος x_q(t) (M = 8)');
ylabel('Πλάτος (V)'); legend('Αρχικό x(t)', 'Κβαντισμένο x_q(t)');
grid on;

subplot(3, 1, 2);
plot(x, xq8_sig, 'g', 'LineWidth', 2);
title(' Χαρακτηριστική Μεταφοράς Κβαντιστή (M = 8)');
xlabel('Είσοδος x(t) [V]'); ylabel('Κβαντισμένη Έξοδος x_q(t) [V]');
grid on;

subplot(3, 1, 3);
plot(t, e8, 'm', 'LineWidth', 1.2);
title(sprintf(' Σφάλμα Κβάντισης e(t) = x(t) - x_q(t) [SQNR = %.2f dB]', sqnr_sim(1)));
xlabel('Χρόνος t (s)'); ylabel('Σφάλμα e(t) [V]');
ylim([-delta8 delta8]); grid on;

% 4. Επαλήθευση του Νόμου 6.02 dB/Bit 
figure('Name', 'SQNR vs Resolution (6.02 dB/bit Rule)', 'Color', 'w', 'Position', [150, 150, 850, 500]);
plot(log2(M_values), sqnr_theo, 'k--', 'LineWidth', 2, 'Marker', 'o', 'DisplayName', 'Θεωρητικό SQNR (6.02 dB/bit)'); hold on;
plot(log2(M_values), sqnr_sim, 'rx', 'MarkerSize', 10, 'LineWidth', 2, 'DisplayName', 'Προσομοίωση SQNR');
title(' SQNR ως συνάρτηση Ανάλυσης R (Νόμος 6.02 dB/Bit)');
xlabel('Ανάλυση R (Bits = log_2(M))'); ylabel('SQNR (dB)');
legend('Location', 'northwest'); grid on;