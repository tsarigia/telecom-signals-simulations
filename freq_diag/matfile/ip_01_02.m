% MATLAB script for Illustrative Problem 1.2.
echo on;   % Ενεργοποιεί εμφάνιση κάθε εντολής στο Command Window
fnct='lambda'; % Δηλώνει ότι η συνάρτηση του σήματος είναι το αρχείο lambda.m
a=-4;% Αρχή διαστήματος μίας περιόδου
b=4;
n=24; % Αριθμός συντελεστών (μέχρι c_24)
tol=1e-6;% Ανοχή σφάλματος για την αριθμητική ολοκλήρωση
xx=fseries(fnct,a,b,n,tol); % Υπολογισμός συντελεστών Fourier σειράς για τη συνάρτηση fnct

xx1=xx(n+1:-1:2); % Αντιστροφή για να δημιουργηθεί συμμετρία (αρνητικές συχνότητες)
xx1=[conj(xx1),xx];
absxx1=abs(xx1); % Υπολογισμός μέτρου κάθε συντελεστή (πλάτος)

pause % Press any key to see a plot of the magnitude spectrum.
n1=[-n:n]; % Δείκτες για k = -n,...,n
stem(n1,absxx1) % Stem διάγραμμα (ραβδάκια) πλάτους |c_k|
title('The Discrete Magnitude Spectrum')

phasexx1=angle(xx1); % Υπολογισμός φάσης κάθε συντελεστή
pause % Press any key to see a plot of the phase.
stem(n1,phasexx1) % Stem διάγραμμα φάσης ∠c_k
title('The Discrete Phase Spectrum')

%Για περιοδικό σήμα υπολογίζει τους συντελεστές σειράς Fourier 𝑐𝑘, σήμα με περίοδο 𝑇=𝑏−𝑎 και σχεδιάζει τα διακριτά φάσματα πλάτους και φάσης.