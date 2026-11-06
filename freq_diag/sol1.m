% spectrum
% Compute and plot the magnitude and phase spectra of the signal:

% x(t) = 2,     -3 <= t <= -2
%        |t|+2, |t| < 2
%        1.5,   2 <= t < 3
%        0,     otherwise
%
% The Fourier transform X(jω) is approximated numerically using the FFT.

clear; close all; clc;

% 1. Define the time interval and signal.
dt = 0.001; % Sampling interval (1 ms).
t = -5:dt:5; % Time interval containing the entire signal.
x = zeros(size(t)); % Initialize the signal.

% Define the piecewise signal.
x(t >= -3 & t <= -2) = 2;
x(abs(t) < 2) = abs(t(abs(t) < 2)) + 2;
x(t >= 2 & t <= 3) = 1.5;

% Plot the time-domain signal.
figure('Name', 'Time-Domain Signal x(t)');
plot(t, x, 'LineWidth',1.4);
xlabel('t (s)'); ylabel('x(t)');
title('Time-Domain Signal x(t)');
grid on; xlim([-4 4]);

% 2. Approximate the continuous Fourier transform using the FFT.
% Zero-padding makes the frequency grid denser, but does not improve the
% underlying frequency resolution.
N = 2^15; % FFT size (power of two).
fs = 1/dt; % Sampling frequency (Hz).
X = dt * fftshift(fft(x, N));

% Frequency axes.
f = (-N/2:N/2-1) * (fs/N); % Hz.
omega = 2 * pi * f; % rad/s.

% Correct for the time axis starting at t(1), rather than at zero.
X = X .* exp(-1j * omega * t(1));

% Compute magnitude and wrapped phase.
magX = abs(X);
phaseX = angle(X);

% Hide phase where the magnitude is small and the phase is unreliable.
thresh = max(magX) * 1e-2;
phaseX(magX < thresh) = NaN;

% 3. Plot the magnitude and phase spectra.

% Magnitude spectrum.
figure('Name', 'Magnitude Spectrum');
plot(omega, magX, 'LineWidth',1.3);
xlabel('\omega (rad/s)');
ylabel('|X(j\omega)|');
title('Magnitude Spectrum |X(j\omega)|');
grid on; xlim([-50 50]);

% Wrapped phase spectrum (radians).
figure('Name', 'Phase Spectrum');
idx = magX >= thresh;
plot(omega(idx), phaseX(idx), 'LineWidth',1.3);
xlabel('\omega (rad/s)');
ylabel('Phase (rad)');
title('Phase Spectrum \angle X(j\omega)');
grid on; xlim([-50 50]);

% 4. Report completion in the Command Window.
fprintf('Fourier transform approximation completed.\n');
fprintf('  Sampling interval dt = %.4f s, FFT size = %d\n', dt, N);
fprintf('  The plots show the frequency range [-50, 50] rad/s.\n');
fprintf('  Phase is shown wrapped in [-pi, pi] and omitted at low magnitudes.\n');