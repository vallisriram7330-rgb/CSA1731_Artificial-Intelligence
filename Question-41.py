from sklearn.datasets import load_iris
from sklearn.decomposition import PCA

data = load_iris()
X = data.data  # Original shape: (150, 4)

pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X)

print("Original shape:", X.shape)
print("Reduced shape:", X_reduced.shape)
print("Explained variance ratio:", pca.explained_variance_ratio_)
