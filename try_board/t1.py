def NN(number, digitCount):
    # Normalizes a single digit number to have digitCount 0s in front of it
    format = "%0" + str(digitCount) + "d"
    print format
    return format % number

a = [1,2,3,4]

for i in range(4):
    print NN(a[i],2)