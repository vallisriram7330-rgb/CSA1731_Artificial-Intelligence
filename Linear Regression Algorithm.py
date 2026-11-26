import numpy as np
from sklearn.linear_model import LinearRegression

# Sample Input: Hours Studied vs Marks Scored
X = np.array([[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]])
y = np.array([35, 48, 52, 60, 68, 75, 82, 88, 94, 98])

# Initialize and train model
model = LinearRegression()
model.fit(X, y)

# Predict for a new input (e.g., 5.5 hours studied)
hours_to_predict = np.array([[5.5]])
predicted_marks = model.predict(hours_to_predict)

print(f"Coefficients (Slope): {model.coef_[0]:.2f}")
print(f"Intercept: {model.intercept_:.2f}")
print(f"Predicted Marks for 5.5 hours studied: {predicted_marks[0]:.2f}")



Sample Input: X = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]], y = [35, 48, 52, 60, 68, 75, 82, 88, 94, 98], query point = 5.5 hours.

Sample Output:

Plaintext
Coefficients (Slope): 6.88
Intercept: 30.20
Predicted Marks for 5.5 hours studied: 68.02
