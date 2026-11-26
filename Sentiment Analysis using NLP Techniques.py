from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Sample Dataset
corpus = [
    "The product is amazing and works perfectly.",
    "Terrible quality, broke after one day.",
    "Very happy with this purchase, excellent service!",
    "Worst experience ever, complete waste of money.",
    "Absolutely wonderful, highly recommend it!"
]
labels = [1, 0, 1, 0, 1] # 1: Positive, 0: Negative

# Convert text data to TF-IDF features
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(corpus)

# Train Classifier
model = LogisticRegression()
model.fit(X_train, labels)

# Test with new sentences
test_sentences = ["An absolute masterpiece, loved it!", "Broken and useless."]
X_test = vectorizer.transform(test_sentences)
predictions = model.predict(X_test)

for sent, pred in zip(test_sentences, predictions):
    sentiment = "Positive" if pred == 1 else "Negative"
    print(f"Review: '{sent}' --> Sentiment: {sentiment}")





Sample Input: Custom corpus of 5 labeled product review sentences and test sentences.

Sample Output:

Plaintext
Review: 'An absolute masterpiece, loved it!' --> Sentiment: Positive
Review: 'Broken and useless.' --> Sentiment: Negative
