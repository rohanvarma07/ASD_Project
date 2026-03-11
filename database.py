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
        """Get database connection with timeout and WAL mode"""
        conn = sqlite3.connect(self.db_path, timeout=30.0)  # 30 second timeout
        conn.row_factory = sqlite3.Row  # Access columns by name
        # Enable WAL mode for better concurrency
        conn.execute('PRAGMA journal_mode=WAL')
        return conn
    
    def __enter__(self):
        """Context manager entry"""
        self.conn = self.get_connection()
        return self.conn
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensures connection is closed"""
        if hasattr(self, 'conn') and self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.conn.close()
        return False
    
    def init_database(self):
        """Create database tables if they don't exist"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                mobile TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')
        
        # Check if username column exists (for existing databases)
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        if 'username' not in columns:
            cursor.execute('ALTER TABLE users ADD COLUMN username TEXT DEFAULT "User"')
            print("✅ Added username column to existing users table")
        
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
        
        # Create screening_results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS screening_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_email TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                ethnicity TEXT NOT NULL,
                jaundice TEXT NOT NULL,
                family_history TEXT NOT NULL,
                exam_result TEXT NOT NULL,
                q1_routine TEXT NOT NULL,
                q2_repeats TEXT NOT NULL,
                q3_focus TEXT NOT NULL,
                q4_empathy TEXT NOT NULL,
                q5_changes TEXT NOT NULL,
                q6_socializing TEXT NOT NULL,
                q7_friends TEXT NOT NULL,
                q8_movements TEXT NOT NULL,
                q9_eye_contact TEXT NOT NULL,
                q10_expressions TEXT NOT NULL,
                total_score INTEGER,
                risk_level TEXT,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_email) REFERENCES users (email)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print("✅ Database initialized successfully!")
    
    # ========================================
    # USER MANAGEMENT
    # ========================================
    
    def register_user(self, email, mobile, password, username=None):
        """Register a new user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Check if user already exists
            cursor.execute('SELECT email FROM users WHERE email = ?', (email,))
            if cursor.fetchone():
                conn.close()
                return False, "Email already registered"
            
            # Use email prefix as username if not provided
            if not username:
                username = email.split('@')[0]
            
            # Hash password and insert user
            password_hash = generate_password_hash(password)
            cursor.execute('''
                INSERT INTO users (username, email, mobile, password_hash)
                VALUES (?, ?, ?, ?)
            ''', (username, email, mobile, password_hash))
            
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
            
            # Get username, default to email prefix if not set
            username = user['username'] if user['username'] else email.split('@')[0]
            
            return True, {
                'username': username,
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
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, filename, file_size, upload_date
                FROM uploaded_files
                WHERE user_email = ?
                ORDER BY upload_date DESC
            ''', (user_email,))
            
            files = [dict(row) for row in cursor.fetchall()]
            return files
        finally:
            if conn:
                conn.close()
    
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
        conn = None
        try:
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
            
            if result:
                result_dict = dict(result)
                if result_dict['results_data']:
                    result_dict['results_data'] = json.loads(result_dict['results_data'])
                return result_dict
            return None
        finally:
            if conn:
                conn.close()
    
    # ========================================
    # UTILITY FUNCTIONS
    # ========================================
    
    def get_user_stats(self, user_email):
        """Get user statistics"""
        conn = None
        try:
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
            
            return {
                'files_uploaded': file_count,
                'analyses_performed': analysis_count,
                'total_cases_analyzed': total_cases
            }
        finally:
            if conn:
                conn.close()
    
    def save_screening_result(self, user_email, screening_data):
        """Save screening result with retry logic"""
        import time
        
        max_retries = 3
        retry_delay = 0.1  # 100ms
        
        for attempt in range(max_retries):
            try:
                conn = self.get_connection()
                cursor = conn.cursor()
                
                # Calculate total score (count 'yes' answers)
                total_score = sum([
                    1 for q in ['q1_routine', 'q2_repeats', 'q3_focus', 'q4_empathy', 'q5_changes',
                               'q6_socializing', 'q7_friends', 'q8_movements', 'q9_eye_contact', 'q10_expressions']
                    if screening_data.get(q, '').lower() == 'yes'
                ])
                
                # Determine risk level
                if total_score >= 7:
                    risk_level = 'High'
                elif total_score >= 4:
                    risk_level = 'Medium'
                else:
                    risk_level = 'Low'
                
                # Check if user already has a screening result
                cursor.execute('SELECT id FROM screening_results WHERE user_email = ?', (user_email,))
                existing = cursor.fetchone()
                
                if existing:
                    # Update existing screening
                    cursor.execute('''
                        UPDATE screening_results SET
                            age = ?, gender = ?, ethnicity = ?, jaundice = ?, family_history = ?,
                            exam_result = ?, q1_routine = ?, q2_repeats = ?, q3_focus = ?,
                            q4_empathy = ?, q5_changes = ?, q6_socializing = ?, q7_friends = ?,
                            q8_movements = ?, q9_eye_contact = ?, q10_expressions = ?,
                            total_score = ?, risk_level = ?, completed_at = CURRENT_TIMESTAMP
                        WHERE user_email = ?
                    ''', (
                        screening_data['age'], screening_data['gender'], screening_data['ethnicity'],
                        screening_data['jaundice'], screening_data['family_history'], screening_data['exam_result'],
                        screening_data['q1_routine'], screening_data['q2_repeats'], screening_data['q3_focus'],
                        screening_data['q4_empathy'], screening_data['q5_changes'], screening_data['q6_socializing'],
                        screening_data['q7_friends'], screening_data['q8_movements'], screening_data['q9_eye_contact'],
                        screening_data['q10_expressions'], total_score, risk_level, user_email
                    ))
                else:
                    # Insert new screening
                    cursor.execute('''
                        INSERT INTO screening_results (
                            user_email, age, gender, ethnicity, jaundice, family_history, exam_result,
                            q1_routine, q2_repeats, q3_focus, q4_empathy, q5_changes, q6_socializing,
                            q7_friends, q8_movements, q9_eye_contact, q10_expressions, total_score, risk_level
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        user_email, screening_data['age'], screening_data['gender'], screening_data['ethnicity'],
                        screening_data['jaundice'], screening_data['family_history'], screening_data['exam_result'],
                        screening_data['q1_routine'], screening_data['q2_repeats'], screening_data['q3_focus'],
                        screening_data['q4_empathy'], screening_data['q5_changes'], screening_data['q6_socializing'],
                        screening_data['q7_friends'], screening_data['q8_movements'], screening_data['q9_eye_contact'],
                        screening_data['q10_expressions'], total_score, risk_level
                    ))
                
                conn.commit()
                conn.close()
                
                return True, {'total_score': total_score, 'risk_level': risk_level}
            
            except sqlite3.OperationalError as e:
                if 'locked' in str(e).lower() and attempt < max_retries - 1:
                    # Database is locked, retry after a short delay
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                    continue
                else:
                    # Max retries reached or different error
                    return False, str(e)
            except Exception as e:
                try:
                    conn.close()
                except:
                    pass
                return False, str(e)
        
        return False, "Database is busy. Please try again."
    
    def get_screening_result(self, user_email):
        """Get user's screening result"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM screening_results WHERE user_email = ?
            ''', (user_email,))
            
            result = cursor.fetchone()
            
            if result:
                return dict(result)
            return None
        finally:
            if conn:
                conn.close()
    
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
                username VARCHAR(100) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                mobile VARCHAR(20) NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')
        
        # Add username column if it doesn't exist (for existing databases)
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='users' AND column_name='username'
        """)
        if not cursor.fetchone():
            cursor.execute('ALTER TABLE users ADD COLUMN username VARCHAR(100) DEFAULT %s', ('User',))
            print("✅ Added username column to PostgreSQL users table")
        
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
        
        # Create screening_results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS screening_results (
                id SERIAL PRIMARY KEY,
                user_email VARCHAR(255) NOT NULL,
                age INTEGER,
                gender VARCHAR(10),
                ethnicity VARCHAR(50),
                jaundice VARCHAR(3),
                family_asd VARCHAR(3),
                q1_score INTEGER,
                q2_score INTEGER,
                q3_score INTEGER,
                q4_score INTEGER,
                q5_score INTEGER,
                q6_score INTEGER,
                q7_score INTEGER,
                q8_score INTEGER,
                q9_score INTEGER,
                q10_score INTEGER,
                total_score INTEGER,
                prediction VARCHAR(50),
                confidence REAL,
                risk_level VARCHAR(20),
                screening_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
    
    def register_user(self, email, mobile, password, username=None):
        """Register a new user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Check if user already exists
            cursor.execute('SELECT email FROM users WHERE email = %s', (email,))
            if cursor.fetchone():
                conn.close()
                return False, "Email already registered"
            
            # Use email prefix as username if not provided
            if not username:
                username = email.split('@')[0]
            
            # Hash password and insert user
            password_hash = generate_password_hash(password)
            cursor.execute('''
                INSERT INTO users (username, email, mobile, password_hash)
                VALUES (%s, %s, %s, %s)
            ''', (username, email, mobile, password_hash))
            
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
            
            # Get username, default to email prefix if not set
            username = user.get('username') if user.get('username') else email.split('@')[0]
            
            return True, {
                'username': username,
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
