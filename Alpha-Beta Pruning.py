def alpha_beta(node,maximizing,alpha,beta):
    if isinstance(node,int): return node
    if maximizing:
        value=float("-inf")
        for child in node:
            value=max(value,alpha_beta(child,False,alpha,beta))
            alpha=max(alpha,value)
            if alpha>=beta: break
        return value
    value=float("inf")
    for child in node:
        value=min(value,alpha_beta(child,True,alpha,beta))
        beta=min(beta,value)
        if alpha>=beta: break
    return value
tree=[[3,5],[2,9]]
print("Best value using Alpha-Beta:",
      alpha_beta(tree,True,float("-inf"),float("inf")))



Output:
Best value using Alpha-Beta: 3
