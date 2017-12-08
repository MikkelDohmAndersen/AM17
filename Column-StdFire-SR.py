﻿"""
Column - Standard fire with reduced cross section method

    Args:
        CL: Center Line for column
        F: Vertical load,N, for the column to support (Calculated as a centrally placed load, also in the case when the column's center of gravity moves)
        Str: Strength class for the wood (C30, C24, C18, C14, GL32h, GL28h or GL24h)
        Sup: Support conditions for the column (1=Simply supported both ends, 2=One end fixed and one end not supported, 3=One end fixed and one end simply supported, 4=Both ends fixed
        ToW: Type of Wood; Sawn, Planed or Glulam (Glued laminated timber) standard profiles.
        WidthProfile: Width of profile [mm] to calculate NRc,fire for. If no value is inserted, the NRc,fire is calculated on ToW.
        HeightProfile: Height of profile [mm] to calculate NRc,fire for. If no value is inserted, the NRc,fire is calculated on ToW.
        WS: Wood Species (1=Conifer p>290 kg/m3, 2=Laminated wood p>290 kg/m3 , 3=Hardwood p>450 kg/m3, 4=Plywood with a thickness d>20 mm and density p>450 kg/m3
        t: Time of exposure in minutes
        SEF: Sides Exposed to Fire(1=Width, 2=Height, 3=Width+Height, 4=Width+2*Height, 5=2*Width+Height, 6=2*Width, 7=2*Height, 8=All
    Returns:
        NRc,fire: Charateristic resistance of the column after fire
        Width: Width of the cross section before fire
        Height: Height of the cross section before fire
        Geo: 3D model of the cross section
        Utilization: Utilization rate [%]
        ErrorMessage: Check this output for error messages

"""

import rhinoscriptsyntax as rs
import math as m

"""-------------------------------------------------------------------------"""
# USER INPUTS
# Support conditions
if Sup==1:
    l0=1
elif Sup==2:
    l0=2
elif Sup==3:
    l0=0.699
elif Sup==4:
    l0=1/2
else:
    l0=1

# Strength class
if str.upper(Str)=='C30':
    fm=30
    fc=23
    E=8000
elif str.upper(Str)=='C24':
    fm=24
    fc=21
    E=7400
elif str.upper(Str)=='C18':
    fm=18
    fc=18
    E=6000
elif str.upper(Str)=='C14':
    fm=14
    fc=16
    E=4700
elif str.upper(Str)=='GL32H':
    fm=32
    fc=29
    E=11100
elif str.upper(Str)=='GL28H':
    fm=38
    fc=26.5
    E=10200
elif str.upper(Str)=='GL24H':
    fm=24
    fc=24
    E=9400

if WidthProfile>0 and HeightProfile>0:
    W=[WidthProfile]
    H=[HeightProfile]
    Bc=0.1
    Input=0
elif str.lower(ToW)=='sawn':
    W=[50,38,50,50,75,50,50,63,50,50,100,50,75,75,75,125,75,100,150,100,175,200]
    H=[50,73,75,100,75,125,150,125,175,200,100,225,150,175,200,125,225,200,150,225,175,200]
    Bc=0.2
    Input=1
elif str.lower(ToW)=='planed':
    W=[45,45,45,70,45,45,45,45,95,45,70,70,70,120,70,95,145,95,170,195]
    H=[45,70,95,70,120,145,170,195,95,220,145,170,195,120,220,195,145,220,170,195]
    Bc=0.2
    Input=1
elif str.lower(ToW)=='glulam':
    w=[185,160,140,115,90,65,185,160,140,115,90,65,185,160,140,115,90,65,
    185,160,140,115,90,65,185,160,140,115,90,65,185,160,140,115,90,65,
    185,160,140,115,90,65,185,160,140,115,90,65,185,160,140,115,90,65,
    185,160,140,115,90,65,185,160,140,115,90,65,185,160,140,115,90,65,
    185,160,140,115,90,65,185,160,140,115,90,65,185,160,140,115,90,65,
    185,160,140,115,90,65,185,160,140,115,90,65,185,160,140,115,90,65,
    185,160,140,115,90,65,185,160,140,115,90,65,185,160,140,115,90,65,
    185,160,140,115,90,65,185,160,140,115,90,65,185,160,140,115,90,65,
    185,160,140,115,90,65,185,160,140,115,90,65,185,160,140,115,90,65,
    185,160,140,115,90,65,185,160,140,115,90,65,185,160,140,115,90,65,
    185,160,140,115,90,65,185,160,140,115,90,65,185,160,140,115,90,65,
    185,160,140,115,90,65,185,160,140,115,90,65,185,160,140,115,90,65,
    185,160,140,115,90,65,185,160,140,115,90,65,185,160,140,115,90,65,
    185,160,140,115,90,65,185,160,140,115,90,65,185,160,140,115,90,65,
    185,160,140,115,90,65]
    h=[100,100,100,100,100,100,133,133,133,133,133,133,167,167,167,167,167,167,
    200,200,200,200,200,200,233,233,233,233,233,233,267,267,267,267,267,267,
    300,300,300,300,300,300,333,333,333,333,333,333,367,367,367,367,367,367,
    400,400,400,400,400,400,433,433,433,433,433,433,467,467,467,467,467,467,
    500,500,500,500,500,500,533,533,533,533,533,533,567,567,567,567,567,567,
    600,600,600,600,600,600,633,633,633,633,633,633,667,667,667,667,667,667,
    700,700,700,700,700,700,733,733,733,733,733,733,767,767,767,767,767,767,
    800,800,800,800,800,800,833,833,833,833,833,833,867,867,867,867,867,867,
    900,900,900,900,900,900,933,933,933,933,933,933,967,967,967,967,967,967,
    1000,1000,1000,1000,1000,1000,1033,1033,1033,1033,1033,1033,1067,1067,1067,1067,1067,1067,
    1100,1100,1100,1100,1100,1100,1133,1133,1133,1133,1133,1133,1167,1167,1167,1167,1167,1167,
    1200,1200,1200,1200,1200,1200,1233,1233,1233,1233,1233,1233,1267,1267,1267,1267,1267,1267,
    1300,1300,1300,1300,1300,1300,1333,1333,1333,1333,1333,1333,1367,1367,1367,1367,1367,1367,
    1400,1400,1400,1400,1400,1400,1433,1433,1433,1433,1433,1433,1467,1467,1467,1467,1467,1467,
    1500,1500,1500,1500,1500,1500]
    A=[]
    for i in range(len(w)):
        A.append(w[i]*h[i]) 
    W = [x for _,x in sorted(zip(A,w))]
    H = [x for _,x in sorted(zip(A,h))]
    Bc=0.1
    Input=1

#Wood species
if WS==1:
    Bn=0.65
elif WS==2:
    Bn=0.65
elif WS==3:
    Bn=0.5
elif WS==4:
    Bn=1
else:
    Bn=0.65

#Sides exposed to fire
SEF = m.ceil(SEF)
if SEF>8:
    SEF=8
if SEF==1 or SEF==2 or SEF==3 or SEF==5 or SEF==6:
    a=1
else:
    a=2

"""-------------------------------------------------------------------------"""
# CALCULATION OF CROSS SECTION AFTER FIRE
# Charring layer
dchar = t*Bn

# Check for bmin
if dchar < 13:
    bmin = 8.15*dchar
else:
    bmin = a*dchar+80
W = [x for x in W if x > bmin]
H = [x for x in W if x > bmin]

# Cross section after fire
wr = [] 
hr = []
for i in range(len(W)):
    if SEF==1:
        wr.append(W[i])
        hr.append(H[i]-dchar)
    elif SEF==2:
        wr.append(W[i]-dchar)
        hr.append(H[i])
    elif SEF==3:
        wr.append(W[i]-dchar)
        hr.append(H[i]-dchar)
    elif SEF==4:
        wr.append(W[i]-2*dchar)
        hr.append(H[i]-dchar)
    elif SEF==5:
        wr.append(W[i]-dchar)
        hr.append(H[i]-2*dchar)
    elif SEF==6:
        wr.append(W[i])
        hr.append(H[i]-2*dchar)
    elif SEF==7:
        wr.append(W[i]-2*dchar)
        hr.append(H[i])
    elif SEF==8:
        wr.append(W[i]-2*dchar)
        hr.append(H[i]-2*dchar)

Wr = []
Hr = []
w = []
h = []
for i in range(len(wr)):
    if wr[i]>0 and hr[i]>0:
        Wr.append(wr[i])
        Hr.append(hr[i])
        w.append(W[i])
        h.append(H[i])

"""-------------------------------------------------------------------------"""
# Calculation of new moment of inertia
# Area of 1 corner
r = dchar
Acr = r**2*(1-m.pi/4)
# Moment of inertia corner
Ir = 0.00742*r**4
# Distance to center of gravity corner
sr = 0.223*r

Ar = []     #Area of cross section with rounded corners
S = []      #Static moment about original axis
Sh = []     #Static moment about original axis case 3
Sw = []     #Static moment about original axis case 3
drh = []     #Displacement of axis for corners
drw = []     #Displacement of axis for corners
Iysq = []   #Moment of inertia around z axis rectangle
Izsq = []   #Moment of inertia around y axis rectangle
Iycr = []   #Moment of inertia corner z axis corner
Izcr = []   #Moment of inertia corner y axis corner
Iytot = []  #Moment of inertia combined z axis total
Iztot = []  #Moment of inertia combined y axis total
Pr = []     #Perimeter


# Sides exposed to fire
# Width, Height, 2*Width, 2*Height same calculations
if SEF==1 or SEF==2 or SEF==6 or SEF== 7:  
    for i in range(len(Wr)):
        Iytot.append(1/12*Wr[i]*H[i]**3)
        Iztot.append(1/12*Hr[i]*Wr[i]**3)
        Pr.append(2*Wr[i]+2*Hr[i])
        Ar.append(Wr[i]*Hr[i])
# Width + Height
elif SEF==3:
    for i in range(len(Wr)):
        Ar.append(Wr[i]*Hr[i]-Acr)
        Sh.append(Acr*(Hr[i]/2-sr))
        drh.append(Sh[i]/Ar[i])
        Iysq.append(1/12*Wr[i]*(Hr[i]-2*drh[i])**3+1/12*Wr[i]*(2*drh[i])**3+Wr[i]*2*drh[i]*(Hr[i]/2)**2)
        Iycr.append(Ir+Acr*((Hr[i]/2)+drh[i]-sr)**2)
        Iytot.append(Iysq[i]-Iycr[i])
        Sw.append(Acr*(Wr[i]/2-sr))
        drw.append(Sw[i]/Ar[i])
        Izsq.append(1/12*Hr[i]*(Wr[i]-2*drh[i])**3+1/12*Hr[i]*(2*drh[i])**3+Hr[i]*2*drh[i]*(Wr[i]/2)**2)
        Izcr.append(Ir+Acr*((Wr[i]/2)+drw[i]-sr)**2)
        Iztot.append(Izsq[i]-Izcr[i])
        Pr.append(Hr[i]+(Hr[i]-r)+Wr[i]+(Wr[i]-r)+(m.pi*r*2)/4)

# Width + 2*Height 
elif SEF==4: 
    for i in range(len(W)):
        Ar.append(Wr[i]*Hr[i]-2*Acr)
        S.append(2*Acr*(Hr[i]/2-sr))
        drh.append(S[i]/Ar[i])
        Iysq.append(1/12*Wr[i]*(Hr[i]-2*drh[i])**3+1/12*Wr[i]*(2*drh[i])**3+Wr[i]*2*drh[i]*(Hr[i]/2)**2)
        Iycr.append(2*Ir+2*Acr*((Hr[i]/2)+drh[i]-0.223*r)**2)
        Iytot.append(Iysq[i]-Iycr[i])
        Izsq.append((1/12*Hr[i]*Wr[i]**3))
        Izcr.append(2*Ir+2*Acr*((Wr[i]/2)-0.223*r)**2)
        Iztot.append(Izsq[i]-Izcr[i])
        Pr.append((Wr[i])+2*(Hr[i]-r)+(Wr[i]-2*r)+(2*(m.pi*r*2)/4))

# 2*Width + Height
elif SEF==5:
    for i in range(len(Wr)):
        Ar.append(Hr[i]*Wr[i]-2*Acr)
        S.append(2*Acr*(Wr[i]/2-sr))
        drw.append(S[i]/Ar[i])
        Iysq.append(1/12*Hr[i]*(Wr[i]-2*drw[i])**3+1/12*Hr[i]*(2*drw[i])**3+Hr[i]*2*drw[i]*(Wr[i]/2)**2)
        Iycr.append(2*Ir+2*Acr*((Wr[i]/2)+drw[i]-0.223*r)**2)
        Iytot.append(Iysq-Iycr)
        Izsq.append((1/12*Wr[i]*Hr[i]**3))
        Izcr.append(2*Ir+2*Acr*((Hr[i]/2)-0.223*r)**2)
        Iztot.append(Izsq-Izcr)
        Pr.append((Hr[i]+2*(Wr[i]-r)+(Hr[i]-2*r)+(2*(m.pi*r*2)/4)))

# 2*Width + 2*Height
elif SEF==8: 
    for i in range(len(Wr)):
        Ar.append(Wr[i]*Hr[i]-4*Acr)
        Iytot.append(1/12*Wr[i]*Hr[i]**3-r**2*(4-m.pi)*(Hr[i]/2-sr)**2-4*Ir)
        Iztot.append(1/12*Hr[i]*Wr[i]**3-r**2*(4-m.pi)*(Wr[i]/2-sr)**2-4*Ir)
        Pr.append(2*(Hr[i]-2*r)+2*(Wr[i]-2*r)+m.pi*r*2)

else:
    print('You are doing something wrong')
Iy=Iytot
Iz=Iztot
"""-------------------------------------------------------------------------"""

# Verification of wooden column (Calculation of NRc,fire)
# Critical buckling length
ls = rs.CurveLength(CL)

# Checking for weakest axis
I = []
for i in range(len(Wr)):
    if Hr[i]>Wr[i]:
        I.append(Iz[i])
    else:
        I.append(Iy[i])

C =[]       # Reduction factor for compression strength
F = []      # Reduction factor for flexural strength
TS = []     # Reduction factor for tensile and shear strength

for i in range(len(Pr)):
    if t<20:
        C.append(1-1/125*Pr[i]/Ar[i]*t/20)
        F.append(1-1/200*Pr[i]/Ar[i]*t/20)
        TS.append(1-1/330*Pr[i]/Ar[i]*t/20)
    else:
        C.append(1-1/125*Pr[i]/Ar[i])
        F.append(1-1/200*Pr[i]/Ar[i])
        TS.append(1-1/330*Pr[i]/Ar[i])

Lambda = []
SigmaE = []  
kE = []  
Lambdarel = [] 
kfire = []
kc = []
Nrcfire = []

for i in range(len(Wr)):
    #Slenderness ratio
    Lambda.append(ls/m.sqrt(I[i]/Ar[i]))
    #Euler stress
    SigmaE.append(m.pi**2*(E/fc))
    #Euler factor
    kE.append(SigmaE[i]/fc)
    #Relative slenderness ratio
    Lambdarel.append(Lambda[i]/m.sqrt(SigmaE[i]))
    #kfire coefficient
    kfire.append(0.5*(1+Bc*(Lambdarel[i]-0.5)+Lambdarel[i]**2))
    #Critical buckling factor
    if Lambdarel[i]<0.5:
        kc.append(1.0)
    else:
        kc.append(1/(kfire[i]+m.sqrt(kfire[i]**2-Lambdarel[i]**2)))
    #Characteristic resistance of wood
    Nrcfire.append(Ar[i]*fc*kc[i])

if Input==0:
    if Nrcfire>F:
        Width = WidthProfile
        Height = HeightProfile
        NRcfire = Nrcfire
        Utilization = F/NRcfire[0]
    else:
        ErrorMessage='No profiles with selected citeria can support the load'

else:
# Selecting the smallest profile with capability to support the load
    Wi = []
    He = []
    NRc =[]
    for i in range(len(Wr)):
        if Nrcfire[i]>F:
            Wi.append(w[i])
            He.append(h[i])
            NRc.append(Nrcfire[i])
    if len(Wi)>0:
        Width = Wi[0]
        Height = He[0]
        NRcfire = NRc[0]
        Utilization = F/NRcfire
    else:
        ErrorMessage='No profiles with selected citeria can support the load'


"""-------------------------------------------------------------------------"""
# 3D model for "baking"
if NRcfire>F:
    End = rs.CurveEndPoint(CL)
    Start = rs.CurveStartPoint(CL)
    Vector = rs.VectorAdd(Start,End)
    Plane = rs.PlaneFromNormal(Start,Vector)
    CrossSection = rs.AddRectangle(Plane, Width, Height)
    #Translation vector center
    Vec1 =rs.VectorAdd([0,0,0],[-Width/2,-Height/2,0])
    Geo = rs.MoveObject(rs.ExtrudeCurve(CrossSection,CL),Vec1)
    rs.CapPlanarHoles(Geo)

