# Autism Spectrum Disorder Detection System

A professional web-based system for autism detection using machine learning. This project provides an intuitive interface for uploading autism screening datasets and automatically generating predictions with persistent database storage.

🌐 **Live Demo**: [Deploy on Render](https://render.com) | [See Deployment Guide](docs/DEPLOYMENT_GUIDE.md)

## 📋 Features

- **User Authentication**: Secure registration and login system with encrypted passwords
- **Database Backend**: PostgreSQL (production) / SQLite (development) for persistent data storage
- **Dataset Upload**: Easy CSV file upload with validation and tracking
- **Automatic Detection**: ML-based autism detection without manual algorithm selection
- **Visual Analytics**: Interactive charts and detailed statistics
- **Result History**: Access previous prediction results from database
- **Responsive Design**: Clean, modern UI that works on all devices
- **Production Ready**: Configured for deployment on Render, Heroku, Railway, etc.

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3 (Custom, original design - 719 lines)
- Vanilla JavaScript (492 lines)

### Backend
- Python 3.11+
- Flask 2.3.3
- Pandas 2.0.3
- NumPy 1.24.3
- SQLite3 (development)
- PostgreSQL (production via psycopg2-binary)

### Deployment
- Gunicorn 21.2.0 (production server)
- Render / Heroku / Railway compatible

## 📁 Project Structure

```
ASD_FEND/
├── app.py                          # Main Flask application (430 lines)
├── database.py                     # Database module (681 lines)
├── requirements.txt                # Python dependencies
├── Procfile                        # Production deployment config
├── runtime.txt                     # Python version specification
├── .gitignore                      # Git ignore rules
├── README.md                       # This file
├── asd_database.db                 # SQLite database (local dev)
├── sample_autism_dataset.csv       # Sample data for testing
│
├── templates/                      # HTML templates (7 files)
│   ├── home.html                  # Landing page
│   ├── about.html                 # About ASD and the system
│   ├── register.html              # User registration
│   ├── login.html                 # User login
│   ├── dashboard.html             # User dashboard
│   ├── upload.html                # Dataset upload
│   └── results.html               # Prediction results
│
├── static/                         # Static assets
│   ├── css/
│   │   └── styles.css             # Complete styling (719 lines)
│   └── js/
│       └── script.js              # Client-side interactions (492 lines)
│
├── docs/                           # Documentation
│   ├── DATABASE_SETUP_GUIDE.md    # Complete database documentation
│   ├── DATABASE_QUICK_START.md    # Quick reference
│   ├── DEPLOYMENT_GUIDE.md        # Production deployment guide
│   ├── RENDER_DATABASE_WARNING.md # Critical deployment info
│   ├── QUICK_DEPLOY_RENDER.txt    # 5-minute deployment
│   ├── DATABASE_IMPLEMENTATION_SUMMARY.md
│   └── DATABASE_VERIFICATION_REPORT.md
│
├── models/                         # ML models directory (future use)
│   └── .gitkeep
│
└── uploads/                        # User-uploaded CSV files
    └── .gitkeep
```
├── models/                 # ML models directory (auto-created)
│
├── app.py                  # Flask backend application
├── requirements.txt        # Python dependencies
├── sample_autism_dataset.csv  # Sample dataset for testing
└── README.md              # This file
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project

```bash
cd ASD_FEND
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5001`

**Note:** Port changed from 5000 to 5001 because macOS uses port 5000 for AirPlay Receiver.

## 🚀 Production Deployment

Ready to deploy your app to the world? See our comprehensive deployment guides:

### Quick Deploy (5 minutes)
- **[Render](https://render.com)** - Recommended for beginners
  - ✅ Free tier available
  - ✅ Automatic deployments from GitHub
  - ✅ HTTPS included
  - 📖 [Quick Deploy Guide](QUICK_DEPLOY_RENDER.txt)

### Other Options
- **PythonAnywhere** - Python-focused hosting
- **Heroku** - Popular platform (paid)
- **Railway** - Modern deployment platform

📖 **Full Deployment Guide**: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

### Pre-Deployment Checklist
- [x] Procfile created
- [x] runtime.txt configured
- [x] requirements.txt includes gunicorn
- [x] Environment variables configured
- [x] Production-ready app.py


## 💻 Usage Guide

### 1. Register an Account
- Navigate to the Register page
- Fill in your details:
  - Username (minimum 3 characters)
  - Email address
  - Mobile number (10 digits)
  - Password (minimum 6 characters)
  - Confirm password
- Click "Create Account"

### 2. Login
- Use your registered email and password
- You'll be redirected to the dashboard

### 3. Upload Dataset
- Click "Upload Dataset" from the dashboard
- Select your CSV file (must contain required columns)
- Click "Upload and Process Dataset"
- View the data preview

### 4. View Results
- Access "Prediction Results" to see:
  - Total records analyzed
  - Number of ASD detected cases
  - Number of non-ASD cases
  - Detection rate percentage
  - Visual charts
  - Detailed predictions table

## 📊 Dataset Format

Your CSV file must contain the following columns:

| Column Name | Description | Data Type | Values |
|-------------|-------------|-----------|--------|
| ID | Unique identifier | Integer | 1, 2, 3, ... |
| A1_Score | Question 1 response | Binary | 0 or 1 |
| A2_Score | Question 2 response | Binary | 0 or 1 |
| A3_Score | Question 3 response | Binary | 0 or 1 |
| A4_Score | Question 4 response | Binary | 0 or 1 |
| A5_Score | Question 5 response | Binary | 0 or 1 |
| A6_Score | Question 6 response | Binary | 0 or 1 |
| A7_Score | Question 7 response | Binary | 0 or 1 |
| A8_Score | Question 8 response | Binary | 0 or 1 |
| A9_Score | Question 9 response | Binary | 0 or 1 |
| A10_Score | Question 10 response | Binary | 0 or 1 |
| age | Age of individual | Integer | Any positive number |
| gender | Gender | Character | m, f, male, female |
| ethnicity | Ethnic background | Text | Any text |

### Sample Dataset

A sample dataset (`sample_autism_dataset.csv`) is included in the project for testing.

## 🔐 Default Test Credentials

For testing purposes, a default admin account is created:

```
Email: admin@example.com
Password: admin123
```

**Note**: Remove this in production!

## 🎨 Design Philosophy

The UI follows a clean, medical-style design with:
- Soft color palette suitable for healthcare applications
- Card-based layout for better content organization
- Responsive design for mobile and desktop
- Intuitive navigation
- Professional typography
- Smooth transitions and interactions

## 🧠 Machine Learning Model

The current implementation uses a **rule-based approach** for demonstration:
- Calculates sum of A1-A10 scores
- If total score ≥ 6: Predicts ASD
- If total score < 6: Predicts No ASD

### Upgrading to a Real ML Model

To use a trained machine learning model:

1. Train your model using scikit-learn:
```python
from sklearn.ensemble import RandomForestClassifier
# Train your model
model = RandomForestClassifier()
model.fit(X_train, y_train)
```

2. Save the model:
```python
import pickle
with open('models/asd_model.pkl', 'wb') as f:
    pickle.dump(model, f)
```

3. Update the `predict_asd()` function in `app.py` to load and use the model.

## 📚 Documentation

Comprehensive guides are available in the `docs/` directory:

- **[DATABASE_SETUP_GUIDE.md](docs/DATABASE_SETUP_GUIDE.md)** - Complete database setup and configuration
- **[DATABASE_QUICK_START.md](docs/DATABASE_QUICK_START.md)** - Quick reference for database operations
- **[DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)** - Full production deployment guide
- **[QUICK_DEPLOY_RENDER.txt](docs/QUICK_DEPLOY_RENDER.txt)** - 5-minute deployment to Render
- **[RENDER_DATABASE_WARNING.md](docs/RENDER_DATABASE_WARNING.md)** - ⚠️ Critical info about database deployment

## ⚠️ Important Notes

- **Medical Disclaimer**: This system is for screening purposes only and should not replace professional medical diagnosis.
- **Data Privacy**: User passwords are hashed, and data is stored securely in the database.
- **Database**: Uses SQLite for local development and PostgreSQL for production deployment.
- **Security**: Secret key uses environment variable in production. Always set `SECRET_KEY` environment variable when deploying.
- **File Storage**: Uploaded files are stored locally. For production, consider cloud storage (S3, Cloudinary, etc.).

## 🔧 Configuration

### File Upload Settings
- Maximum file size: 10MB
- Allowed formats: CSV only
- Upload directory: `uploads/`

### Database Settings
- Development: SQLite (`asd_database.db`)
- Production: PostgreSQL (set `DATABASE_URL` environment variable)
- Auto-detection based on environment

### Session Settings
- Session security: Encrypted with SECRET_KEY
- Secret key: From environment variable or default (change in production)

## 🐛 Troubleshooting

### Port Already in Use
If port 5000 is already in use, change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use different port
```

### Module Not Found Errors
Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### File Upload Errors
Check that the `uploads/` directory exists and has write permissions.

## 📈 Future Enhancements

- [ ] Implement real ML model (Random Forest, SVM, Neural Network)
- [ ] Add database support (SQLite/PostgreSQL)
- [ ] User profile management
- [ ] Export results to PDF
- [ ] Email notifications
- [ ] Multi-language support
- [ ] API endpoints for integration
- [ ] Advanced visualizations with Chart.js/D3.js

## 📄 License

This project is developed for educational and research purposes.

## 👨‍💻 Development

This project is designed as a student project demonstrating full-stack web development with machine learning integration.

## 📞 Support

For questions or issues, please refer to the code comments or contact your instructor.

---

**Developed for Educational Purposes | 2026**
