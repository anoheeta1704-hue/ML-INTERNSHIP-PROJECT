import pandas as pd
from sklearn.linear_model import LogisticRegression

def train_model():
    df = pd.read_csv("data/placement_data.csv")
    X = df[["skills_count", "cgpa", "projects"]]
    y = df["placed"]

    model = LogisticRegression()
    model.fit(X, y)
    return model

model = train_model()

def predict_placement(skills_count, cgpa, projects):
    probability = model.predict_proba([[skills_count, cgpa, projects]])[0][1]
    return round(probability * 100, 2)
