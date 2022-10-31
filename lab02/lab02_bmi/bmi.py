'''
Take in a weight and height and calculate BMI 
'''

weight = eval(input("What is your weight in kg? "))
height = eval(input("What is your height in m? "))

bmi = round(weight / (height * height), 1)

print(f"Your BMI is {bmi}")
