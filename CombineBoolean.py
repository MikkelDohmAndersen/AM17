""" Combines two equal length lists of boolean statements
    to one, either dominated by true or false values
"""
T = []
F = []
for i in x:
    if i == 'True':
        T.append('True')
        F.append('True')
    else:
        T.append('False')
        F.append('False')

for i in range(len(y)):
    if y[i] == 'True':
        T[i]= 'True'

for i in range(len(y)):
    if y[i] == 'False':
        F[i]= 'False'

True=T
False=F