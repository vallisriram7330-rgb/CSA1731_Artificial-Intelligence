from collections import deque
start=(1,2,3,4,0,6,7,5,8)
goal=(1,2,3,4,5,6,7,8,0)

def neighbours(s):
    z=s.index(0); r,c=divmod(z,3)
    for name,nz in [("Up",z-3),("Down",z+3),("Left",z-1),("Right",z+1)]:
        if name=="Up" and r==0 or name=="Down" and r==2: continue
        if name=="Left" and c==0 or name=="Right" and c==2: continue
        t=list(s); t[z],t[nz]=t[nz],t[z]
        yield name,tuple(t)

q=deque([(start,[])])
seen={start}
while q:
    s,path=q.popleft()
    if s==goal:
        print("Moves:",path); print("Number of moves:",len(path)); break
    for a,t in neighbours(s):
        if t not in seen:
            seen.add(t); q.append((t,path+[a]))


Output:
Moves: ['Down', 'Right']
Number of moves: 2
