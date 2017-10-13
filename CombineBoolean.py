""" Combines two equal length lists of boolean statements
    to one, either dominated by true or false values
"""

a = []

#print(x)
for i in x:
    if i == 'True':
        a.append('True')
    else:
        for i in y:
            if i == 'True':
                a.append('True')
            else:
                a.append('False')


print(a)