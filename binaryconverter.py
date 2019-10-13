num = float(input("Enter the number to convert into binary :"))
if num < 0:
	isNeg = True
	num = abs(num)
else:
	isNeg = False
x = int(num)
if x < num:
	y = float(num - x)
p = 0
while ((2**p)*y)%1 != 0:
	reminder = str((2**p)*y - int((2**p)*y))
	p += 1
print (p)
z = (y*(2**p))
print (z)
result1 = ''
if z == 0:
	result1 = '0'
while z > 0 :
	result1 = str(int(z%2)) + result1
	z = int(z/2)
print(len(result1))
for i in range (p - len(result1)):
	result1 = '0' + result1
print ('result1 is: ' +result1)

result =''
if num == 0:
	result = '0'
while num > 0:
	result = str(int(num%2)) + result
	num = int(num/2)
	
if isNeg:
	result ='-' + result
print ('output is ' +result + '.' +result1)
