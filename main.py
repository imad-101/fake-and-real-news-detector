from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import re
import traceback

app = FastAPI(title="Fake News Detection API")

# Load model with error handling
try:
    model = joblib.load("model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")
    print("✓ Models loaded successfully")
except Exception as e:
    print(f"✗ Error loading models: {e}")
    model = None
    vectorizer = None

@app.get("/")
def read_root():
    return {
        "message": "Fake News Detection API",
        "status": "running",
        "model_loaded": model is not None,
        "endpoints": {
            "predict": "/predict",
            "docs": "/docs",
            "health": "/health"
        }
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy" if model is not None else "unhealthy",
        "model_loaded": model is not None,
        "vectorizer_loaded": vectorizer is not None
    }

class NewsRequest(BaseModel):
    text: str

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text

@app.post("/predict")
def predict_news(data: NewsRequest):
    try:
        # Check if models are loaded
        if model is None or vectorizer is None:
            raise HTTPException(
                status_code=503,
                detail="Model not loaded. Please check server logs."
            )
        
        # Validate input
        if not data.text or len(data.text.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="Text cannot be empty"
            )
        
        # Process and predict
        cleaned = clean_text(data.text)
        vector = vectorizer.transform([cleaned])
        prediction = model.predict(vector)[0]
        probability = model.predict_proba(vector)[0].max()

        return {
            "prediction": "Real" if prediction == 1 else "Fake",
            "confidence": round(float(probability), 2),
            "text_length": len(data.text),
            "cleaned_text_length": len(cleaned)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Prediction error: {str(e)}"
        )
