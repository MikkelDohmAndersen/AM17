import math as m
#Corner
Ar = r**2*(1-m.pi/4)
Ir = 0.00742*r**4
sr = 0.223*r

#Cross section area
A = []
for i in range(len(W)):
    A.append(W[i]*H[i]-Ar)

#In case of fire exposed sides type 4
#Static moment about original axis
S = Ar*(H/2-sr)
#Displacement of axis for corners
dr = S/A
#print(dr)

#Moment of inertia
#For rectangel
Isq = 1/12*W*(H-2*dr)**3+1/12*W*(2*dr)**3+W*2*dr*(H/2)**2
print(Isq)
#For corner
Icr = 2*Ir+Ar*(H/2*dr-0.223*r)**2
#Total moment of inertia for cross section
Itot = Isq-Icr
print(Itot)

Pr = 2*H+W-((4-m.pi)**2)
print(Pr)