# 🚀 RENDER REDEPLOYMENT INSTRUCTIONS

## What Was Fixed

### Problem
- Render was showing old database or missing tables
- `screening_results` table was not being created in PostgreSQL
- Database wasn't being initialized automatically

### Solution
1. ✅ Added `screening_results` table to PostgreSQL initialization
2. ✅ Created `start.sh` script for automatic database setup
3. ✅ Updated `Procfile` to use startup script
4. ✅ Pushed all changes to GitHub

---

## 🔄 REDEPLOY ON RENDER (CRITICAL STEPS)

### Step 1: Manual Deploy (Recommended)
Go to your Render dashboard → Your web service → Click **"Manual Deploy"** → Select **"Clear build cache & deploy"**

This will:
- Pull the latest code from GitHub
- Rebuild with the new `start.sh` script
- Create the `screening_results` table in PostgreSQL
- Initialize all missing tables

### Step 2: Check Deployment Logs
Watch the logs during deployment. You should see:
```
🚀 Starting ASD Detection System...
✅ Using PostgreSQL database (production)
📊 Database will be auto-initialized on first connection
✅ PostgreSQL database initialized successfully!
🌐 Starting web server...
```

### Step 3: Verify Tables Are Created
After deployment completes, you can verify the database has all tables:

**Expected Tables:**
1. `users` - User accounts
2. `screening_results` - Individual screening data ✅ **NEW**
3. `uploaded_files` - CSV upload tracking
4. `analysis_results` - CSV analysis results

---

## ⚠️ IMPORTANT: If Still Having Issues

### Option A: Reset PostgreSQL Database (Clean Start)
If you still see old data:

1. Go to Render Dashboard → Your PostgreSQL database
2. Click **"Danger Zone"** → **"Delete Database"** ⚠️
3. Create a new PostgreSQL database
4. Update the `DATABASE_URL` environment variable in your web service
5. Redeploy the web service

### Option B: Manually Create Missing Table
Connect to PostgreSQL and run:

```sql
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
);
```

---

## ✅ Test After Deployment

1. **Register a new user** (or use existing)
2. **Login** to the dashboard
3. **Go to Screening page** and fill out the form
4. **Submit** - Should work without errors!
5. **Check Dashboard** - Should show screening history

---

## 🔧 Environment Variables (Double Check)

Make sure these are set in Render:

```bash
SECRET_KEY=64b7cd9b0ed6bda4bb81d94a0334482eb28a6488289324d423911341f8a1443a
DATABASE_URL=postgresql://user:password@host:5432/database  # Auto-set by Render
```

---

## 📝 What Changed in Code

### File: `database.py`
- Added `screening_results` table creation in PostgreSQL `init_database()` method
- Now creates all 4 tables: users, screening_results, uploaded_files, analysis_results

### File: `start.sh` (NEW)
- Automatically initializes database on startup
- Works for both SQLite (dev) and PostgreSQL (production)

### File: `Procfile`
- Changed from: `web: gunicorn app:app`
- Changed to: `web: bash start.sh`
- Now runs initialization before starting web server

---

## 🎯 Expected Result

After redeployment, your Render app should:
- ✅ Create all database tables automatically
- ✅ Allow screening form submissions
- ✅ Store screening results in PostgreSQL
- ✅ Display screening history in dashboard
- ✅ No more "table not found" or "old database" errors

---

**Ready to redeploy!** Go to Render → Manual Deploy → Clear build cache & deploy 🚀
