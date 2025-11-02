#!/bin/bash

echo "🚀 Setting up Student Stress Monitor Application..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3.8+ and try again."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Create virtual environment (optional but recommended)
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate || source venv/Scripts/activate 2>/dev/null

# Install backend dependencies
echo "📚 Installing backend dependencies..."
cd backend
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies. Please check your Python and pip installation."
    exit 1
fi

echo "✅ Dependencies installed successfully"

# Train the model if not already trained
if [ ! -f "models/stress_model.pkl" ]; then
    echo "🧠 Training machine learning model..."
    python train_model.py

    if [ $? -ne 0 ]; then
        echo "❌ Failed to train model. Please check the data and dependencies."
        exit 1
    fi

    echo "✅ Model trained successfully"
else
    echo "✅ Model already exists"
fi

# Test the API
echo "🧪 Testing API endpoints..."
python -c "
import requests
import json
try:
    # Start server in background for testing
    import subprocess
    import time
    import signal

    # Start server
    proc = subprocess.Popen(['python', 'app.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(3)  # Wait for server to start

    # Test health endpoint
    response = requests.get('http://localhost:5001/health')
    if response.status_code == 200:
        print('✅ API health check passed')
    else:
        print('❌ API health check failed')

    # Kill the test server
    proc.terminate()
    proc.wait()

except Exception as e:
    print(f'⚠️  API test skipped: {e}')
"

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "🚀 To start the application:"
echo "1. Start the backend server:"
echo "   cd backend && python app.py"
echo ""
echo "2. Open the frontend:"
echo "   Open frontend/index.html in your browser"
echo "   Or serve it: cd frontend && python -m http.server 8000"
echo ""
echo "📚 For deployment instructions, see docs/DEPLOYMENT.md"
echo "📖 For usage instructions, see README.md"
echo ""
echo "⚠️  Important: This application is for educational purposes only."
echo "   It should not replace professional medical advice."