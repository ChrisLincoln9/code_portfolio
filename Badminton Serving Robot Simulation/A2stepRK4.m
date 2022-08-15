function znext = A2stepRK4(t,z,dt,k1,k2)
% [REFERENCE]
dz = A2stateDeriv(t,z,k1,k2);

A = dt * dz;
B = dt *(dz+A/2);
C = dt *(dz+B/2);
D = dt *(dz+C);

znext = z + (A+2*B+2*C+D)/6;


end