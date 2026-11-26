import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Sample User-Item Rating Matrix (Rows: Users, Columns: Movies)
# Movies: [Inception, Interstellar, Titanic, Avengers, Toy Story]
ratings = np.array([
    [5, 5, 0, 2, 1],
    [4, 0, 0, 3, 2],
    [0, 0, 5, 4, 5],
    [2, 1, 4, 5, 4],
    [5, 4, 1, 0, 0]
])

# Compute item-item cosine similarity matrix
item_similarity = cosine_similarity(ratings.T)

# Function to recommend movies for a given item index
def recommend_similar_item(movie_idx):
    similar_scores = item_similarity[movie_idx]
    similar_item_idx = np.argsort(similar_scores)[-2] # Second highest (highest is itself)
    return similar_item_idx

target_movie = 0 # Inception
recommended_movie = recommend_similar_item(target_movie)
print(f"If the user liked Movie #{target_movie}, recommended Movie index is: #{recommended_movie}")



Sample Input: A $5 \times 5$ user-item rating matrix across 5 users and 5 movies.Sample Output:PlaintextIf the user liked Movie #0, recommended Movie index is: #1
