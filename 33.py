n = int(input())
d = {}
summ = 0
for i in range(0,n):
    x = input().split()
    d[x[0]] = x[1]
for el in d.values():
    summ += int(el)
print(summ)