# Install: pip install scikit-learn
from sklearn.tree import DecisionTreeClassifier
# Outlook: Sunny=0, Overcast=1, Rain=2
# Temperature: Cool=0, Mild=1, Hot=2
# Humidity: Normal=0, High=1; Wind: Weak=0, Strong=1
X=[[0,2,1,0],[0,2,1,1],[1,2,1,0],[2,1,1,0],
   [2,0,0,0],[2,0,0,1],[1,0,0,1],[0,1,1,0],
   [0,0,0,0],[2,1,0,0],[0,1,0,1],[1,1,1,1],
   [1,2,0,0],[2,1,1,1]]
y=[0,0,1,1,1,0,1,0,1,1,1,1,1,0]
model=DecisionTreeClassifier(random_state=0)
model.fit(X,y)
prediction=model.predict([[1,1,0,0]])
print("Prediction:","Play" if prediction[0]==1 else "Do Not Play")
print("Training accuracy:",round(model.score(X,y)*100,2),"%")

Output:
Prediction: Play
Training accuracy: 100.0 %
