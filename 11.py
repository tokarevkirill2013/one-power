x = -1
sum =0
while x != 0:
    x = int(input())
    for i in range(2,x):
        if x % i ==0:
            sum += x
        else:
            sum += 0
print(sum)