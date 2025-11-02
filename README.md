# Student Stress Monitor - MVP

A complete web application that predicts student stress levels using machine learning and provides personalized recommendations.

## 🚀 Features

- **AI-Powered Stress Assessment**: Random Forest model with 90.45% accuracy
- **Interactive Assessment Form**: 20 comprehensive questions covering key stress factors
- **Real-time Predictions**: Instant stress level analysis with confidence scores
- **Personalized Recommendations**: Tailored advice based on stress level
- **Responsive Design**: Works on desktop and mobile devices
- **Professional UI**: Clean, user-friendly interface suitable for students

## 📊 Model Performance

- **Accuracy**: 90.45%
- **Model Type**: Random Forest Classifier
- **Dataset**: 1,100 student records with 20 features
- **Classes**: Low Risk, Moderate Risk, High Risk

### Top Contributing Factors:
1. Blood Pressure (16.1% importance)
2. Sleep Quality (9.1% importance)
3. Basic Needs (7.5% importance)
4. Academic Performance (7.1% importance)
5. Anxiety Level (6.6% importance)

## 🏗️ Architecture

```
├── backend/           # Flask API server
│   ├── app.py        # Main Flask application
│   ├── train_model.py # ML model training script
│   ├── requirements.txt
│   └── models/       # Trained model files
├── frontend/         # Web interface
│   ├── index.html    # Main HTML page
│   ├── style.css     # Styling
│   └── script.js     # Frontend logic
├── data/            # Dataset
└── docs/           # Documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### 1. Setup Backend

```bash
cd backend
pip install -r requirements.txt
```

### 2. Train the Model (Optional - already pre-trained)

```bash
python train_model.py
```

### 3. Start the API Server

```bash
python app.py
```

The API will be available at `http://localhost:5001`

### 4. Open the Frontend

Open `frontend/index.html` in your web browser, or serve it using a simple HTTP server:

```bash
cd frontend
python -m http.server 8000
```

Then visit `http://localhost:8000`

## 📡 API Endpoints

### Health Check
```bash
GET /health
```

### Stress Prediction
```bash
POST /predict
Content-Type: application/json

{
  "anxiety_level": 15,
  "self_esteem": 10,
  "mental_health_history": 1,
  "depression": 18,
  "headache": 4,
  "blood_pressure": 3,
  "sleep_quality": 2,
  "breathing_problem": 3,
  "noise_level": 4,
  "living_conditions": 2,
  "safety": 3,
  "basic_needs": 3,
  "academic_performance": 2,
  "study_load": 5,
  "teacher_student_relationship": 2,
  "future_career_concerns": 5,
  "social_support": 1,
  "peer_pressure": 4,
  "extracurricular_activities": 1,
  "bullying": 3
}
```

### Feature Information
```bash
GET /features
```

## 🎯 Assessment Questions

The application assesses 20 key stress factors:

1. **Anxiety Level** (0-21): Current anxiety level
2. **Self Esteem** (0-30): Self-esteem rating
3. **Mental Health History** (0/1): Previous mental health issues
4. **Depression** (0-27): Depression level
5. **Headache** (0-5): Headache frequency
6. **Blood Pressure** (1-5): Blood pressure concerns
7. **Sleep Quality** (1-5): Sleep quality rating
8. **Breathing Problems** (1-5): Breathing issue frequency
9. **Noise Level** (1-5): Environmental noise
10. **Living Conditions** (1-5): Quality of living situation
11. **Safety** (1-5): Feeling of safety
12. **Basic Needs** (1-5): Basic needs fulfillment
13. **Academic Performance** (1-5): Academic performance rating
14. **Study Load** (1-5): Academic workload burden
15. **Teacher-Student Relationship** (1-5): Relationship quality
16. **Future Career Concerns** (1-5): Career worry level
17. **Social Support** (1-5): Support system strength
18. **Peer Pressure** (1-5): Peer pressure level
19. **Extracurricular Activities** (0-5): Activity involvement
20. **Bullying** (1-5): Bullying experience

## 🎨 Stress Level Indicators

- **🟢 Low Risk**: Minimal stress, maintenance recommendations
- **🟡 Moderate Risk**: Active coping strategies needed
- **🔴 High Risk**: Professional support recommended

## 🚨 Emergency Resources

The application includes emergency contact information:
- Crisis Text Line: Text HOME to 741741
- National Suicide Prevention Lifeline: 988
- Campus Counseling Services

## 🔒 Privacy & Disclaimers

- ⚠️ This assessment is for informational purposes only
- 🏥 Should not replace professional medical advice
- 🔒 No personal data is stored or transmitted beyond the session
- 📱 Works offline after initial load

## 🌐 Deployment Options

### Option 1: Heroku
1. Create a `Procfile` in the backend directory:
   ```
   web: gunicorn app:app
   ```
2. Deploy to Heroku with the Python buildpack

### Option 2: Railway
1. Connect your GitHub repository
2. Railway will auto-detect the Python app
3. Set the start command: `python app.py`

### Option 3: Vercel (Frontend only)
1. Deploy the frontend directory to Vercel
2. Update the API_BASE_URL in script.js to point to your backend

### Option 4: Local Development
Perfect for testing and development as described in Quick Start

## 🛠️ Development

### Adding New Features
1. **New Questions**: Update the HTML form and corresponding API validation
2. **Model Improvements**: Retrain with new features in `train_model.py`
3. **UI Enhancements**: Modify `style.css` and `script.js`

### Model Retraining
```bash
cd backend
python train_model.py
```

This will:
- Load the latest dataset
- Train a new Random Forest model
- Save updated model files
- Display performance metrics

## 📈 Performance Metrics

- **Model Accuracy**: 90.45%
- **API Response Time**: <2 seconds
- **Frontend Load Time**: <3 seconds
- **Mobile Responsive**: ✅
- **Cross-browser Compatible**: ✅

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 👥 Support

For technical support or questions about mental health resources, please contact:
- Technical Issues: Open a GitHub issue
- Mental Health Support: Contact your local counseling services

---

**⚠️ Important Notice**: This application is designed to support mental health awareness and should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified health providers with questions about mental health conditions.