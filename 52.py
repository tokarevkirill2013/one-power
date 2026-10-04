x = input().split()

def summm(n):
    su = 0
    for i in range(0,n):
        su += int(x[i])
    return su
n = len(x)
print(summm(n))