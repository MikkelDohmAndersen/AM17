import math as m
#Area of 1 corner
Acr = r**2*(1-m.pi/4)
#Moment of inertia corner
Ir = 0.00742*r**4
#Distance to center of gravity corner
sr = 0.223*r

#Lists for calculation
A = []      #Cross section area
S = []      #Static moment about original axis
dr = []     #Displacement of axis for corners
Iysq = []   #Moment of inertia around z axis rectangle
Izsq = []   #Moment of inertia around y axis rectangle
Iycr = []   #Moment of inertia corner z axis corner
Izcr = []   #Moment of inertia corner y axis corner
Iytot = []  #Moment of inertia combined z axis total
Iztot = []  #Moment of inertia combined y axis total
Pr = []     #Perimeter
Ar = []     #Area of cross section with rounded corners
#Sides exposed to fire
if z==1:    #Width
    for i in range(len(W)):
        Iytot.append(1/12*W[i]*H[i]**3)
        Iztot.append(1/12*H[i]*W[i]**3)
        Pr.append(2*W[i]+2*H[i]-r)
        Ar.append(W[i]*(H[i]-r))
elif z==2:  #Height
    print('Undergoing construction')
elif z==3:  #Width + Height
    print('Undergoing construction')
elif z==4:  #Width + 2*Height 
    for i in range(len(W)):
        A.append(W[i]*H[i]-2*Acr)
        S.append(Acr*(H[i]/2-sr))
        dr.append(S[i]/A[i])
        Iysq.append(1/12*W[i]*(H[i]-2*dr[i])**3+1/12*W[i]*(2*dr[i])**3+W[i]*2*dr[i]*(H[i]/2)**2)
        Icr.append(2*Ir+Acr*((H[i]/2)+dr[i]-0.223*r)**2)
        Itot.append(Iysq[i]-Icr[i])
        Pr.append(2*(H[i]-2*r)+(W[i]-2*r)+(W[i]-4*r)+(2*(m.pi*r*2)/4))
        Ar.append(W[i]*H[i]-2*Acr)
elif z==5:  #2*Width + Height
    print('Undergoing construction')
elif z==6:  #2*Width
    print('Undergoing construction')
elif z==7:  #2*Height
    print('Undergoing construction')
elif z==8:  #2*Width + 2*Height
    print('Undergoing construction')
else:
    print('You are doing something wrong')