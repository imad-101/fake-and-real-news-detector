FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data
RUN python -c "import nltk; nltk.download('stopwords')"

# Copy application files (models last to use cache when code changes)
COPY main.py .

# Copy model files - updated Jan 13, 2026
COPY model.pkl .
COPY vectorizer.pkl .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
