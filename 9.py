n = int(input())
c = []
for i in range(1,n+1):
    for u in range(1,n+1):
        if i != u:
            c.append(1)
        else:
            c.append(0)
    print(c)
    c = []