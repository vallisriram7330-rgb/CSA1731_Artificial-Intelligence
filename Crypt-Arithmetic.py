from itertools import permutations
letters="SENDMORY"
for p in permutations("0123456789",8):
    d=dict(zip(letters,p))
    if d["S"]=="0" or d["M"]=="0": continue
    send=int("".join(d[x] for x in "SEND"))
    more=int("".join(d[x] for x in "MORE"))
    money=int("".join(d[x] for x in "MONEY"))
    if send+more==money:
        print("SEND =",send)
        print("MORE =",more)
        print("MONEY =",money)
        print("Verified:",send+more==money)
        break

Output:
SEND = 9567
MORE = 1085
MONEY = 10652
Verified: True
