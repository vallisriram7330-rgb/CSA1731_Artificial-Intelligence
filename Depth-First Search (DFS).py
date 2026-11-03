graph={"A":["B","C"],"B":["A","D","E"],"C":["A","F"],
       "D":["B"],"E":["B","F"],"F":["C","E"]}
def dfs(u,seen,order):
    seen.add(u); order.append(u)
    for v in graph[u]:
        if v not in seen: dfs(v,seen,order)
visited=set(); order=[]
dfs("A",visited,order)
print("DFS Traversal:",order)

Output:
DFS Traversal: ['A', 'B', 'D', 'E', 'F', 'C']
