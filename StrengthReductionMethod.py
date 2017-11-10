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
Sh = []     #Static moment about original axis case 3
Sw = []     #Static moment about original axis case 3
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
#Width, Height, 2*Width, 2*Height same calculations
if z==1 or z==2 or z==6 or z== 7:  
    for i in range(len(W)):
        Iytot.append(1/12*W[i]*H[i]**3)
        Iztot.append(1/12*H[i]*W[i]**3)
        Pr.append(2*W[i]+2*H[i])
        Ar.append(W[i]*H[i])
#Width + Height
elif z==3:
    for i in range(len(W)):
        A.append(W[i]*H[i]-Acr)
        Sh.append(Acr*(H[i]/2-sr))
        drh.append(Sh[i]/A[i])
        Iysq.append(1/12*W[i]*(H[i]-2*drh[i])**3+1/12*W[i]*(2*drh[i])**3+W[i]*2*drh[i]*(H[i]/2)**2)
        Iycr.append(Ir+Acr*((H[i]/2)+drh[i]-sr)**2)
        Iytot.append(Iysq[i]-Iycr[i])
        Sw.append(Acr*(W[i]/2-sr))
        drw.append(Sw[i]/A[i])
        Izsq.append(1/12*H[i]*(W[i]-2*drh[i])**3+1/12*H[i]*(2*drh[i])**3+H[i]*2*drh[i]*(W[i]/2)**2)
        Iycr.append(Ir+Acr*((W[i]/2)+drw[i]-sr)**2)
        Iztot.append(Izsq[i]-Izcr[i])
        Pr.append(H[i]+(H[i]-r)+W[i]+(W[i]-r)+(m.pi*r*2)/4)
        Ar.append(H[i]*W[i]-Acr)
#Width + 2*Height 
elif z==4: 
    for i in range(len(W)):
        A.append(W[i]*H[i]-2*Acr)
        S.append(2*Acr*(H[i]/2-sr))
        dr.append(S[i]/A[i])
        Iysq.append(1/12*W[i]*(H[i]-2*dr[i])**3+1/12*W[i]*(2*dr[i])**3+W[i]*2*dr[i]*(H[i]/2)**2)
        Iycr.append(2*Ir+2*Acr*((H[i]/2)+dr[i]-0.223*r)**2)
        Iytot.append(Iysq[i]-Iycr[i])
        Izsq.append((1/12*H[i]*W[i]**3))
        Izcr.append(2*Ir+2*Acr*((W[i]/2)-0.223*r)**2)
        Iztot.append(Izsq[i]-Izcr[i])
        Pr.append((W[i])+2*(H[i]-r)+(W[i]-2*r)+(2*(m.pi*r*2)/4))
        Ar.append(W[i]*H[i]-2*Acr)
#2*Width + Height
elif z==5:
    for i in range(len(W)):
        A.append(H[i]*W[i]-2*Acr)
        S.append(2*Acr*(W[i]/2-sr))
        dr.append(S[i]/A[i])
        Iysq.append(1/12*H[i]*(W[i]-2*dr[i])**3+1/12*H[i]*(2*dr[i])**3+H[i]*2*dr[i]*(W[i]/2)**2)
        Iycr.append(2*Ir+2*Acr*((W[i]/2)+dr[i]-0.223*r)**2)
        Iytot.append(Iysq-Iycr)
        Izsq.append((1/12*W[i]*H[i]**3))
        Izcr.append(2*Ir+2*Acr*((H[i]/2)-0.223*r)**2)
        Iztot.append(Izsq-Izcr)
        Pr.append((H[i]+2*(W[i]-r)+(H[i]-2*r)+(2*(m.pi*r*2)/4)))
        Ar.append(H[i]*W[i]-2*Acr)
#2*Width + 2*Height
elif z==8: 
    for i in range(len(W)):
        Iytot.append(1/12*W[i]*H[i]**3-r**2*(4-m.pi)*(H[i]/2-sr)**2-4*Ir)
        Iztot.append(1/12*H[i]*W[i]**3-r**2*(4-m.pi)*(W[i]/2-sr)**2-4*Ir)
        Pr.append(2*(H[i]-2*r)+2*(W[i]-2*r)+m.pi*r*2)
        Ar.append(W[i]*H[i]-4*Acr)
else:
    print('You are doing something wrong')
Iy=Iytot
Iz=Iztot