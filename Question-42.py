import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Rows = Users (U0, U1, U2), Columns = Items (I0, I1, I2, I3)
ratings = np.array([,
 ,
    [1, 1, 5, 4]
])

# Compute user-to-user similarity
user_sim = cosine_similarity(ratings)

# Predict U0's rating for unrated Item 2 (index 2) using weighted sum
weights = user_sim[0, 1:]
item_ratings = ratings[1:, 2]
predicted_rating = np.dot(weights, item_ratings) / np.sum(weights)

print(f"User Similarity Matrix:\n{np.round(user_sim, 2)}")
print(f"Predicted rating for User 0 on Item 2: {predicted_rating:.2f}")
