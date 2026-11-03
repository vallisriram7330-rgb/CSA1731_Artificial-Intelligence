from collections import deque
start=(0,0); goal=2

def next_states(a,b):
    moves=[
        (4,b),(a,3),(0,b),(a,0),
        (a-min(a,3-b),b+min(a,3-b)),
        (a+min(b,4-a),b-min(b,4-a))
    ]
    return set(moves)

q=deque([(start,[start])]); seen={start}
while q:
    state,path=q.popleft()
    if goal in state:
        print("Solution states:",path)
        print("Steps:",len(path)-1); break
    for nxt in next_states(*state):
        if nxt not in seen:
            seen.add(nxt); q.append((nxt,path+[nxt]))

Output:
Solution states: [(0, 0), (4, 0), (1, 3), (1, 0), (0, 1), (4, 1), (2, 3)]
Steps: 6
