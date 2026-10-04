n = int(input())
def maath(a):
    summ = 1
    for i in range(1,a + 1):
        summ = summ * i
    return summ
print(maath(n))