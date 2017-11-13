"""
Column - Standard fire with reduced cross section method

    Args:
        CL: Center Line for column
        F: Vertical load,N, for the beam to support (Calculated as a centrally placed load, also in the case when the column's center of gravity moves)
        Str: Strength class for the wood
        Sup: Support conditions for the column (1=Simply supported both ends, 2=One end fixed and one end not supported, 3=One end fixed and one end simply supported, 4=Both ends fixed
        ToW: Type of Wood; Sawn, Planed or Glulam (Glued laminated timber)
        WS: Wood Species (1=Conifer p>290 kg/m3, 2=Laminated wood p>290 kg/m3 , 3=Hardwood p>450 kg/m3 
        t: Time of exposure in minutes
        SEF: Sides Exposed to Fire(1=Width, 2=Height, 3=Width+Height, 4=Width+2*Height, 5=2*Width+Height, 6=2*Width, 7=2*Height, 8=All
    Returns:
        NRc,fire: Charateristic resistance of the column after fire
        Width: Width of the cross section before fire
        Height: Height of the cross section before fire
        Geo: 3D model of the cross section
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
elif str.upper(Str)=='GL32':
    fm=32
    fc=29
    E=11100
elif str.upper(Str)=='GL28':
    fm=38
    fc=26.5
    E=10200
elif str.upper(Str)=='GL24':
    fm=24
    fc=24
    E=9400

# Type of Wood
if str.lower(ToW)=='sawn':
    W=[50,38,50,50,75,50,50,63,50,50,100,50,75,75,75,125,75,100,150,100,175,200]
    H=[50,73,75,100,75,125,150,125,175,200,100,225,150,175,200,125,225,200,150,225,175,200]
elif str.lower(ToW)=='planed':
    W=[45,45,45,70,45,45,45,45,95,45,70,70,70,120,70,95,145,95,170,195]
    H=[45,70,95,70,120,145,170,195,95,220,145,170,195,120,220,195,145,220,170,195]
elif str.lower(ToW)=='glulam':
    W=[]
    H=[]

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
# New cross section
w=[] 
h=[]
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
        #print('z 7')
    elif SEF==8:
        w.append(W[i]-2*dchar)
        h.append(H[i]-2*dchar)
        #print('z 8')

print w, h

# Calculation of new moment of inertia

# Calculation of NRc,fire
#ls = rs.CurveLength(CL)*l0

# 3D model for "baking"