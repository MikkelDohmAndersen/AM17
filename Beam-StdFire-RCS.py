"""
Column - Standard fire with reduced cross section method

    Args:
        CL: Center Line for column [mm]
        F: Uniformly distributed load,[kN/m], for the beam to support
        Str: Strength class for the wood (C30, C24, C18, C14, GL32h, GL28h or GL24h)
        Sup: Support conditions for the column (1=Simply supported both ends, 2=One end fixed and one end not supported, 3=One end fixed and one end simply supported, 4=Both ends fixed
        ToW: Type of Wood; Sawn, Planed or Glulam (Glued laminated timber) standard profiles.
        WidthProfile: Width of profile [mm] to calculate NRc,fire for. If no value is inserted, the NRc,fire is calculated on ToW.
        HeightProfile: Height of profile [mm] to calculate NRc,fire for. If no value is inserted, the NRc,fire is calculated on ToW.
        WS: Wood Species (1=Conifer p>290 kg/m3, 2=Laminated wood p>290 kg/m3 , 3=Hardwood p>450 kg/m3
        t: Time of exposure in minutes
        SEF: Sides Exposed to Fire(1=Width, 2=Height, 3=Width+Height, 4=Width+2*Height, 5=2*Width+Height, 6=2*Width, 7=2*Height, 8=All
    Returns:
        Mmaxfire: Moment capacity [kNm)
        Width: Width [mm] of the cross section before fire
        Height: Height [mm] of the cross section before fire
        Geo: 3D model of the cross section
        Utilization: Utilization rate [%]
        ErrorMessage: Check this output for error messages
"""

import rhinoscriptsyntax as rs
import math as m

"""-------------------------------------------------------------------------"""
# USER INPUTS
# Support conditions
L=rs.CurveLength(CL)
if Sup==1:
    Mmax=1/8*F*L**2
elif Sup==2:
    Mmax=1/2*F*L**2
elif Sup==3:
    Mmax=9/128*F*L**2
elif Sup==4:
    Mmax=1/8*F*L**2


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
    Input=0
elif str.lower(ToW)=='sawn':
    W=[50,38,50,50,75,50,50,63,50,50,100,50,75,75,75,125,75,100,150,100,175,200]
    H=[50,73,75,100,75,125,150,125,175,200,100,225,150,175,200,125,225,200,150,225,175,200]
    Input=1
elif str.lower(ToW)=='planed':
    W=[45,45,45,70,45,45,45,45,95,45,70,70,70,120,70,95,145,95,170,195]
    H=[45,70,95,70,120,145,170,195,95,220,145,170,195,120,220,195,145,220,170,195]
    Input=1
elif str.lower(ToW)=='glulam':
    W=[]
    H=[]
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
# Calculation of new resistance moment 
Wy = []
for i in range(len(wr)):
    Wy.append(1/6*wr[i]*hr[i]**2)

"""-------------------------------------------------------------------------"""

# Verification of wooden beam 
mmaxfire = []
for i in range(len(wr)):
    mmaxfire.append(fm*Wy[i])

if Input==0:
    if mmaxfire[i]>Mmax:
       Width = WidthProfile
       Height = HeightProfile
       Mmaxfire = mmaxfire[0]/1000
       Utilization = Mmax/Mmaxfire*10**(-4)
    else:
        ErrorMessage='No profiles with selected citeria can support the load'
else:
    # Selecting the smallest profile with capability to support the load
    Wi = []
    He = []
    mmax =[]
    for i in range(len(wr)):
        if mmaxfire[i]>Mmax:
            Wi.append(Wr[i])
            He.append(Hr[i])
            mmax.append(mmaxfire[i])
    if len(Wi)>0:
        Width = Wi[0]
        Height = He[0]
        Mmaxfire = mmax[0]/(10**6)
        Utilization = Mmax/Mmaxfire*10**(-4)
    else:
        ErrorMessage='No profiles with selected citeria can support the load'



"""-------------------------------------------------------------------------"""
# 3D model for "baking"
if mmaxfire[i]>Mmax:
    End = rs.CurveEndPoint(CL)
    Start = rs.CurveStartPoint(CL)
    Vector = rs.VectorAdd(Start,End)
    Plane = rs.PlaneFromNormal(Start,Vector)
    CrossSection = rs.AddRectangle(Plane, Height, Width)
    #Translation vector center
    Vec1 =rs.VectorAdd([0,0,0],[-Width/2,-Height/2,0])
    Geo = rs.MoveObject(rs.ExtrudeCurve(CrossSection,CL),Vec1)
    rs.CapPlanarHoles(Geo)


