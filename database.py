"""
DATABASE MODULE
Handles all database operations for ASD Detection System
Supports SQLite (development) and PostgreSQL (production)
"""

import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import json

class Database:
    """Database handler for user authentication and file storage"""
    
    def __init__(self, db_path='asd_database.db'):
        """Initialize database connection"""
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Access columns by name
        return conn
    
    def init_database(self):
        """Create database tables if they don't exist"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                mobile TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')
        
        # Create uploaded_files table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS uploaded_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_email TEXT NOT NULL,
                filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_size INTEGER,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_email) REFERENCES users (email)
            )
        ''')
        
        # Create analysis_results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analysis_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_email TEXT NOT NULL,
                file_id INTEGER,
                total_cases INTEGER,
                asd_positive INTEGER,
                asd_negative INTEGER,
                accuracy_score REAL,
                confidence_score REAL,
                results_data TEXT,
                analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_email) REFERENCES users (email),
                FOREIGN KEY (file_id) REFERENCES uploaded_files (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print("✅ Database initialized successfully!")
    
    # ========================================
    # USER MANAGEMENT
    # ========================================
    
    def register_user(self, email, mobile, password):
        """Register a new user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Check if user already exists
            cursor.execute('SELECT email FROM users WHERE email = ?', (email,))
            if cursor.fetchone():
                conn.close()
                return False, "Email already registered"
            
            # Hash password and insert user
            password_hash = generate_password_hash(password)
            cursor.execute('''
                INSERT INTO users (email, mobile, password_hash)
                VALUES (?, ?, ?)
            ''', (email, mobile, password_hash))
            
            conn.commit()
            conn.close()
            return True, "Registration successful"
        
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def login_user(self, email, password):
        """Authenticate user login"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            user = cursor.fetchone()
            
            if not user:
                conn.close()
                return False, "Email not found"
            
            # Check password
            if not check_password_hash(user['password_hash'], password):
                conn.close()
                return False, "Incorrect password"
            
            # Update last login
            cursor.execute('''
                UPDATE users SET last_login = CURRENT_TIMESTAMP
                WHERE email = ?
            ''', (email,))
            conn.commit()
            conn.close()
            
            return True, {
                'email': user['email'],
                'mobile': user['mobile'],
                'created_at': user['created_at']
            }
        
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_user(self, email):
        """Get user details"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT email, mobile, created_at, last_login FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return dict(user)
        return None
    
    # ========================================
    # FILE MANAGEMENT
    # ========================================
    
    def save_uploaded_file(self, user_email, filename, file_path, file_size):
        """Save uploaded file information"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO uploaded_files (user_email, filename, file_path, file_size)
                VALUES (?, ?, ?, ?)
            ''', (user_email, filename, file_path, file_size))
            
            file_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return True, file_id
        
        except Exception as e:
            return False, str(e)
    
    def get_user_files(self, user_email):
        """Get all files uploaded by user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, filename, file_size, upload_date
            FROM uploaded_files
            WHERE user_email = ?
            ORDER BY upload_date DESC
        ''', (user_email,))
        
        files = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return files
    
    def get_file_path(self, file_id):
        """Get file path by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT file_path FROM uploaded_files WHERE id = ?', (file_id,))
        result = cursor.fetchone()
        conn.close()
        
        return result['file_path'] if result else None
    
    # ========================================
    # ANALYSIS RESULTS MANAGEMENT
    # ========================================
    
    def save_analysis_results(self, user_email, file_id, results):
        """Save analysis results"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO analysis_results 
                (user_email, file_id, total_cases, asd_positive, asd_negative, 
                 accuracy_score, confidence_score, results_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_email,
                file_id,
                results.get('total_cases', 0),
                results.get('asd_positive', 0),
                results.get('asd_negative', 0),
                results.get('accuracy_score', 0.0),
                results.get('confidence_score', 0.0),
                json.dumps(results)
            ))
            
            result_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return True, result_id
        
        except Exception as e:
            return False, str(e)
    
    def get_user_results(self, user_email, limit=10):
        """Get analysis results for user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT ar.*, uf.filename
            FROM analysis_results ar
            LEFT JOIN uploaded_files uf ON ar.file_id = uf.id
            WHERE ar.user_email = ?
            ORDER BY ar.analyzed_at DESC
            LIMIT ?
        ''', (user_email, limit))
        
        results = []
        for row in cursor.fetchall():
            result = dict(row)
            # Parse JSON data
            if result['results_data']:
                result['results_data'] = json.loads(result['results_data'])
            results.append(result)
        
        conn.close()
        return results
    
    def get_latest_result(self, user_email):
        """Get most recent analysis result"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT ar.*, uf.filename
            FROM analysis_results ar
            LEFT JOIN uploaded_files uf ON ar.file_id = uf.id
            WHERE ar.user_email = ?
            ORDER BY ar.analyzed_at DESC
            LIMIT 1
        ''', (user_email,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            result_dict = dict(result)
            if result_dict['results_data']:
                result_dict['results_data'] = json.loads(result_dict['results_data'])
            return result_dict
        return None
    
    # ========================================
    # UTILITY FUNCTIONS
    # ========================================
    
    def get_user_stats(self, user_email):
        """Get user statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Count uploaded files
        cursor.execute('SELECT COUNT(*) as count FROM uploaded_files WHERE user_email = ?', (user_email,))
        file_count = cursor.fetchone()['count']
        
        # Count analyses
        cursor.execute('SELECT COUNT(*) as count FROM analysis_results WHERE user_email = ?', (user_email,))
        analysis_count = cursor.fetchone()['count']
        
        # Get total cases analyzed
        cursor.execute('SELECT SUM(total_cases) as total FROM analysis_results WHERE user_email = ?', (user_email,))
        total_cases = cursor.fetchone()['total'] or 0
        
        conn.close()
        
        return {
            'files_uploaded': file_count,
            'analyses_performed': analysis_count,
            'total_cases_analyzed': total_cases
        }
    
    def delete_old_files(self, days=30):
        """Delete files older than specified days"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM uploaded_files
            WHERE upload_date < datetime('now', '-' || ? || ' days')
        ''', (days,))
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted_count


# ========================================
# POSTGRESQL SUPPORT (FOR PRODUCTION)
# ========================================

class PostgreSQLDatabase:
    """PostgreSQL database handler for production deployment"""
    
    def __init__(self, database_url=None):
        """Initialize PostgreSQL connection"""
        try:
            import psycopg2
            from psycopg2.extras import RealDictCursor
            self.psycopg2 = psycopg2
            self.RealDictCursor = RealDictCursor
        except ImportError:
            raise ImportError("psycopg2 not installed. Run: pip install psycopg2-binary")
        
        self.database_url = database_url or os.environ.get('DATABASE_URL')
        if not self.database_url:
            raise ValueError("DATABASE_URL not provided")
        
        self.init_database()
    
    def get_connection(self):
        """Get PostgreSQL connection"""
        conn = self.psycopg2.connect(self.database_url, cursor_factory=self.RealDictCursor)
        return conn
    
    def init_database(self):
        """Create PostgreSQL tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                mobile VARCHAR(20) NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')
        
        # Create uploaded_files table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS uploaded_files (
                id SERIAL PRIMARY KEY,
                user_email VARCHAR(255) NOT NULL,
                filename VARCHAR(255) NOT NULL,
                file_path TEXT NOT NULL,
                file_size INTEGER,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_email) REFERENCES users (email)
            )
        ''')
        
        # Create analysis_results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analysis_results (
                id SERIAL PRIMARY KEY,
                user_email VARCHAR(255) NOT NULL,
                file_id INTEGER,
                total_cases INTEGER,
                asd_positive INTEGER,
                asd_negative INTEGER,
                accuracy_score REAL,
                confidence_score REAL,
                results_data TEXT,
                analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_email) REFERENCES users (email),
                FOREIGN KEY (file_id) REFERENCES uploaded_files (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print("✅ PostgreSQL database initialized successfully!")
    
    # ========================================
    # USER MANAGEMENT (PostgreSQL uses %s instead of ?)
    # ========================================
    
    def register_user(self, email, mobile, password):
        """Register a new user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Check if user already exists
            cursor.execute('SELECT email FROM users WHERE email = %s', (email,))
            if cursor.fetchone():
                conn.close()
                return False, "Email already registered"
            
            # Hash password and insert user
            password_hash = generate_password_hash(password)
            cursor.execute('''
                INSERT INTO users (email, mobile, password_hash)
                VALUES (%s, %s, %s)
            ''', (email, mobile, password_hash))
            
            conn.commit()
            conn.close()
            return True, "Registration successful"
        
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def login_user(self, email, password):
        """Authenticate user login"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
            user = cursor.fetchone()
            
            if not user:
                conn.close()
                return False, "Email not found"
            
            # Check password
            if not check_password_hash(user['password_hash'], password):
                conn.close()
                return False, "Incorrect password"
            
            # Update last login
            cursor.execute('''
                UPDATE users SET last_login = CURRENT_TIMESTAMP
                WHERE email = %s
            ''', (email,))
            conn.commit()
            conn.close()
            
            return True, {
                'email': user['email'],
                'mobile': user['mobile'],
                'created_at': user['created_at']
            }
        
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_user(self, email):
        """Get user details"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT email, mobile, created_at, last_login FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return dict(user)
        return None
    
    # ========================================
    # FILE MANAGEMENT
    # ========================================
    
    def save_uploaded_file(self, user_email, filename, file_path, file_size):
        """Save uploaded file information"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO uploaded_files (user_email, filename, file_path, file_size)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            ''', (user_email, filename, file_path, file_size))
            
            file_id = cursor.fetchone()['id']
            conn.commit()
            conn.close()
            
            return True, file_id
        
        except Exception as e:
            return False, str(e)
    
    def get_user_files(self, user_email):
        """Get all files uploaded by user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, filename, file_size, upload_date
            FROM uploaded_files
            WHERE user_email = %s
            ORDER BY upload_date DESC
        ''', (user_email,))
        
        files = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return files
    
    def get_file_path(self, file_id):
        """Get file path by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT file_path FROM uploaded_files WHERE id = %s', (file_id,))
        result = cursor.fetchone()
        conn.close()
        
        return result['file_path'] if result else None
    
    # ========================================
    # ANALYSIS RESULTS MANAGEMENT
    # ========================================
    
    def save_analysis_results(self, user_email, file_id, results):
        """Save analysis results"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO analysis_results 
                (user_email, file_id, total_cases, asd_positive, asd_negative, 
                 accuracy_score, confidence_score, results_data)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            ''', (
                user_email,
                file_id,
                results.get('total_cases', 0),
                results.get('asd_positive', 0),
                results.get('asd_negative', 0),
                results.get('accuracy_score', 0.0),
                results.get('confidence_score', 0.0),
                json.dumps(results)
            ))
            
            result_id = cursor.fetchone()['id']
            conn.commit()
            conn.close()
            
            return True, result_id
        
        except Exception as e:
            return False, str(e)
    
    def get_user_results(self, user_email, limit=10):
        """Get analysis results for user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT ar.*, uf.filename
            FROM analysis_results ar
            LEFT JOIN uploaded_files uf ON ar.file_id = uf.id
            WHERE ar.user_email = %s
            ORDER BY ar.analyzed_at DESC
            LIMIT %s
        ''', (user_email, limit))
        
        results = []
        for row in cursor.fetchall():
            result = dict(row)
            # Parse JSON data
            if result['results_data']:
                result['results_data'] = json.loads(result['results_data'])
            results.append(result)
        
        conn.close()
        return results
    
    def get_latest_result(self, user_email):
        """Get most recent analysis result"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT ar.*, uf.filename
            FROM analysis_results ar
            LEFT JOIN uploaded_files uf ON ar.file_id = uf.id
            WHERE ar.user_email = %s
            ORDER BY ar.analyzed_at DESC
            LIMIT 1
        ''', (user_email,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            result_dict = dict(result)
            if result_dict['results_data']:
                result_dict['results_data'] = json.loads(result_dict['results_data'])
            return result_dict
        return None
    
    # ========================================
    # UTILITY FUNCTIONS
    # ========================================
    
    def get_user_stats(self, user_email):
        """Get user statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Count uploaded files
        cursor.execute('SELECT COUNT(*) as count FROM uploaded_files WHERE user_email = %s', (user_email,))
        file_count = cursor.fetchone()['count']
        
        # Count analyses
        cursor.execute('SELECT COUNT(*) as count FROM analysis_results WHERE user_email = %s', (user_email,))
        analysis_count = cursor.fetchone()['count']
        
        # Get total cases analyzed
        cursor.execute('SELECT SUM(total_cases) as total FROM analysis_results WHERE user_email = %s', (user_email,))
        total_cases = cursor.fetchone()['total'] or 0
        
        conn.close()
        
        return {
            'files_uploaded': file_count,
            'analyses_performed': analysis_count,
            'total_cases_analyzed': total_cases
        }
    
    def delete_old_files(self, days=30):
        """Delete files older than specified days"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM uploaded_files
            WHERE upload_date < NOW() - INTERVAL '%s days'
        ''', (days,))
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted_count
