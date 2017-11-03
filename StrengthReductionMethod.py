import math as m
#Area of 1 corner
Ar = r**2*(1-m.pi/4)
#Moment of inertia corner
Ir = 0.00742*r**4
#Distance to center of gravity corner
sr = 0.223*r

#In case of fire exposed sides type 4
#Cross section area
A = []
S = []
dr = []
Isq = []
Icr = []
Itot = []
Pr = []
for i in range(len(W)):
    A.append(W[i]*H[i]-2*Ar)
    #Static moment about original axis
    S.append(Ar*(H[i]/2-sr))
    #Displacement of axis for corners
    dr.append(S[i]/A[i])
    #Moment of inertia
    #For rectangel
    Isq.append(1/12*W[i]*(H[i]-2*dr[i])**3+1/12*W[i]*(2*dr[i])**3+W[i]*2*dr[i]*(H[i]/2)**2)
    #For corner
    Icr.append(2*Ir+Ar*((H[i]/2)+dr[i]-0.223*r)**2)
    #Total moment of inertia for cross section
    Itot.append(Isq[i]-Icr[i])
    #Perimeter
    Pr.append(2*(H[i]-2*r)+(W[i]-2*r)+(W[i]-4*r)+(2*(m.pi*r*2)/4))
