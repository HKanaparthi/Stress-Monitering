from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Load the trained model and preprocessing objects
model = joblib.load('models/stress_model.pkl')
scaler = joblib.load('models/scaler.pkl')
feature_columns = joblib.load('models/feature_columns.pkl')
feature_importance = joblib.load('models/feature_importance.pkl')

# Stress level mapping
STRESS_LEVELS = {
    0: 'Low Risk',
    1: 'Moderate Risk',
    2: 'High Risk'
}

# Recommendations based on stress level
RECOMMENDATIONS = {
    0: [
        "Maintain your current healthy habits",
        "Continue regular exercise and good sleep schedule",
        "Keep practicing stress management techniques",
        "Stay connected with friends and family"
    ],
    1: [
        "Consider stress management techniques like deep breathing or meditation",
        "Ensure you're getting 7-8 hours of sleep each night",
        "Take regular breaks from academic work",
        "Talk to friends, family, or a counselor about your concerns",
        "Engage in physical activity or hobbies you enjoy"
    ],
    2: [
        "Consider speaking with a mental health professional",
        "Contact your institution's counseling services",
        "Reach out to trusted friends or family members",
        "Practice immediate stress relief techniques (deep breathing, progressive muscle relaxation)",
        "Prioritize sleep, nutrition, and basic self-care",
        "If experiencing crisis thoughts, contact emergency services immediately"
    ]
}

def get_feature_insights(prediction_data, top_n=3):
    """Get top contributing factors for the prediction"""
    # Get the most important features for this prediction
    feature_values = np.array(prediction_data).reshape(1, -1)
    feature_scaled = scaler.transform(feature_values)

    # Get feature importance scores
    importance_scores = feature_importance.set_index('feature')['importance']

    # Get top contributing factors based on feature importance and values
    insights = []
    for idx, feature in enumerate(feature_columns[:top_n]):
        if feature in importance_scores.index:
            insights.append({
                'factor': feature.replace('_', ' ').title(),
                'importance': float(importance_scores[feature]),
                'value': int(prediction_data[idx])
            })

    return sorted(insights, key=lambda x: x['importance'], reverse=True)[:top_n]

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'features_count': len(feature_columns)
    })

@app.route('/predict', methods=['POST'])
def predict_stress():
    """Predict stress level based on input features"""
    try:
        data = request.json

        # Validate input
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Extract features in the correct order
        features = []
        for feature in feature_columns:
            if feature not in data:
                return jsonify({'error': f'Missing required field: {feature}'}), 400
            features.append(data[feature])

        # Convert to numpy array and scale
        features_array = np.array(features).reshape(1, -1)
        features_scaled = scaler.transform(features_array)

        # Make prediction
        prediction = model.predict(features_scaled)[0]
        prediction_proba = model.predict_proba(features_scaled)[0]

        # Get confidence score
        confidence = float(max(prediction_proba))

        # Get feature insights
        insights = get_feature_insights(features)

        # Prepare response
        response = {
            'stress_level': int(prediction),
            'stress_label': STRESS_LEVELS[prediction],
            'confidence': round(confidence * 100, 1),
            'recommendations': RECOMMENDATIONS[prediction],
            'contributing_factors': insights,
            'disclaimer': 'This assessment is for informational purposes only and should not replace professional medical advice.'
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/features', methods=['GET'])
def get_features():
    """Get the list of required features for the model"""
    return jsonify({
        'features': feature_columns,
        'feature_descriptions': {
            'anxiety_level': 'Current anxiety level (0-21)',
            'self_esteem': 'Self-esteem level (0-30)',
            'mental_health_history': 'Mental health history (0=No, 1=Yes)',
            'depression': 'Depression level (0-27)',
            'headache': 'Headache frequency (0-5)',
            'blood_pressure': 'Blood pressure level (1-5)',
            'sleep_quality': 'Sleep quality (1-5)',
            'breathing_problem': 'Breathing problems (1-5)',
            'noise_level': 'Environment noise level (1-5)',
            'living_conditions': 'Living conditions quality (1-5)',
            'safety': 'Safety feeling (1-5)',
            'basic_needs': 'Basic needs fulfillment (1-5)',
            'academic_performance': 'Academic performance (1-5)',
            'study_load': 'Study workload (1-5)',
            'teacher_student_relationship': 'Teacher-student relationship (1-5)',
            'future_career_concerns': 'Future career concerns (1-5)',
            'social_support': 'Social support level (1-5)',
            'peer_pressure': 'Peer pressure level (1-5)',
            'extracurricular_activities': 'Extracurricular involvement (0-5)',
            'bullying': 'Bullying experience (1-5)'
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)