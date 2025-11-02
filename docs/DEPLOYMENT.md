# Deployment Guide

This guide covers different deployment options for the Student Stress Monitor application.

## 🚀 Deployment Options

### 1. Heroku Deployment (Recommended)

#### Prerequisites
- Heroku account
- Heroku CLI installed
- Git repository

#### Steps

1. **Prepare the backend for Heroku**
   ```bash
   cd backend
   ```

2. **Initialize git repository (if not already done)**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

3. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

4. **Set environment variables (optional)**
   ```bash
   heroku config:set FLASK_ENV=production
   ```

5. **Deploy to Heroku**
   ```bash
   git push heroku main
   ```

6. **Update frontend API URL**
   - Update `API_BASE_URL` in `frontend/script.js` to your Heroku app URL
   - Example: `https://your-app-name.herokuapp.com`

#### Files needed for Heroku:
- `Procfile` ✅ (already created)
- `runtime.txt` ✅ (already created)
- `requirements.txt` ✅ (already created)

### 2. Railway Deployment

#### Steps

1. **Connect to Railway**
   - Go to [railway.app](https://railway.app)
   - Connect your GitHub repository
   - Select the backend folder as the root

2. **Configure build settings**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`

3. **Environment Variables**
   - Set `PORT` to `5001` (or Railway will assign automatically)

4. **Deploy**
   - Railway auto-deploys on git push

### 3. Vercel Deployment (Frontend + Serverless Backend)

#### Frontend Deployment

1. **Deploy frontend to Vercel**
   ```bash
   cd frontend
   vercel --prod
   ```

2. **Or connect GitHub repository**
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Set build settings to serve the `frontend` directory

#### Backend as Serverless Function

1. **Convert Flask app to Vercel serverless function**
   - Create `api/` directory in project root
   - Move Flask app logic to `api/app.py`
   - Update imports and structure for Vercel

### 4. Digital Ocean App Platform

#### Steps

1. **Create App on Digital Ocean**
   - Go to App Platform in Digital Ocean console
   - Connect GitHub repository

2. **Configure build settings**
   ```yaml
   name: student-stress-monitor
   services:
   - name: backend
     source_dir: /backend
     github:
       repo: your-username/your-repo
       branch: main
     run_command: gunicorn app:app
     environment_slug: python
     instance_count: 1
     instance_size_slug: basic-xxs
   ```

### 5. AWS EC2 Deployment

#### Steps

1. **Launch EC2 instance**
   - Choose Ubuntu 20.04 LTS
   - Configure security groups for HTTP/HTTPS

2. **Install dependencies**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip nginx
   ```

3. **Clone and setup application**
   ```bash
   git clone your-repo
   cd your-repo/backend
   pip3 install -r requirements.txt
   ```

4. **Configure Nginx**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:5001;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

5. **Run with PM2 or systemd**
   ```bash
   sudo npm install -g pm2
   pm2 start app.py --interpreter python3
   ```

## 🔧 Environment Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Port for the Flask app | `5001` |
| `FLASK_ENV` | Flask environment | `development` |
| `DEBUG` | Enable debug mode | `True` |

### Production Settings

For production deployment, update `app.py`:

```python
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run(debug=debug, host='0.0.0.0', port=port)
```

## 🌐 Frontend Deployment Options

### Static Hosting
- **Netlify**: Drag and drop `frontend` folder
- **Vercel**: Connect GitHub and deploy
- **GitHub Pages**: Enable in repository settings
- **Firebase Hosting**: Use Firebase CLI

### CDN Integration
- CloudFlare for performance
- AWS CloudFront for scalability

## 🔒 Security Considerations

### Production Checklist
- [ ] Set `DEBUG=False` in production
- [ ] Use HTTPS (SSL certificates)
- [ ] Configure CORS properly
- [ ] Add rate limiting
- [ ] Input validation and sanitization
- [ ] Error handling and logging
- [ ] Environment variables for sensitive data

### CORS Configuration
Update CORS settings in `app.py` for production:

```python
from flask_cors import CORS

# Development
CORS(app)

# Production
CORS(app, origins=['https://yourdomain.com'])
```

## 📊 Monitoring and Logging

### Application Monitoring
- **Heroku**: Built-in logging and metrics
- **Railway**: Integrated monitoring dashboard
- **Custom**: Implement logging with Python's `logging` module

### Health Checks
The application includes a health check endpoint at `/health`:

```bash
curl https://your-app.herokuapp.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "features_count": 20
}
```

## 🚦 Testing Deployment

### Pre-deployment Testing
1. **Local testing**
   ```bash
   python app.py
   curl http://localhost:5001/health
   ```

2. **Model validation**
   ```bash
   python train_model.py
   ```

3. **API testing**
   - Test all endpoints
   - Validate response formats
   - Check error handling

### Post-deployment Testing
1. **Health check**: Visit `/health` endpoint
2. **Frontend integration**: Test form submission
3. **Load testing**: Use tools like Apache Bench
4. **Cross-browser testing**: Ensure compatibility

## 🔄 CI/CD Pipeline

### GitHub Actions Example

```yaml
name: Deploy to Heroku

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Deploy to Heroku
      uses: akhileshns/heroku-deploy@v3.12.12
      with:
        heroku_api_key: ${{secrets.HEROKU_API_KEY}}
        heroku_app_name: "your-app-name"
        heroku_email: "your-email@example.com"
        appdir: "backend"
```

## 📝 Troubleshooting

### Common Issues

1. **Port binding errors**
   - Ensure `PORT` environment variable is set
   - Check if port is already in use

2. **Module import errors**
   - Verify all dependencies in `requirements.txt`
   - Check Python version compatibility

3. **CORS errors**
   - Update CORS configuration
   - Check frontend API URL

4. **Model loading errors**
   - Ensure model files are included in deployment
   - Check file paths are relative

### Logs and Debugging

```bash
# Heroku logs
heroku logs --tail

# Railway logs
railway logs

# Local debugging
export FLASK_ENV=development
python app.py
```

## 📞 Support

For deployment issues:
1. Check platform-specific documentation
2. Review application logs
3. Test locally first
4. Verify all configuration files

Remember to update the frontend `API_BASE_URL` to match your deployed backend URL!