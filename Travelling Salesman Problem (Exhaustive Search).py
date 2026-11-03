from itertools import permutations
d=[[0,10,15,20],[10,0,35,25],[15,35,0,30],[20,25,30,0]]
best=float("inf"); best_route=None
for p in permutations(range(1,len(d))):
    route=(0,)+p+(0,)
    cost=sum(d[route[i]][route[i+1]] for i in range(len(route)-1))
    if cost<best: best=cost; best_route=route
print("Best route:",best_route)
print("Minimum cost:",best)

Output:
Best route: (0, 1, 3, 2, 0)
Minimum cost: 80
