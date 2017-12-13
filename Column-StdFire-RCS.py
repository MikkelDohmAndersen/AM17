"""
Column - Standard fire with reduced cross section method

    Args:
        CL: Center Line for column
        F: Vertical load,N, for the column to support (Calculated as a centrally placed load, also in the case when the column's center of gravity moves)
        Str: Strength class for the wood (C30, C24, C18, C14, GL32h, GL28h or GL24h)[Default: 24C]
        Sup: Support conditions for the column (1=Simply supported both ends, 2=One end fixed and one end not supported, 3=One end fixed and one end simply supported, 4=Both ends fixed [Default: Simply supported]
        ToW: Type of Wood; Sawn, Planed or Glulam (Glued laminated timber) standard profiles [Default: sawn]
        WidthProfile: Width of profile [mm] to calculate NRc,fire for. If no value is inserted, the NRc,fire is calculated based on ToW.
        HeightProfile: Height of profile [mm] to calculate NRc,fire for. If no value is inserted, the NRc,fire is calculated based on ToW.
        WS: Wood Species (1=Conifer p>290 kg/m3, 2=Laminated wood p>290 kg/m3 , 3=Hardwood p>450 kg/m3 [Default: Conifer]
        t: Time of exposure in minutes [Default 60]
        SEF: Sides Exposed to Fire(1=Width, 2=Height, 3=Width+Height, 4=Width+2*Height, 5=2*Width+Height, 6=2*Width, 7=2*Height, 8=All [Default: All]
    Returns:
        NRc,fire: Charateristic resistance of the column after fire [kN]
        Width: Width of the cross section before fire [mm]
        Height: Height of the cross section before fire [mm]
        Geo: 3D model of the cross section
        Utilization: Utilization rate [%]
        ErrorMessage: Check this output for error messages

"""

import rhinoscriptsyntax as rs
import math as m

"""-------------------------------------------------------------------------"""
# USER INPUTS
# Defaults
StrDef = 'c24'
SupDef = 1
ToWDef = 'sawn'
WSDef = 1
tDef = 60
SEFDef = 8

if not Str:
    Str=StrDef
if not Sup:
    Sup=SupDef
if not ToW:
    ToW=ToWDef
if not WS:
    WS=WSDef
if not t:
    t=tDef
if not SEF:
    SEF=SEFDef

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
    Bn=0.8
elif WS==2:
    Bn=0.7
elif WS==3:
    Bn=0.55
else:
    Bn=0.8

#Sides exposed to fire
SEF = m.ceil(SEF)
if SEF>8:
    SEF=8

"""-------------------------------------------------------------------------"""
# CALCULATION OF CROSS SECTION AFTER FIRE
#Pyrolysis Zone
if t<20: 
    dpy = 7/20*t 
else:
    dpy = 7
# Charring layer
dchar = Bn*t+dpy

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
Ar = []

for i in range(len(wr)):
    if wr[i]>0 and hr[i]>0:
        Wr.append(wr[i])
        Hr.append(hr[i])
        w.append(W[i])
        h.append(H[i])
        Ar.append(wr[i]*hr[i])

"""-------------------------------------------------------------------------"""
# Calculation of new moment of inertia
Iy = []
Iz = []
for i in range(len(Wr)):
    Iy.append(1/12*Wr[i]*Hr[i]**3)
    Iz.append(1/12*Hr[i]*Wr[i]**3)
"""-------------------------------------------------------------------------"""

# Verification of wooden column (Calculation of NRc,fire)
# Critical buckling length
L = []
ls = []
for i in range(len(CL)):
    L.append(rs.CurveLength(CL[i]))
    ls.append(L[i]*l0)

# Checking for weakest axis
I = []
for i in range(len(Wr)):
    if Hr[i]>wr[i]:
        I.append(Iz[i])
    else:
        I.append(Iy[i])

Lambda = []
SigmaE = []  
Lambdarel = [] 
kfire = []
kc = []
Width = []
Height = []
NRcfire = []
Utilization = []
for i in range(len(CL)):
    nrcfire = []
    for j in range(len(Wr)):
        #Slenderness ratio
        Lambda.append(ls[i]/m.sqrt(I[j]/Ar[j]))
        #Euler stress
        SigmaE.append(m.pi**2*(E/fc))
        #Relative slenderness ratio
        Lambdarel.append(Lambda[j]/m.sqrt(SigmaE[j]))
        #kfire coefficient
        kfire.append(0.5*(1+Bc*(Lambdarel[j]-0.5)+Lambdarel[j]**2))
        #Critical buckling factor
        if Lambdarel[j]<0.5:
            kc.append(1.0)
        else:
            kc.append(1/(kfire[j]+m.sqrt(kfire[j]**2-Lambdarel[j]**2)))
        #Characteristic resistance of wood
        nrcfire.append(Ar[j]*fc*kc[j])
    if Input==0:
        if nrcfire>F:
            Width.append(WidthProfile)
            Height.append(HeightProfile)
            NRcfire.append(nrcfire[0])
            Utilization.append(F[i]/NRcfire[0])
        else:
            ErrorMessage='No profiles with selected citeria can support the load'
    else:
    # Selecting the smallest profile with capability to support the load
        Wi = []
        He = []
        NRc = []
        for j in range(len(Wr)):
            if nrcfire[j]>F[i]:
                Wi.append(w[j])
                He.append(h[j])
                NRc.append(nrcfire[j])
        if len(Wi)>0:
            Width.append(Wi[0])
            Height.append(He[0])
            NRcfire.append(NRc[0])
            Utilization.append(F[i]/NRcfire[i])
        else:
            ErrorMessage='No profiles with selected citeria can support the load'

"""-------------------------------------------------------------------------"""
# 3D model for "baking"
End = []
Start = []
Vector = []
Plane = []
CrossSection = []
Geo1 = []
Geo = []
Line = []
Cl = CL[0]

for i in range(len(NRcfire)):
    if NRcfire[i]>F[i]:
        End = rs.CurveEndPoint(Cl)
        Start = rs.CurveStartPoint(Cl)
        Vector = rs.VectorAdd(Start,End)
        Plane = rs.PlaneFromNormal(Start,Vector)
        for i in range(len(CL)):
            CrossSection.append(rs.AddRectangle(Plane, Height[i], Width[i]))
            Geo1.append(rs.MoveObject(rs.ExtrudeCurve(CrossSection[i],CL[i]),rs.CurveStartPoint(CL[i])))
            Geo.append(rs.MoveObject(Geo1[i],[(-Width[i]/2)/10,0,(-Height[i]/2)/10]))
            rs.CapPlanarHoles(Geo[i])