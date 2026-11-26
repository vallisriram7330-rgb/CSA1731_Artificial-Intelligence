from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Sample labeled sentences (1 = Positive, 0 = Negative)
texts = [
    "I love this product, it is amazing",
    "Great performance and easy to use",
    "Worst experience ever, completely broken",
    "Terrible quality and waste of money"
]
labels = [1, 1, 0, 0]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)

model = MultinomialNB()
model.fit(X, labels)

# Test sentiment on new text
sample = vectorizer.transform(["This is an amazing and great tool"])
prediction = model.predict(sample)
print("Sentiment:", "Positive" if prediction[0] == 1 else "Negative")
