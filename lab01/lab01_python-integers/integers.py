'''
TODO Complete this file by following the instructions in the lab exercise.
'''

integers = [1, 2, 3, 4, 5]
integers.append(6)

result = 0
for i in range(0, len(integers)):
    result += integers[i]

print(result)

print(sum(integers))
    
