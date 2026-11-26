import numpy as np
from sklearn.linear_model import LinearRegression

# Training data (X: Independent variable, y: Continuous target)
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 6, 8, 10])

model = LinearRegression()
model.fit(X, y)

# Predict for a new input
prediction = model.predict(np.array([[6]]))
print(f"Predicted value for X=6: {prediction[0]:.2f}")
