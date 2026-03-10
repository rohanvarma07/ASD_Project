# Autism Spectrum Disorder Detection System

A professional web-based system for autism detection using machine learning. This project provides an intuitive interface for uploading autism screening datasets and automatically generating predictions.

## 📋 Features

- **User Authentication**: Secure registration and login system
- **Dataset Upload**: Easy CSV file upload with validation
- **Automatic Detection**: ML-based autism detection without manual algorithm selection
- **Data Preview**: View uploaded dataset before processing
- **Visual Analytics**: Interactive charts and detailed statistics
- **Responsive Design**: Clean, modern UI that works on all devices
- **Result History**: Access previous prediction results

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3 (Custom, original design)
- Vanilla JavaScript

### Backend
- Python 3.8+
- Flask 2.3.3
- Pandas 2.0.3
- NumPy 1.24.3

## 📁 Project Structure

```
ASD_FEND/
│
├── templates/
│   ├── home.html           # Landing page
│   ├── about.html          # About ASD and the system
│   ├── register.html       # User registration
│   ├── login.html          # User login
│   ├── dashboard.html      # User dashboard
│   ├── upload.html         # Dataset upload
│   └── results.html        # Prediction results
│
├── static/
│   ├── css/
│   │   └── styles.css      # Complete styling
│   └── js/
│       └── script.js       # Client-side interactions
│
├── uploads/                # Uploaded CSV files (auto-created)
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

## ⚠️ Important Notes

- **Medical Disclaimer**: This system is for screening purposes only and should not replace professional medical diagnosis.
- **Data Privacy**: In production, implement proper data encryption and privacy measures.
- **Security**: Change the `secret_key` in `app.py` for production use.
- **Database**: Current version uses in-memory storage. For production, use a real database (SQLite, PostgreSQL, etc.).

## 🔧 Configuration

### File Upload Settings
- Maximum file size: 10MB
- Allowed formats: CSV only
- Upload directory: `uploads/`

### Session Settings
- Session timeout: Default Flask session timeout
- Secret key: Change in `app.py` for production

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
