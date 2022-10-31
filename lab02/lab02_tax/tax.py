'''
Calculate the estimated tax on input income 
'''

income = eval(input("Enter your income: "))

number = 0

if income <= 18200:
    pass
elif income <= 37000:
    number = (income - 18200) * 0.19
elif income <= 87000:
    number = ((income - 37000) * 0.325) + 3572
elif income <= 180000:
    number = ((income - 87000) * 0.37) + 19822
else:
    number = ((income - 180000) * 0.45) + 54232
    
tax = '{:,.2f}'.format(number)
print(f"The estimated tax on your income is ${tax}")
