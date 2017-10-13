""" Combines two equal length lists of boolean statements
    to one, either dominated by true or false values
"""

a = []

#print(x)
for i in x:
    if i == 'True':
        a.append('True')
    else:
        a.append('False')

for i in range(len(y)):
    if y[i] == 'True':
        a[i]= 'True'


print(a)
