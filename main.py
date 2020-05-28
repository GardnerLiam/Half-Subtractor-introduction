import sys

def halfAdder(bit1,bit2):
    return bit1^bit2, bit1&bit2

def fullAdder(num1,num2):
    C = []
    carry = 0
    for i in range(len(num1)):
        res = halfAdder(num1[i],num2[i])
        res2 = halfAdder(res[0],carry)
        carry = res[1]|res2[1]
        C.append(res2[0])
    return C

def twosComplement(num):
    flipped = [1 if i == 0 else 0 for i in num]
    C = []
    carry = 0
    for i in range(len(num)):
        res = halfAdder(flipped[i],1 if i == 0 else 0)
        res2 = halfAdder(res[0],carry)
        C.append(res2[0])
        carry = res[1]|res2[1]
    return C

def asArray(binstring):
    return [int(i) for i in binstring][::-1]

def fromArray(binarray):
    return "".join([str(i) for i in binarray][::-1])

def andAll(array):
    if len(array) == 1:
        return array[0]
    array[-2] = 1 if (array[-1]==1 and array[-2]==1) else 0
    return andAll(array[:-1])

def orAll(array):
    if len(array) == 1:
        return array[0]
    array[-2] = 1 if (array[-1] == 1 or array[-2] == 1) else 0
    return orAll(array[:-1])

def n(x):
    return 1 if x == 0 else 0

def halfSubtractor(bit1, bit2):
    diff = bit1^bit2
    borrow = n(bit1)&bit2
    return diff, borrow

def comparator(num1,num2):
    c = []
    x = []
    carry = 1
    for i in range(len(num1)):
        c.append(num1[i]&n(num2[i])&carry)
        x.append(n(num1[i]^num2[i]))
        carry = andAll(x[:])
    return orAll(c)

def fullSubtractor(num1, num2):
    borrow = 0
    newNum = []
    for i in range(len(num1)):
        res = halfSubtractor(num1[i],num2[i])
        #print("Digits: {},{} --> diff:{} --> borrow: {}".format(num1[i],num2[i],res[0],res[1]))
        newNum.append(res[0]-borrow)
        borrow = res[1]
    return newNum

def readTwosComplement(num):
    array = [2**i for i in range(len(num))[::-1]]
    array[0] *= -1
    return sum([int(num[i])*array[i] for i in range(len(num))])

#main loop starts here

if len(sys.argv) < 3:
    print("Error: less than two numbers detected")
    sys.exit(0)

n1 = int(sys.argv[1])
n2 = int(sys.argv[2])

b1 = bin(n1)[2:]
b2 = bin(n2)[2:]

while len(b2) < len(b1):
    b2 = "0" + b2

while len(b1) < len(b2):
    b1 = "0" + b1
    if len(b1) == len(b2):
        break

print(len(b1),len(b2),b1,b2)
print("Subtracting numbers {} and {}".format(n1,n2))
print("Binary values: {} and {}".format(b1,b2))

array1 = asArray(b1)
array2 = asArray(b2)

print("Numeric processing done as: {}, {}".format(array1,array2))
minuendGreater = comparator(array1[::-1],array2[::-1])
print("comparator result: {}".format(minuendGreater))

print("----------------------")

if minuendGreater == 1:
    print("Subtracting values: {}-{}".format(array1,array2))
    value = fullSubtractor(array1,array2)
    print(value)
    value = fromArray(value)
    print("{} --> {}".format(value,int(value,2)))
else:
    print("Subtracting values: {}-{}".format(array2,array1))
    value = fullSubtractor(array2,array1)
    print("Direct Value: {}".format(value))
    value = fromArray(value)
    print("applying two's complement to {}".format(value))
    arrayValue = asArray(value)
    if value[0] == "1":
        arrayValue.append(0)
    tc = twosComplement(arrayValue)
    stringTc = fromArray(tc)
    print("Negative Number: {} --> {}".format(stringTc,readTwosComplement(stringTc)))

