from collections import deque
start=(3,3,0); goal=(0,0,1)
loads=[(2,0),(0,2),(1,1),(1,0),(0,1)]

def valid(m,c):
    rm,rc=3-m,3-c
    return 0<=m<=3 and 0<=c<=3 and not(m>0 and c>m) and not(rm>0 and rc>rm)

def successors(s):
    m,c,b=s
    for dm,dc in loads:
        nxt=(m-dm,c-dc,1) if b==0 else (m+dm,c+dc,0)
        if valid(nxt[0],nxt[1]): yield nxt

q=deque([(start,[start])]); seen={start}
while q:
    s,path=q.popleft()
    if s==goal:
        print("Solution path:")
        for x in path: print(x)
        print("Total crossings:",len(path)-1); break
    for t in successors(s):
        if t not in seen:
            seen.add(t); q.append((t,path+[t]))


Output:
Solution path:
(3, 3, 0)
(3, 1, 1)
(3, 2, 0)
(3, 0, 1)
(3, 1, 0)
(1, 1, 1)
(2, 2, 0)
(0, 2, 1)
(0, 3, 0)
(0, 1, 1)
(0, 2, 0)
(0, 0, 1)
Total crossings: 11      
