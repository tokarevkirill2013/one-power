f = open("inn.txt","r")
text = f.read()
print(text)
f.close()
with open("inn.txt","a") as f:
    text = f.read()