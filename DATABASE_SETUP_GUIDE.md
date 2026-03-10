╔════════════════════════════════════════════════════════════════════════╗
║                                                                        ║
║           DATABASE SETUP GUIDE                                         ║
║       Persistent Storage for Login & CSV Files                         ║
║                                                                        ║
╚════════════════════════════════════════════════════════════════════════╝

Your ASD Detection System now includes a complete database backend!

═══════════════════════════════════════════════════════════════════════
WHAT'S NEW?
═══════════════════════════════════════════════════════════════════════

✅ **Persistent Data Storage**
   - User registrations are saved permanently
   - Login details stored securely (hashed passwords)
   - Uploaded CSV files tracked in database
   - Analysis results saved with history

✅ **Database Options**
   - SQLite (automatic, no setup) - Development
   - PostgreSQL (production-ready) - Deployment

✅ **Features**
   - User management (register, login, profile)
   - File upload tracking
   - Analysis history
   - User statistics

═══════════════════════════════════════════════════════════════════════
DATABASE STRUCTURE
═══════════════════════════════════════════════════════════════════════

**TABLES:**

1. **users**
   - id (Primary Key)
   - email (Unique)
   - mobile
   - password_hash (Encrypted)
   - created_at
   - last_login

2. **uploaded_files**
   - id (Primary Key)
   - user_email (Foreign Key → users.email)
   - filename
   - file_path
   - file_size
   - upload_date

3. **analysis_results**
   - id (Primary Key)
   - user_email (Foreign Key → users.email)
   - file_id (Foreign Key → uploaded_files.id)
   - total_cases
   - asd_positive
   - asd_negative
   - accuracy_score
   - confidence_score
   - results_data (JSON)
   - analyzed_at

═══════════════════════════════════════════════════════════════════════
OPTION 1: SQLITE (DEVELOPMENT) - AUTOMATIC
═══════════════════════════════════════════════════════════════════════

✅ **No Setup Required!**

SQLite is automatically used when you run locally.

**How it works:**
- Database file: `asd_database.db` (created automatically)
- No installation needed
- Perfect for development and testing
- Single file database

**Location:**
```
/Users/rohanvarma/Desktop/ASD_FEND/asd_database.db
```

**To view database:**
```bash
# Install SQLite browser (optional)
brew install sqlite

# View database
sqlite3 asd_database.db

# SQL commands:
.tables                    # Show all tables
SELECT * FROM users;       # View users
SELECT * FROM uploaded_files;  # View files
.quit                      # Exit
```

═══════════════════════════════════════════════════════════════════════
OPTION 2: POSTGRESQL (PRODUCTION)
═══════════════════════════════════════════════════════════════════════

For production deployment (Render, Heroku, etc.)

**AUTOMATIC SETUP ON RENDER:**

1. Go to Render Dashboard
2. Click "New +" → "PostgreSQL"
3. Name: asd-database
4. Database: asd_db
5. User: asd_user
6. Region: Same as your web service
7. Instance Type: Free
8. Click "Create Database"

9. Copy the "Internal Database URL"

10. Go to your Web Service → Environment
11. Add environment variable:
    ```
    Key: DATABASE_URL
    Value: [paste the Internal Database URL]
    ```

12. Save and redeploy

**That's it! Your app will automatically:**
- Detect PostgreSQL
- Create tables
- Use PostgreSQL instead of SQLite

═══════════════════════════════════════════════════════════════════════
OPTION 3: LOCAL POSTGRESQL (ADVANCED)
═══════════════════════════════════════════════════════════════════════

If you want to test PostgreSQL locally:

**1. Install PostgreSQL:**
```bash
brew install postgresql@14
brew services start postgresql@14
```

**2. Create Database:**
```bash
createdb asd_database
```

**3. Set Environment Variable:**
```bash
export DATABASE_URL="postgresql://localhost/asd_database"
```

**4. Run Your App:**
```bash
python app.py
```

The app will automatically use PostgreSQL!

═══════════════════════════════════════════════════════════════════════
HOW TO USE THE DATABASE
═══════════════════════════════════════════════════════════════════════

**1. REGISTER NEW USER:**
   - Go to http://localhost:5001/register
   - Fill in email, mobile, password
   - User is saved to database permanently

**2. LOGIN:**
   - Go to http://localhost:5001/login
   - Enter email and password
   - Session created, user data loaded from database

**3. UPLOAD CSV:**
   - Login first
   - Go to Upload page
   - Select CSV file
   - File info saved to database
   - File path stored for later access

**4. VIEW RESULTS:**
   - Analysis results saved to database
   - View history of all analyses
   - Results persist across sessions

═══════════════════════════════════════════════════════════════════════
DATABASE API REFERENCE
═══════════════════════════════════════════════════════════════════════

**Import:**
```python
from database import Database

db = Database()  # Uses SQLite by default
```

**User Management:**
```python
# Register user
success, message = db.register_user(email, mobile, password)

# Login user
success, user_data = db.login_user(email, password)

# Get user info
user = db.get_user(email)
```

**File Management:**
```python
# Save uploaded file
success, file_id = db.save_uploaded_file(email, filename, filepath, size)

# Get user's files
files = db.get_user_files(email)

# Get file path
path = db.get_file_path(file_id)
```

**Results Management:**
```python
# Save analysis results
success, result_id = db.save_analysis_results(email, file_id, results)

# Get user's results
results = db.get_user_results(email, limit=10)

# Get latest result
latest = db.get_latest_result(email)
```

**Statistics:**
```python
# Get user stats
stats = db.get_user_stats(email)
# Returns: {
#   'files_uploaded': 5,
#   'analyses_performed': 3,
#   'total_cases_analyzed': 150
# }
```

═══════════════════════════════════════════════════════════════════════
TESTING THE DATABASE
═══════════════════════════════════════════════════════════════════════

**1. Start the server:**
```bash
cd /Users/rohanvarma/Desktop/ASD_FEND
python app.py
```

**2. Test Registration:**
```bash
# Register a new user via browser
http://localhost:5001/register

# Fill in:
Email: test@example.com
Mobile: 9876543210
Password: test123
```

**3. Check Database:**
```bash
# View SQLite database
sqlite3 asd_database.db
SELECT * FROM users;
```

**4. Test Login:**
```bash
# Login with registered user
http://localhost:5001/login

Email: test@example.com
Password: test123
```

**5. Test File Upload:**
```bash
# Upload sample CSV
http://localhost:5001/upload

# Select: sample_autism_dataset.csv
```

**6. View Results:**
```bash
# Check results page
http://localhost:5001/results
```

═══════════════════════════════════════════════════════════════════════
MIGRATING TO PRODUCTION
═══════════════════════════════════════════════════════════════════════

**When deploying to production:**

1. ✅ SQLite database (asd_database.db) stays on your local machine
2. ✅ Production uses PostgreSQL (set DATABASE_URL)
3. ✅ All user data starts fresh on production
4. ✅ No migration needed - tables created automatically

**Steps:**
1. Deploy to Render/Heroku
2. Add PostgreSQL database
3. Set DATABASE_URL environment variable
4. App automatically switches to PostgreSQL

═══════════════════════════════════════════════════════════════════════
BACKUP & RESTORE
═══════════════════════════════════════════════════════════════════════

**Backup SQLite Database:**
```bash
# Create backup
cp asd_database.db asd_database_backup_$(date +%Y%m%d).db

# Or use SQLite dump
sqlite3 asd_database.db .dump > backup.sql
```

**Restore SQLite Database:**
```bash
# Restore from backup
cp asd_database_backup_20260310.db asd_database.db

# Or from SQL dump
sqlite3 asd_database.db < backup.sql
```

**Backup PostgreSQL:**
```bash
pg_dump $DATABASE_URL > backup.sql
```

**Restore PostgreSQL:**
```bash
psql $DATABASE_URL < backup.sql
```

═══════════════════════════════════════════════════════════════════════
SECURITY FEATURES
═══════════════════════════════════════════════════════════════════════

✅ **Password Hashing:**
   - Passwords never stored in plain text
   - Uses Werkzeug's generate_password_hash
   - SHA-256 encryption

✅ **SQL Injection Protection:**
   - Parameterized queries
   - No raw SQL with user input

✅ **Session Security:**
   - Secret key for session encryption
   - Secure session cookies

✅ **File Upload Security:**
   - Filename sanitization
   - File type validation
   - Size limits

═══════════════════════════════════════════════════════════════════════
TROUBLESHOOTING
═══════════════════════════════════════════════════════════════════════

**Issue: Database file not found**
Solution: The database is created automatically on first run. Just start the app.

**Issue: PostgreSQL connection error**
Solution: 
- Check DATABASE_URL is correct
- Ensure PostgreSQL is running
- Verify network access

**Issue: Table doesn't exist**
Solution: Delete asd_database.db and restart. Tables are auto-created.

**Issue: Can't login after restart**
Solution: If using SQLite, check that asd_database.db exists in project folder.

**Issue: Users not persisting**
Solution: Make sure you're not deleting asd_database.db file.

═══════════════════════════════════════════════════════════════════════
USEFUL SQL QUERIES
═══════════════════════════════════════════════════════════════════════

```sql
-- View all users
SELECT email, mobile, created_at, last_login FROM users;

-- Count users
SELECT COUNT(*) FROM users;

-- View recent uploads
SELECT u.email, uf.filename, uf.upload_date 
FROM uploaded_files uf
JOIN users u ON uf.user_email = u.email
ORDER BY uf.upload_date DESC
LIMIT 10;

-- View analysis statistics
SELECT 
    user_email,
    COUNT(*) as total_analyses,
    SUM(total_cases) as total_cases_analyzed,
    AVG(accuracy_score) as avg_accuracy
FROM analysis_results
GROUP BY user_email;

-- Find user by email
SELECT * FROM users WHERE email = 'admin@example.com';

-- Delete old files (older than 30 days)
DELETE FROM uploaded_files 
WHERE upload_date < datetime('now', '-30 days');
```

═══════════════════════════════════════════════════════════════════════
PRODUCTION BEST PRACTICES
═══════════════════════════════════════════════════════════════════════

1. ✅ **Use PostgreSQL in production**
   - More reliable than SQLite
   - Better concurrent access
   - Scalable

2. ✅ **Regular Backups**
   - Daily database backups
   - Store backups securely
   - Test restore process

3. ✅ **Monitor Database Size**
   - Clean old files periodically
   - Archive old results
   - Set storage limits

4. ✅ **Environment Variables**
   - Never commit DATABASE_URL
   - Use .env for local testing
   - Set via platform settings

5. ✅ **Database Indexing**
   - Email columns indexed automatically
   - Add indexes for frequently queried fields

═══════════════════════════════════════════════════════════════════════
NEXT STEPS
═══════════════════════════════════════════════════════════════════════

1. **Test Locally:**
   ```bash
   python app.py
   ```
   - Register a user
   - Upload a CSV
   - Check database file created

2. **Deploy to Production:**
   - Follow DEPLOYMENT_GUIDE.md
   - Add PostgreSQL database on Render
   - Set DATABASE_URL environment variable

3. **Verify:**
   - Test registration on live site
   - Upload CSV file
   - Confirm data persists after restart

═══════════════════════════════════════════════════════════════════════
SUMMARY
═══════════════════════════════════════════════════════════════════════

✅ **Local Development:**
   - SQLite used automatically
   - File: asd_database.db
   - No setup required

✅ **Production:**
   - Add PostgreSQL on Render
   - Set DATABASE_URL
   - Automatic table creation

✅ **Data Stored:**
   - User accounts (email, password)
   - Uploaded CSV files (filename, path, size)
   - Analysis results (predictions, stats)
   - User activity history

✅ **Ready to Use:**
   - Start app.py
   - Register users
   - Upload files
   - Data persists forever!

═══════════════════════════════════════════════════════════════════════

🎉 **Your database backend is ready!**

Questions? Check the troubleshooting section above.

═══════════════════════════════════════════════════════════════════════
