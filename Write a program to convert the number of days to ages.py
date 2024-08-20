"""Write a program to convert the number of days to ages"""
from datetime import date 

def calculateAge(birthDate): 
	today = date.today() 
	age = today.year - birthDate.year - ((today.month, today.day) < 
		(birthDate.month, birthDate.day)) 

	return age 
x=int(input("enter the year"))
y=int(input("enter the mounth"))
z=int(input("enter the day"))

print(calculateAge(date(x, y, z)), "years") 
