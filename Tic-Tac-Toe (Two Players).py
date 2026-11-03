board=[" "]*9
def show():
    for i in range(0,9,3):
        print("|".join(board[i:i+3]))
        if i<6: print("-----")
def winner():
    lines=[(0,1,2),(3,4,5),(6,7,8),(0,3,6),
           (1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for a,b,c in lines:
        if board[a]==board[b]==board[c]!=" ": return board[a]
    return None
player="X"
for move in [0,3,1,4,2]:
    board[move]=player
    if winner(): break
    player="O" if player=="X" else "X"
show()
print("Winner:",winner() if winner() else "Draw")


Output:
X|X|X
-----
O|O| 
-----
 | | 
Winner: X
