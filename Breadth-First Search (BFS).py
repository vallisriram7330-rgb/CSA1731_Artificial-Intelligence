from collections import deque
graph={"A":["B","C"],"B":["A","D","E"],"C":["A","F"],
       "D":["B"],"E":["B","F"],"F":["C","E"]}
def bfs(start):
    q=deque([start]); seen={start}; order=[]
    while q:
        u=q.popleft(); order.append(u)
        for v in graph[u]:
            if v not in seen:
                seen.add(v); q.append(v)
    return order
print("BFS Traversal:",bfs("A"))

Output:
BFS Traversal: ['A', 'B', 'C', 'D', 'E', 'F']
