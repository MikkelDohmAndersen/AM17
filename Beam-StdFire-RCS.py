"""
Calculation and selection of the smallest standard or user defined cross section for a wooden beam that can support the given load during a standard fire using the reduced cross section method

Created by Mikkel Dohm Andersen, DTU.BYG

    Args:
        CL: Center Line for beam
        q: Line load for the beam to support [kN/m]
        Str: Strength class for the wood 1=C30, 2=C24, 3=C18, 4=C14, 5=GL32h, 6=GL28h or 7=GL24h)[Default: 24C]
        Sup: Support conditions for the column (1=Simply supported both ends, 2=One end fixed and one end not supported, 3=One end fixed and one end simply supported, 4=Both ends fixed [Default: Simply supported]
        ToW: Type of Wood; 1=Sawn, 2=Planed or 3=Glulam (Glued laminated timber) standard profiles [Default: sawn]
        WidthProfile: Width of profile [mm] to calculate qmax for. If no value is inserted, the qmax is calculated based on ToW.
        HeightProfile: Height of profile [mm] to calculate qmax for. If no value is inserted, the qmax is calculated based on ToW.
        WS: Wood Species (1=Conifer p>290 kg/m3, 2=Laminated wood p>290 kg/m3 , 3=Hardwood p>450 kg/m3 [Default: Conifer]
        t: Time of exposure [minutes] [Default 60]
        SEF: Sides Exposed to Fire(1=Width, 2=Height, 3=Width+Height, 4=Width+2*Height, 5=2*Width+Height, 6=2*Width, 7=2*Height, 8=All [Default: Width+2*Height]
    Returns:
        qmax: Maximum line load the beam can support [kN/m]
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
StrDef = 1
SupDef = 1
ToWDef = 1
WSDef = 1
tDef = 60
SEFDef = 4

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

# Strength class
if Str==1:
    fm=30
    fc=23
    E=8000
elif Str==2:
    fm=24
    fc=21
    E=7400
elif Str==3:
    fm=18
    fc=18
    E=6000
elif Str==4:
    fm=14
    fc=16
    E=4700
elif Str==5:
    fm=32
    fc=29
    E=11100
elif Str==6:
    fm=28
    fc=26.5
    E=10200
elif Str==7:
    fm=24
    fc=24
    E=9400

if WidthProfile>0 and HeightProfile>0:
    W=[WidthProfile]
    H=[HeightProfile]
    Input=0
elif ToW==1:
    W=[50,38,50,50,75,50,50,63,50,50,100,50,75,75,75,125,75,100,150,100,175,200]
    H=[50,73,75,100,75,125,150,125,175,200,100,225,150,175,200,125,225,200,150,225,175,200]
    Input=1
elif ToW==2:
    W=[45,45,45,70,45,45,45,45,95,45,70,70,70,120,70,95,145,95,170,195]
    H=[45,70,95,70,120,145,170,195,95,220,145,170,195,120,220,195,145,220,170,195]
    Input=1
elif ToW==3:
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
w = [] 
h = []
for i in range(len(W)):
    if SEF==1:
        w.append(W[i])
        h.append(H[i]-dchar)
    elif SEF==2:
        w.append(W[i]-dchar)
        h.append(H[i])
    elif SEF==3:
        w.append(W[i]-dchar)
        h.append(H[i]-dchar)
    elif SEF==4:
        w.append(W[i]-2*dchar)
        h.append(H[i]-dchar)
    elif SEF==5:
        w.append(W[i]-dchar)
        h.append(H[i]-2*dchar)
    elif SEF==6:
        w.append(W[i])
        h.append(H[i]-2*dchar)
    elif SEF==7:
        w.append(W[i]-2*dchar)
        h.append(H[i])
    elif SEF==8:
        w.append(W[i]-2*dchar)
        h.append(H[i]-2*dchar)

wr = [] 
hr = []
Wr = []
Hr = []
Ar = []
for i in range(len(w)):
    if w[i]>0 and h[i]>0:
        wr.append(w[i])
        hr.append(h[i])
        Wr.append(W[i])
        Hr.append(H[i])
        # Area of cross section
        Ar.append(w[i]*h[i])


"""-------------------------------------------------------------------------"""
# Calculation of new moment of inertia
Iy = []
Iz = []
for i in range(len(wr)):
    Iy.append(1/12*wr[i]*hr[i]**3)
    Iz.append(1/12*hr[i]*wr[i]**3)

"""-------------------------------------------------------------------------"""
# Support conditions
L = []
Mmax = []
for i in range(len(CL)):
    L.append(rs.CurveLength(CL[i]))
    if Sup==1 or Sup==4:
        Mmax.append(1/8*q[i]*L[i]**2)
    elif Sup==2:
        Mmax.append(1/2*q[i]*L[i]**2)
    elif Sup==3:
        Mmax.append(9/128*q[i]*L[i]**2)


# Verification of wooden beam 
Width = []
Height = []
Utilization = []
Sigmafire = []
qmax = []
for i in range(len(Mmax)):
    sigmafire = []
    Qmax = []
    for j in range(len(Wr)):
        sigmafire.append(Mmax[i]/Iy[j]*Hr[j]/2)
        if Sup==1 or Sup==4:
            Qmax.append((fm*2*Iy[j])/(1/8*L[i]**2*Hr[j]))
        elif Sup==2:
            Qmax.append((fm*2*Iy[j])/(1/2*L[i]**2*Hr[j]))
        elif Sup==3:
            Qmax.append((fm*2*Iy[j])/(9/128*L[i]**2*Hr[j]))
    if Input==0:
        if 0<sigmafire[j]<fm:
           Width.append(WidthProfile)
           Height.append(HeightProfile)
           Sigmafire.append(sigmafire[0])
           qmax.append(Qmax[0])
           Utilization.append(Sigmafire[i]/fm*100)
        else:
            ErrorMessage='No profiles with selected citeria can support the load'
    else:
        # Selecting the smallest profile with capability to support the load
        Wi = []
        He = []
        fmfire =[]
        QMax =[]
        for j in range(len(wr)):
            if 0<sigmafire[j]<fm:
                Wi.append(Wr[j])
                He.append(Hr[j])
                fmfire.append(sigmafire[j])
                QMax.append(Qmax[j])
        if len(Wi)>0:
            Width.append(Wi[0])
            Height.append(He[0])
            Sigmafire.append(fmfire[0])
            qmax.append(QMax[0])
            Utilization.append(Sigmafire[i]/fm*100)
        else:
            ErrorMessage='No profiles with selected citeria can support the load'

"""-------------------------------------------------------------------------"""
# 3D model for "baking"
End = []
Start = []
Vector = []
Plane = []
CrossSection = []
Geo = []
Line = []
Cl = CL[0]

for i in range(len(Sigmafire)):
    if Sigmafire[i]<fm:
        End = rs.CurveEndPoint(Cl)
        Start = rs.CurveStartPoint(Cl)
        Vector = rs.VectorCreate(Start,End)
        Plane = rs.PlaneFromNormal(Start,Vector)
        for i in range(len(CL)):
            CrossSection.append(rs.AddRectangle(Plane, Height[i], Width[i]))
            Geo.append(rs.MoveObject(rs.ExtrudeCurve(CrossSection[i],CL[i]),(rs.CurveStartPoint(CL[i])-rs.CurveStartPoint(CL[0]))))
            rs.CapPlanarHoles(Geo[i])




