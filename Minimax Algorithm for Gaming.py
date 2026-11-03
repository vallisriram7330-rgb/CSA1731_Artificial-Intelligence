def minimax(node,maximizing):
    if isinstance(node,int): return node
    if maximizing:
        return max(minimax(child,False) for child in node)
    return min(minimax(child,True) for child in node)
tree=[[3,5],[2,9]]
print("Best value:",minimax(tree,True))  


Output:
Best value: 3
