from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load dataset
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.3, random_state=42)

# Initialize KNN classifier with k=3
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)

# Predictions & Evaluation
y_pred = knn.predict(X_test)
print(f"Accuracy Score: {accuracy_score(y_test, y_pred) * 100:.2f}%")
print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=iris.target_names))


Sample Input: Iris dataset features (sepal length, sepal width, petal length, petal width) split 70% train / 30% test.

Sample Output:

Plaintext
Accuracy Score: 100.00%

Classification Report:
              precision    recall  f1-score   support

       setosa       1.00      1.00      1.00        19
   versicolor       1.00      1.00      1.00         9
    virginica       1.00      1.00      1.00        17

  accuracy                            1.00        45
 macro avg       1.00      1.00      1.00        45
weighted avg       1.00      1.00      1.00        45
