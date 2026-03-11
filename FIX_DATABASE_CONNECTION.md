# 🔧 FIX: PostgreSQL Connection Error on Render

## Error
```
could not translate host name "dpg-d6ntgjc50q8c73ajq9l0-a" to address: Name or service not known
```

## What This Means
- Your app is trying to connect to a PostgreSQL database that doesn't exist or was deleted
- The `DATABASE_URL` environment variable points to an old/invalid database

---

## ✅ SOLUTION: Update DATABASE_URL

### Step 1: Get the New DATABASE_URL from PostgreSQL

1. Go to **Render Dashboard**
2. Click on your **PostgreSQL database** (in the sidebar or services list)
3. Scroll down to **Connection** section
4. Find **Internal Database URL** (recommended) or **External Database URL**
5. **Copy** the full URL - it looks like:
   ```
   postgresql://username:password@hostname:5432/database_name
   ```

### Step 2: Update Environment Variable in Web Service

1. Go to your **Web Service** (the Flask app)
2. Click on **Environment** tab (left sidebar)
3. Find the `DATABASE_URL` variable
4. Click **Edit**
5. **Paste** the new DATABASE_URL you copied
6. Click **Save Changes**

### Step 3: Redeploy

After saving the environment variable:
- Render will **automatically redeploy** your service
- OR click **"Manual Deploy"** → **"Deploy latest commit"**

---

## 🆕 ALTERNATIVE: Create Fresh PostgreSQL Database

If you don't have a PostgreSQL database or want to start fresh:

### 1. Create New PostgreSQL Database

1. Render Dashboard → **New** → **PostgreSQL**
2. Fill in details:
   - **Name**: `asd-database` (or any name)
   - **Database**: `asd_db`
   - **User**: `asd_user`
   - **Region**: Same as your web service
   - **PostgreSQL Version**: 15 or 16
3. Click **Create Database**
4. Wait 2-3 minutes for creation

### 2. Get the Connection String

After database is created:
1. Click on the database
2. Scroll to **Connections**
3. Copy **Internal Database URL**

### 3. Link to Web Service

1. Go to your **Web Service**
2. Click **Environment** tab
3. Add or update `DATABASE_URL`:
   - **Key**: `DATABASE_URL`
   - **Value**: (paste the Internal Database URL)
4. Click **Save Changes**

### 4. Redeploy

The service will auto-redeploy. Watch logs for:
```
✅ Using PostgreSQL database (production)
✅ PostgreSQL database initialized successfully!
```

---

## 🔍 VERIFY DATABASE CONNECTION

After deployment, check the logs for these messages:

### ✅ Success:
```
✅ Connected to PostgreSQL database
✅ PostgreSQL database initialized successfully!
```

### ❌ Still Error:
```
could not translate host name...
```
→ Double-check DATABASE_URL is correct
→ Make sure database is in "Available" status (not "Creating")

---

## 📝 IMPORTANT NOTES

### Database URL Format
```
postgresql://user:password@hostname.render.com:5432/database_name
```

### Internal vs External URL
- **Internal URL**: Use this (faster, secure, free)
  - Format: `dpg-xxxxx-a.oregon-postgres.render.com`
- **External URL**: Only if connecting from outside Render
  - Format: `dpg-xxxxx-a.oregon-postgres.render.com` (public)

### Common Mistakes
- ❌ Using old DATABASE_URL after deleting database
- ❌ Using External URL when Internal URL is available
- ❌ Typo in DATABASE_URL (missing characters)
- ❌ Database still in "Creating" status

---

## 🎯 QUICK FIX CHECKLIST

- [ ] PostgreSQL database is created and shows "Available" status
- [ ] Copied the correct **Internal Database URL**
- [ ] Pasted it into web service **Environment** → `DATABASE_URL`
- [ ] Saved the environment variable
- [ ] Redeployed the web service
- [ ] Checked logs for "✅ Connected to PostgreSQL database"

---

## 🆘 STILL NOT WORKING?

### Option 1: Use SQLite (Temporary Development)
Remove the `DATABASE_URL` environment variable completely:
- Web Service → Environment → Delete `DATABASE_URL`
- Redeploy
- App will use SQLite (works but data will be lost on restart)

### Option 2: Check Database Status
- Render Dashboard → PostgreSQL database
- Status should be **"Available"** (green)
- If "Suspended" or "Creating", wait or recreate

### Option 3: Fresh Start
1. Delete old PostgreSQL database
2. Delete `DATABASE_URL` environment variable
3. Create new PostgreSQL database
4. Add new `DATABASE_URL`
5. Redeploy

---

**Most Common Solution:** Just update the DATABASE_URL with the correct Internal Database URL from your PostgreSQL service! 🎯
