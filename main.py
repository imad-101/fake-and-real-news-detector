from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import re

app = FastAPI(title="Fake News Detection API")

model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

class NewsRequest(BaseModel):
    text: str

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text

@app.post("/predict")
def predict_news(data: NewsRequest):
    cleaned = clean_text(data.text)
    vector = vectorizer.transform([cleaned])
    prediction = model.predict(vector)[0]
    probability = model.predict_proba(vector)[0].max()

    return {
        "prediction": "Real" if prediction == 1 else "Fake",
        "confidence": round(float(probability), 2)
    }
