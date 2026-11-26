from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load dataset
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.3, random_state=42)

# Train Decision Tree
clf = DecisionTreeClassifier(criterion='gini', max_depth=3, random_state=42)
clf.fit(X_train, y_train)

# Predict & Evaluate
y_pred = clf.predict(X_test)
print(f"Decision Tree Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%\n")

# Display decision rules
tree_rules = export_text(clf, feature_names=list(iris.feature_names))
print("Decision Rules:\n", tree_rules)


Sample Input: Iris feature dataset.

Sample Output:

Plaintext
Decision Tree Accuracy: 100.00%

Decision Rules:
 |--- petal width (cm) <= 0.80
 |   |--- class: 0
 |--- petal width (cm) >  0.80
 |   |--- petal width (cm) <= 1.75
 |   |   |--- petal length (cm) <= 4.95
 |   |   |   |--- class: 1
 |   |   |--- petal length (cm) >  4.95
 |   |   |   |--- class: 2
 |   |--- petal width (cm) >  1.75
 |   |   |--- petal length (cm) <= 4.85
 |   |   |   |--- class: 2
 |   |   |--- petal length (cm) >  4.85
 |   |   |   |--- class: 2
