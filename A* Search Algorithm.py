import heapq
graph={"A":[("B",1),("C",4)],"B":[("A",1),("C",2),("D",5)],
       "C":[("A",4),("B",2),("D",1)],"D":[("B",5),("C",1)]}
h={"A":3,"B":2,"C":1,"D":0}
def astar(start,goal):
    pq=[(h[start],0,start)]; cost={start:0}; parent={start:None}
    while pq:
        f,g,u=heapq.heappop(pq)
        if g!=cost[u]: continue
        if u==goal:
            path=[]
            while u is not None: path.append(u); u=parent[u]
            return path[::-1],g
        for v,w in graph[u]:
            ng=g+w
            if ng<cost.get(v,float("inf")):
                cost[v]=ng; parent[v]=u
                heapq.heappush(pq,(ng+h[v],ng,v))
    return None,float("inf")
path,total=astar("A","D")
print("Path:",path); print("Cost:",total)


Output:
Path: ['A', 'B', 'C', 'D']
Cost: 4
