N=8
board=[-1]*N
solutions=[]

def safe(row,col):
    for r in range(row):
        c=board[r]
        if c==col or abs(c-col)==abs(r-row):
            return False
    return True

def solve(row):
    if row==N:
        solutions.append(board.copy()); return
    for col in range(N):
        if safe(row,col):
            board[row]=col
            solve(row+1)
            board[row]=-1

solve(0)
print("One solution:",solutions[0])
print("Total solutions:",len(solutions))

Output:
One solution: [0, 4, 7, 5, 2, 6, 1, 3]
Total solutions: 92
