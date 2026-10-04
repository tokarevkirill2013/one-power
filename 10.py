n = int(input())
c = []
h = -n
for i in range(1,n+1):
    h += n
    for u in range(1,n+1):
        c.append(str(u+h))
    print("\t".join(c))
    c = []