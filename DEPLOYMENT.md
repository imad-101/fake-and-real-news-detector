# Deployment Guide - Fake News Detector API

## Option 1: Render (Recommended - Free Tier Available)

### Steps:
1. Create account at [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name:** fake-news-detector
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt && python -c "import nltk; nltk.download('stopwords')"`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Click "Create Web Service"

**URL:** `https://your-app-name.onrender.com`

---

## Option 2: Railway (Easy & Fast)

### Steps:
1. Create account at [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway auto-detects Python and deploys
5. Add environment variables if needed

**URL:** Auto-generated Railway URL

---

## Option 3: Docker Container (Any Platform)

### Build and Run Locally:
```bash
# Build image
docker build -t fake-news-detector .

# Run container
docker run -p 8000:8000 fake-news-detector
```

### Deploy to Docker Hub:
```bash
# Tag image
docker tag fake-news-detector your-username/fake-news-detector

# Push to Docker Hub
docker push your-username/fake-news-detector
```

---

## Option 4: AWS EC2 (Traditional Cloud)

### Steps:
1. Launch EC2 instance (Ubuntu 22.04)
2. SSH into instance
3. Install dependencies:
```bash
sudo apt update
sudo apt install python3-pip python3-venv -y
```

4. Clone your code and setup:
```bash
git clone your-repo
cd fake-news-ml
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -c "import nltk; nltk.download('stopwords')"
```

5. Run with nohup or systemd:
```bash
nohup uvicorn main:app --host 0.0.0.0 --port 8000 &
```

6. Configure security group to allow port 8000

---

## Option 5: Google Cloud Run (Serverless)

### Steps:
1. Install Google Cloud SDK
2. Build and push container:
```bash
gcloud builds submit --tag gcr.io/YOUR-PROJECT-ID/fake-news-detector
```

3. Deploy:
```bash
gcloud run deploy fake-news-detector \
  --image gcr.io/YOUR-PROJECT-ID/fake-news-detector \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## Option 6: DigitalOcean App Platform

### Steps:
1. Create account at [digitalocean.com](https://digitalocean.com)
2. Go to App Platform → Create App
3. Connect GitHub repository
4. Configure:
   - **Type:** Web Service
   - **Build Command:** `pip install -r requirements.txt`
   - **Run Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Click "Create Resources"

---

## Important Notes:

### Before Deployment:
- ✅ Ensure `model.pkl` and `vectorizer.pkl` are in your repository
- ✅ Push all code to GitHub
- ✅ Test locally first: `uvicorn main:app --reload`

### Environment Variables (if needed):
```
PORT=8000
WORKERS=1
```

### Free Tier Options:
- **Render:** 750 hours/month free
- **Railway:** $5 free credits/month
- **Google Cloud Run:** 2 million requests/month free
- **AWS Lambda + API Gateway:** 1 million requests/month free

### Production Recommendations:
1. Add authentication/API keys
2. Implement rate limiting
3. Add logging and monitoring
4. Use HTTPS (most platforms auto-provide)
5. Set up CORS if needed for frontend

### Testing Deployed API:
```bash
curl -X POST "https://your-app.com/predict" \
  -H "Content-Type: application/json" \
  -d '{"text": "Your news article here"}'
```

---

## Fastest Deployment (5 minutes):

**Use Railway:**
1. Go to railway.app
2. "New Project" → "Deploy from GitHub"
3. Select repo → Done!

Your API will be live with auto-generated URL.
