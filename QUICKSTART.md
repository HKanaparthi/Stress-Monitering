# 🚀 Quick Start Guide

Get the Student Stress Monitor application running in under 5 minutes!

## ⚡ One-Command Setup

```bash
bash setup.sh
```

This will automatically:
- ✅ Check Python installation
- 📦 Install all dependencies
- 🧠 Train the ML model (if needed)
- 🧪 Test the API
- 📋 Show you next steps

## 🏃‍♂️ Manual Setup (if preferred)

### 1. Install Dependencies
```bash
cd backend
pip install flask flask-cors scikit-learn joblib pandas
```

### 2. Train Model (if models/ directory is empty)
```bash
python train_model.py
```

### 3. Start Backend API
```bash
python app.py
```
Server will start at `http://localhost:5001`

### 4. Open Frontend
```bash
# Option 1: Direct file access
open frontend/index.html

# Option 2: Local web server
cd frontend
python -m http.server 8000
# Then visit http://localhost:8000
```

## 🎯 Test the Application

1. **Backend Test**: Visit `http://localhost:5001/health`
   - Should return: `{"status": "healthy", "model_loaded": true, "features_count": 20}`

2. **Frontend Test**: Open the web interface and fill out a few questions
   - Submit the form to get stress level prediction
   - Check that recommendations appear

## 📱 Using the App

1. **Fill Assessment Form**: Answer 20 questions about your current situation
2. **Get Results**: View your stress level (Low/Moderate/High Risk)
3. **Read Recommendations**: Follow personalized advice based on your results
4. **Emergency Resources**: Always available at the bottom of results

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Change port in backend/app.py, line 155:
app.run(debug=True, host='0.0.0.0', port=5002)  # Change 5001 to 5002

# Also update frontend/script.js, line 2:
const API_BASE_URL = 'http://localhost:5002';
```

### Module Not Found
```bash
pip install -r backend/requirements.txt
```

### Model Not Loading
```bash
cd backend
python train_model.py
```

## 🚀 Deploy to Production

See `docs/DEPLOYMENT.md` for complete deployment instructions to:
- Heroku (recommended)
- Railway
- Vercel
- AWS
- Digital Ocean

## ⚠️ Important Notes

- This is an educational tool, not a medical device
- Always seek professional help for serious mental health concerns
- Emergency contacts are provided in the app interface

## 🆘 Need Help?

1. Check `README.md` for detailed documentation
2. Review `docs/DEPLOYMENT.md` for deployment issues
3. Ensure Python 3.8+ is installed
4. Verify all files are in correct locations:

```
Aiproject/
├── backend/          # Flask API
├── frontend/         # Web interface
├── data/            # Dataset
├── docs/            # Documentation
└── setup.sh         # Automated setup
```

Ready to go! 🎉