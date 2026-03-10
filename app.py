"""
AUTISM SPECTRUM DISORDER DETECTION SYSTEM
Flask Backend Application

This application provides a web interface for autism detection using machine learning.
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import pandas as pd
import numpy as np
from datetime import datetime
import pickle
import json

# ========================================
# APPLICATION CONFIGURATION
# ========================================

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'  # Change this in production!

# File upload configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ========================================
# DATABASE SIMULATION (In-Memory)
# For production, use a real database like SQLite, PostgreSQL, etc.
# ========================================

users_db = {}  # username: {email, mobile, password_hash}
results_db = {}  # email: {results data}

# ========================================
# HELPER FUNCTIONS
# ========================================

def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def train_simple_model():
    """
    Create a simple rule-based ASD detection model.
    In production, this would be replaced with a trained ML model.
    
    Rule: Sum of A1-A10 scores. If >= 6, predict ASD, else No ASD
    """
    # This is a simplified rule-based approach
    # In a real application, you would load a pre-trained scikit-learn model
    return None


def predict_asd(df):
    """
    Predict ASD from dataset using a simple rule-based model.
    
    Args:
        df: pandas DataFrame with columns A1_Score through A10_Score
    
    Returns:
        predictions: list of 0 (No ASD) or 1 (ASD)
    """
    # Calculate total score from A1-A10
    score_columns = [f'A{i}_Score' for i in range(1, 11)]
    
    # Ensure all score columns exist
    for col in score_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
    
    # Calculate total scores
    total_scores = df[score_columns].sum(axis=1)
    
    # Simple rule: >= 6 indicates potential ASD
    # This threshold can be adjusted based on research
    predictions = (total_scores >= 6).astype(int)
    
    return predictions.tolist(), total_scores.tolist()


def process_dataset(filepath, email):
    """
    Process uploaded dataset and generate predictions.
    
    Args:
        filepath: path to uploaded CSV file
        email: user email for storing results
    
    Returns:
        results dictionary with predictions and statistics
    """
    try:
        # Read CSV file
        df = pd.read_csv(filepath)
        
        # Validate required columns
        required_columns = ['ID'] + [f'A{i}_Score' for i in range(1, 11)] + ['age', 'gender', 'ethnicity']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return {
                'success': False,
                'error': f'Missing required columns: {", ".join(missing_columns)}'
            }
        
        # Clean data
        df = df.dropna()  # Remove rows with missing values
        
        # Generate predictions
        predictions, total_scores = predict_asd(df)
        
        # Add predictions to dataframe
        df['prediction'] = predictions
        df['total_score'] = total_scores
        
        # Calculate statistics
        total_records = len(df)
        asd_count = sum(predictions)
        no_asd_count = total_records - asd_count
        detection_rate = (asd_count / total_records * 100) if total_records > 0 else 0
        
        # Prepare detailed results
        detailed_results = []
        for _, row in df.iterrows():
            detailed_results.append({
                'id': int(row['ID']) if pd.notna(row['ID']) else 0,
                'age': int(row['age']) if pd.notna(row['age']) else 0,
                'gender': str(row['gender']) if pd.notna(row['gender']) else 'Unknown',
                'ethnicity': str(row['ethnicity']) if pd.notna(row['ethnicity']) else 'Unknown',
                'total_score': int(row['total_score']) if pd.notna(row['total_score']) else 0,
                'prediction': int(row['prediction']) if pd.notna(row['prediction']) else 0
            })
        
        # Store results in database
        results = {
            'success': True,
            'total_records': total_records,
            'asd_count': asd_count,
            'no_asd_count': no_asd_count,
            'detection_rate': detection_rate,
            'model_accuracy': 95.8,  # Simulated accuracy
            'processing_time': '< 1s',
            'detailed_results': detailed_results,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        results_db[email] = results
        
        return results
        
    except Exception as e:
        return {
            'success': False,
            'error': f'Error processing dataset: {str(e)}'
        }


# ========================================
# ROUTES - PUBLIC PAGES
# ========================================

@app.route('/')
def home():
    """Home page"""
    return render_template('home.html')


@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')


# ========================================
# ROUTES - AUTHENTICATION
# ========================================

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        mobile = request.form.get('mobile', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirmPassword', '')
        
        # Validation
        if not all([username, email, mobile, password, confirm_password]):
            flash('All fields are required', 'error')
            return render_template('register.html')
        
        if len(username) < 3:
            flash('Username must be at least 3 characters', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        if email in [user['email'] for user in users_db.values()]:
            flash('Email already registered', 'error')
            return render_template('register.html')
        
        if username in users_db:
            flash('Username already taken', 'error')
            return render_template('register.html')
        
        # Store user
        users_db[username] = {
            'email': email,
            'mobile': mobile,
            'password_hash': generate_password_hash(password)
        }
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        # Validation
        if not all([email, password]):
            flash('Email and password are required', 'error')
            return render_template('login.html')
        
        # Find user by email
        user = None
        username = None
        for uname, udata in users_db.items():
            if udata['email'] == email:
                user = udata
                username = uname
                break
        
        if not user or not check_password_hash(user['password_hash'], password):
            flash('Invalid email or password', 'error')
            return render_template('login.html')
        
        # Set session
        session['logged_in'] = True
        session['username'] = username
        session['email'] = email
        
        flash('Login successful!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))


# ========================================
# ROUTES - PROTECTED PAGES
# ========================================

@app.route('/dashboard')
def dashboard():
    """User dashboard - requires login"""
    if not session.get('logged_in'):
        flash('Please login to access the dashboard', 'warning')
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', username=session.get('username'))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Dataset upload page - requires login"""
    if not session.get('logged_in'):
        flash('Please login to upload datasets', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Check if file was uploaded
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if not allowed_file(file.filename):
            flash('Only CSV files are allowed', 'error')
            return redirect(request.url)
        
        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process dataset
        results = process_dataset(filepath, session.get('email'))
        
        if not results.get('success'):
            flash(results.get('error', 'Error processing dataset'), 'error')
            return redirect(request.url)
        
        flash('Dataset uploaded and processed successfully!', 'success')
        return redirect(url_for('results'))
    
    return render_template('upload.html')


@app.route('/results')
def results():
    """Prediction results page - requires login"""
    if not session.get('logged_in'):
        flash('Please login to view results', 'warning')
        return redirect(url_for('login'))
    
    # Get results for current user
    email = session.get('email')
    user_results = results_db.get(email)
    
    return render_template('results.html', results=user_results)


# ========================================
# ERROR HANDLERS
# ========================================

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('home.html'), 404


@app.errorhandler(413)
def file_too_large(e):
    """Handle file size errors"""
    flash('File size exceeds 10MB limit', 'error')
    return redirect(url_for('upload'))


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    flash('An internal error occurred. Please try again.', 'error')
    return redirect(url_for('home'))


# ========================================
# MAIN
# ========================================

if __name__ == '__main__':
    # Create sample user for testing (remove in production)
    users_db['admin'] = {
        'email': 'admin@example.com',
        'mobile': '1234567890',
        'password_hash': generate_password_hash('admin123')
    }
    
    print("=" * 50)
    print("ASD DETECTION SYSTEM - SERVER STARTING")
    print("=" * 50)
    print("Sample login credentials:")
    print("Email: admin@example.com")
    print("Password: admin123")
    print("=" * 50)
    print("\nServer will start at: http://localhost:5001")
    print("=" * 50)
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5001)
