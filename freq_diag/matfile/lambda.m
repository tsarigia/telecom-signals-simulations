function y=lambda(x)
%		y=lambda(x) generates a triangular signal.% y=lambda(x) δημιουργεί ένα τριγωνικό σήμα στο διάστημα (-1,1)
y=(x+1).*(x>-1 & x<0)+(x==0)+(-x+1).*(x>0 & x<1);
