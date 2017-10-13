""" Returns member index of all moments of inertia larger than needed

    Args:
        I: Moment of inertia needed
        Iy: Moment of inertia y-axiz
        Iz: Moment of inertia z-axiz
    Returns:
        i: member index

"""
Y=[]
Z=[]

#print (Iy)
#print (Y)

# Muliplying the list values to match input for Iy
for i in Iy:
    Y.append(i*10**6)
print (Y)

y=[]
for i in Y:
    y.append(i>I)
print(y)

Index = []





