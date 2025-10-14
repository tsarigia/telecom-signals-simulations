function xx=fseries(funfcn,a,b,n,tol,p1,p2,p3)
%FSERIES    Returns the Fourier series coefficients.
%       XX=FSERIES(FUNFCN,A,B,N,TOL,P1,P2,P3)
%       funfcn=the given function, in an m-file.
%       It can depend on up to three parameters
%       p1,p2, and p3. The function is given
%       over one period extending from 'a' to 'b'
%       xx=vector of length n+1 of Fourier Series
%       Coefficients, xx0,xx1,...,xxn.
%       p1,p2,p3=parameters of funfcn. 
%       tol=the error level.

j=sqrt(-1);% Ορισμός φανταστικής μονάδας
args0=[]; % Δημιουργία λίστας επιπλέον παραμέτρων
% Αν υπάρχουν p1,p2,p3, τα προσθέτει στη λίστα κλήσης
for nn=1:nargin-5
  args0=[args0,',p',int2str(nn)];
end
args=[args0,')'];
t=b-a;
% ---- Υπολογισμός συντελεστή c0 ----
xx(1)=eval(['1/(',num2str(t),').*quad(funfcn,a,b,tol,[]',args]) 
% Χρησιμοποιεί την ενσωματωμένη quad (numerical integration)
% c0 = (1/T)*∫ f(x) dx

% ---- Υπολογισμός συντελεστών ck για k=1:n ----
for i=1:n
  new_fun = 'exp_fnct' ;   % Συνάρτηση που πολλαπλασιάζει με e^{-j2πkx/T}
  args=[',', num2str(i), ',', num2str(t), args0, ')' ] ;%Δημιουργεί αλφαριθμητικό (string) που περιέχει τα ορίσματα που θα περαστούν στη exp_fnct.
  xx(i+1)=eval(['1/(',num2str(t),').*quad(new_fun,a,b,tol,[],funfcn',args]);
end
%Καλεί τη quad για να ολοκληρώσει τη συνάρτηση exp_fnct από a έως b, με ανοχή σφάλματος tol.
%1/('num2str(t)')Πολλαπλασιάζει με 1/T (όπως στον ορισμό του cₖ).
%Χρησιμοποιεί eval για να μετατρέψει το αλφαριθμητικό σε MATLAB εντολή και να την εκτελέσει.
%xx(i+1)Αποθηκεύει το αποτέλεσμα (συντελεστής cᵢ) στο διάνυσμα xx.