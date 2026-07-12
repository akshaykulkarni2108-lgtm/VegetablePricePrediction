import joblib

model = joblib.load("models/random_forest.pkl")

def predict_price(data):
    prediction = model.predict(data)
    return prediction