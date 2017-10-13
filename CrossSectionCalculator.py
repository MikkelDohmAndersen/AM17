""" Returns member boolean statement indicating moments of inertia larger than needed

    Args:
        I: Moment of inertia needed
        Iy: Moment of inertia y-axiz
        Iz: Moment of inertia z-axiz
    Returns:
        PatternY: Boolean statement for capacity > needed for y axis
        PatternZ: Boolean statement for capacity > needed for z axis
"""
Y=[]
Z=[]

# Muliplying the list values to match input for Iy
for i in Iy:
    Y.append(i*10**6)
for i in Iz:
    Z.append(i*10**6)
#print (y)

#Empty list for the new values
PatternY=[]
PatternZ=[]
#Creating boolean statement for capacity > needed
for i in Y:
    PatternY.append(i>I)
print(PatternY)
for i in Z:
    PatternZ.append(i>I)
print(PatternZ)





