regions=["A","B","C","D"]
colors=["Red","Green","Blue"]
adj={"A":["B","C"],"B":["A","C","D"],
     "C":["A","B","D"],"D":["B","C"]}
assigned={}
def safe(region,color):
    return all(assigned.get(n)!=color for n in adj[region])
def solve(i=0):
    if i==len(regions): return True
    r=regions[i]
    for color in colors:
        if safe(r,color):
            assigned[r]=color
            if solve(i+1): return True
            del assigned[r]
    return False
if solve():
    print("Map Coloring Solution:")
    for r in regions: print(r,":",assigned[r])
else: print("No solution")


Output:
Map Coloring Solution:
A : Red
B : Green
C : Blue
D : Red
