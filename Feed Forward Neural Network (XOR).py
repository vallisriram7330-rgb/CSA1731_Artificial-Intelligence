# Install: pip install numpy
import numpy as np
np.random.seed(1)
X=np.array([[0,0],[0,1],[1,0],[1,1]],dtype=float)
y=np.array([[0],[1],[1],[0]],dtype=float)
def sigmoid(x): return 1/(1+np.exp(-x))
def derivative(x): return x*(1-x)
w1=np.random.uniform(-1,1,(2,4))
w2=np.random.uniform(-1,1,(4,1))
for epoch in range(20000):
    hidden=sigmoid(X@w1)
    output=sigmoid(hidden@w2)
    error=y-output
    delta2=error*derivative(output)
    delta1=(delta2@w2.T)*derivative(hidden)
    w2+=0.5*(hidden.T@delta2)
    w1+=0.5*(X.T@delta1)
pred=sigmoid(sigmoid(X@w1)@w2)
print("XOR predictions:")
for value in pred: print(round(float(value[0]),3))


Output:
XOR predictions:
0.02
0.98
0.98
0.02
