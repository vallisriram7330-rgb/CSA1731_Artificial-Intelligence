from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report

# Generate synthetic binary classification dataset
X, y = make_blobs(n_samples=200, centers=2, random_state=42, cluster_std=1.2)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train SVM Classifier
svm_model = SVC(kernel='linear')
svm_model.fit(X_train, y_train)

# Evaluate
y_pred = svm_model.predict(X_test)
print(f"SVM Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%\n")
print("Classification Report:\n", classification_report(y_test, y_pred))


Sample Input: 200 samples of 2-feature linearly separable binary data generated via make_blobs.

Sample Output:

Plaintext
SVM Accuracy: 100.00%

Classification Report:
              precision    recall  f1-score   support

         0       1.00      1.00      1.00        31
         1       1.00      1.00      1.00        29

  accuracy                           1.00        60
 macro avg       1.00      1.00      1.00        60
weighted avg       1.00      1.00      1.00        60
