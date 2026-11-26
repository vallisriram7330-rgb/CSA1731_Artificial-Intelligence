from sklearn.datasets import load_iris
from sklearn.decomposition import PCA

# Load dataset (4 features)
iris = load_iris()
X = iris.data

# Apply PCA to reduce dimensions from 4 to 2
pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X)

print(f"Original shape: {X.shape}")
print(f"Reduced shape: {X_reduced.shape}")
print(f"Explained Variance Ratio: {pca.explained_variance_ratio_}")
print(f"Total Variance Retained: {sum(pca.explained_variance_ratio_) * 100:.2f}%")



Sample Input: Iris dataset shape (150, 4).

Sample Output:

Plaintext
Original shape: (150, 4)
Reduced shape: (150, 2)
Explained Variance Ratio: [0.92461872 0.05306657]
Total Variance Retained: 97.77%
