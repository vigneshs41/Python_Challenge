"""Python Program to Print the Fibonacci sequence"""

c,n1=0,0
n2=1
x=int(input("enter the number"))
while(c<x):
    print(n1,end=' ')
    nth = n1 + n2
       # update values
    n1 = n2
    n2 = nth
    c += 1
