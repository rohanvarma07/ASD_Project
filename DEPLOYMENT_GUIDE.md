╔════════════════════════════════════════════════════════════════════════╗
║                                                                        ║
║           PRODUCTION DEPLOYMENT GUIDE                                  ║
║       ASD Detection System - Full Working Project                      ║
║                                                                        ║
╚════════════════════════════════════════════════════════════════════════╝

This guide covers multiple deployment options for your ASD Detection System.

═══════════════════════════════════════════════════════════════════════
═══════════════════════════════════════════════════════════════════════

OPTION 1: RENDER (RECOMMENDED - FREE & EASIEST)

═══════════════════════════════════════════════════════════════════════

🚨 **CRITICAL: YOU MUST USE POSTGRESQL ON RENDER!**

⚠️ SQLite will NOT work on Render (ephemeral file system - data lost on restart)
✅ PostgreSQL is FREE and required for production
📖 See RENDER_DATABASE_WARNING.md for full explanation

═══════════════════════════════════════════════════════════════════════

✅ Why Render?
- ✓ FREE tier available
- ✓ Automatic deployments from GitHub
- ✓ Easy setup (5 minutes)
- ✓ HTTPS included
- ✓ PostgreSQL database available (FREE)
- ✓ No credit card required for free tier

---

📋 STEP-BY-STEP DEPLOYMENT TO RENDER:

⚠️ **IMPORTANT: Create PostgreSQL database FIRST before web service!**

**STEP 0: CREATE POSTGRESQL DATABASE (REQUIRED)**
   
   1. Go to Render Dashboard: https://dashboard.render.com
   2. Click "New +" → "PostgreSQL"
   3. Configure database:
      - Name: asd-database
      - Database: asd_db
      - User: asd_user
      - Region: Oregon (US West) - remember this!
      - PostgreSQL Version: 15
      - Instance Type: **Free** ✅
   4. Click "Create Database"
   5. Wait 2-3 minutes for provisioning
   6. Once ready, click on database name
   7. Scroll to "Connections" section
   8. **COPY the "Internal Database URL"** (starts with postgresql://)
      - Example: `postgresql://asd_user:xxxxx@dpg-xxxxx-a/asd_db`
      - ⚠️ Use INTERNAL not EXTERNAL URL!
   9. Save this URL - you'll need it in Step 4

**STEP 1: SIGN UP FOR RENDER**
   - Go to: https://render.com
   - Click "Get Started for Free"
   - Sign up with GitHub account (recommended)

**STEP 2: CONNECT YOUR GITHUB REPOSITORY**
   - Once logged in, click "New +"
   - Select "Web Service"
   - Click "Connect GitHub"
   - Authorize Render to access your repositories
   - Find and select "rohanvarma07/ASD_Project"

**STEP 3: CONFIGURE YOUR WEB SERVICE**
   
   Fill in these settings:
   
   Name: asd-detection-system (or your preferred name)
   
   Region: Oregon (SAME as your database!)
   
   Branch: main
   
   Root Directory: (leave blank)
   
   Runtime: Python 3
   
   Build Command: pip install -r requirements.txt
   
   Start Command: gunicorn app:app
   
   Instance Type: Free
   
**STEP 4: ADD ENVIRONMENT VARIABLES (CRITICAL!)**
   
   Click "Advanced" and add these environment variables:
   
   **Key: DATABASE_URL** ⚠️ REQUIRED!
   **Value: [paste Internal Database URL from Step 0]**
   Example: postgresql://asd_user:xxxxx@dpg-xxxxx-a/asd_db
   
   Key: SECRET_KEY
   Value: (generate a random secret - see below)
   
   Key: DEBUG
   Value: False

**STEP 5: DEPLOY!**
   - Click "Create Web Service"
   - Wait 3-5 minutes for deployment
   - Watch build logs - should see:
     * "✅ Database initialized successfully!"
     * "✅ Connected to PostgreSQL database"
   - Your app will be live at: https://asd-detection-system.onrender.com

**STEP 6: TEST YOUR DEPLOYMENT**
   - Visit your Render URL
   - Register a new account
   - Login with: your-email@example.com / your-password
   - Test file upload with sample dataset
   - Verify results display
   
**STEP 7: VERIFY DATA PERSISTENCE (IMPORTANT!)**
   - Go to Render Dashboard → Your Web Service
   - Click "Manual Deploy" → "Deploy latest commit"
   - Wait for restart
   - Try logging in again
   - ✅ Your account should still exist!
   - ✅ This confirms PostgreSQL is working

---

🔐 GENERATE SECRET KEY:

Run this in your terminal:
```bash
python3 -c 'import secrets; print(secrets.token_hex(32))'
```

Copy the output and use it as your SECRET_KEY environment variable.

---

⚙️ AUTOMATIC DEPLOYMENTS:

Once set up, Render will automatically:
- Deploy when you push to GitHub
- Rebuild on every commit to main branch
- Show build logs
- Provide deployment notifications

═══════════════════════════════════════════════════════════════════════
═══════════════════════════════════════════════════════════════════════

OPTION 2: PYTHONANYWHERE (PYTHON-FOCUSED HOSTING)

═══════════════════════════════════════════════════════════════════════

✅ Why PythonAnywhere?
- ✓ FREE tier for students/beginners
- ✓ Python-focused hosting
- ✓ Easy Flask deployment
- ✓ Built-in database support
- ✓ No credit card required

---

📋 STEP-BY-STEP DEPLOYMENT TO PYTHONANYWHERE:

1. SIGN UP
   - Go to: https://www.pythonanywhere.com
   - Click "Pricing & signup"
   - Choose "Create a Beginner account" (FREE)
   - Complete registration

2. CLONE YOUR REPOSITORY
   - Open a Bash console (from Dashboard)
   - Run these commands:

```bash
cd ~
git clone https://github.com/rohanvarma07/ASD_Project.git
cd ASD_Project
```

3. CREATE VIRTUAL ENVIRONMENT
```bash
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. SET UP WEB APP
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Manual configuration"
   - Select Python 3.10
   
5. CONFIGURE WSGI FILE
   - Click on WSGI configuration file link
   - Replace content with:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/YOUR_USERNAME/ASD_Project'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['SECRET_KEY'] = 'your-secret-key-here'
os.environ['DEBUG'] = 'False'

# Import your Flask app
from app import app as application
```

   Replace YOUR_USERNAME with your PythonAnywhere username

6. SET VIRTUAL ENVIRONMENT PATH
   - In Web tab, find "Virtualenv" section
   - Enter: /home/YOUR_USERNAME/ASD_Project/venv

7. SET STATIC FILES
   - In "Static files" section, add:
   
   URL: /static/
   Directory: /home/YOUR_USERNAME/ASD_Project/static

8. RELOAD WEB APP
   - Click the green "Reload" button
   - Visit: https://YOUR_USERNAME.pythonanywhere.com

═══════════════════════════════════════════════════════════════════════
═══════════════════════════════════════════════════════════════════════

OPTION 3: HEROKU (POPULAR PLATFORM)

═══════════════════════════════════════════════════════════════════════

⚠️ Note: Heroku no longer offers free tier, but it's still popular.

📋 DEPLOYMENT STEPS:

1. Install Heroku CLI:
   - macOS: brew tap heroku/brew && brew install heroku
   - Or download from: https://devcenter.heroku.com/articles/heroku-cli

2. Login to Heroku:
```bash
heroku login
```

3. Create Heroku App:
```bash
cd /Users/rohanvarma/Desktop/ASD_FEND
heroku create asd-detection-system
```

4. Set Environment Variables:
```bash
heroku config:set SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
heroku config:set DEBUG=False
```

5. Deploy:
```bash
git push heroku main
```

6. Open App:
```bash
heroku open
```

═══════════════════════════════════════════════════════════════════════
═══════════════════════════════════════════════════════════════════════

OPTION 4: RAILWAY (MODERN PLATFORM)

═══════════════════════════════════════════════════════════════════════

✅ Why Railway?
- ✓ $5 free credit monthly
- ✓ GitHub integration
- ✓ Easy setup
- ✓ Modern interface

📋 DEPLOYMENT STEPS:

1. Sign up at: https://railway.app
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Choose "rohanvarma07/ASD_Project"
5. Add environment variables:
   - SECRET_KEY: (generate random key)
   - DEBUG: False
6. Railway will auto-deploy!

═══════════════════════════════════════════════════════════════════════
═══════════════════════════════════════════════════════════════════════

OPTION 5: VERCEL (WITH SERVERLESS FUNCTIONS)

═══════════════════════════════════════════════════════════════════════

Requires converting Flask to serverless functions.

1. Sign up at: https://vercel.com
2. Install Vercel CLI: npm i -g vercel
3. Deploy: vercel --prod

Note: This requires additional configuration for Flask.

═══════════════════════════════════════════════════════════════════════
═══════════════════════════════════════════════════════════════════════

PRE-DEPLOYMENT CHECKLIST

═══════════════════════════════════════════════════════════════════════

Before deploying, make sure:

✅ SECURITY
- [✓] SECRET_KEY uses environment variable
- [✓] DEBUG=False in production
- [✓] Gunicorn added to requirements.txt
- [ ] Change default admin password
- [ ] Add rate limiting (optional)
- [ ] Enable CORS if needed (optional)

✅ FILES PREPARED
- [✓] Procfile created
- [✓] runtime.txt created
- [✓] requirements.txt updated with gunicorn
- [✓] .gitignore configured
- [✓] All changes committed to GitHub

✅ TESTING
- [✓] App runs locally without errors
- [✓] All routes accessible
- [✓] File upload works
- [✓] Predictions work
- [✓] Results display correctly

✅ DOCUMENTATION
- [✓] README.md updated
- [✓] Deployment guide created
- [✓] Environment variables documented

═══════════════════════════════════════════════════════════════════════

COMMIT DEPLOYMENT FILES TO GITHUB

═══════════════════════════════════════════════════════════════════════

Run these commands:

```bash
cd /Users/rohanvarma/Desktop/ASD_FEND

# Add new deployment files
git add Procfile runtime.txt requirements.txt app.py

# Commit changes
git commit -m "Add production deployment configuration"

# Push to GitHub
git push origin main
```

═══════════════════════════════════════════════════════════════════════

RECOMMENDED DEPLOYMENT PATH (EASIEST)

═══════════════════════════════════════════════════════════════════════

For beginners, I recommend this order:

1. ⭐ RENDER (Easiest & Free)
   - Best for: Complete beginners
   - Setup time: 5 minutes
   - Free tier: Yes
   - Auto-deploy: Yes

2. 🐍 PYTHONANYWHERE (Python-focused)
   - Best for: Python developers
   - Setup time: 10 minutes
   - Free tier: Yes
   - Manual deployment: Yes

3. 🚂 RAILWAY (Modern)
   - Best for: Quick deployment
   - Setup time: 3 minutes
   - Free tier: Limited
   - Auto-deploy: Yes

═══════════════════════════════════════════════════════════════════════

POST-DEPLOYMENT TASKS

═══════════════════════════════════════════════════════════════════════

After successful deployment:

1. TEST THOROUGHLY
   - Visit all pages
   - Test registration
   - Test login
   - Upload sample dataset
   - Verify results

2. UPDATE README
   - Add live demo link
   - Add deployment badge
   - Update installation instructions

3. MONITOR
   - Check application logs
   - Monitor error rates
   - Track performance

4. SHARE
   - Add link to portfolio
   - Share on LinkedIn
   - Tweet about it
   - Post on Reddit

═══════════════════════════════════════════════════════════════════════

ENVIRONMENT VARIABLES NEEDED

═══════════════════════════════════════════════════════════════════════

For production deployment, set these:

Required:
- SECRET_KEY: Random secure string (32+ characters)
- DEBUG: False
- PYTHON_VERSION: 3.11.0

Optional:
- PORT: (Usually auto-set by platform)
- DATABASE_URL: (If using PostgreSQL)
- MAX_CONTENT_LENGTH: 10485760 (10MB)

Generate SECRET_KEY:
```bash
python3 -c 'import secrets; print(secrets.token_hex(32))'
```

═══════════════════════════════════════════════════════════════════════

TROUBLESHOOTING COMMON ISSUES

═══════════════════════════════════════════════════════════════════════

Issue: Build fails
Solution: Check requirements.txt for incompatible versions

Issue: App crashes on start
Solution: Check logs, ensure gunicorn is installed

Issue: Static files not loading
Solution: Configure static file paths in platform settings

Issue: Database connection errors
Solution: Check DATABASE_URL environment variable

Issue: Memory errors
Solution: Reduce pandas operations, optimize data processing

═══════════════════════════════════════════════════════════════════════

UPGRADING TO PAID TIER (OPTIONAL)

═══════════════════════════════════════════════════════════════════════

If you need more resources:

Render Pro: $7/month
- More RAM and CPU
- Always-on (no sleep)
- Custom domains
- Priority support

PythonAnywhere Hacker: $5/month
- More CPU time
- Custom domains
- SSH access
- More storage

Railway Pro: $5/month credit
- Pay for what you use
- More resources
- Better performance

═══════════════════════════════════════════════════════════════════════

ADDING CUSTOM DOMAIN (OPTIONAL)

═══════════════════════════════════════════════════════════════════════

1. Buy domain from Namecheap, GoDaddy, etc.
2. In your deployment platform:
   - Go to Settings
   - Find "Custom Domain" section
   - Add your domain
   - Copy DNS settings
3. Update DNS records at domain registrar
4. Wait for DNS propagation (up to 48 hours)

═══════════════════════════════════════════════════════════════════════

NEXT STEPS AFTER DEPLOYMENT

═══════════════════════════════════════════════════════════════════════

1. Set up monitoring:
   - Use Sentry for error tracking
   - Set up uptime monitoring (UptimeRobot)
   - Configure analytics (Google Analytics)

2. Add features:
   - Email notifications
   - Export to PDF
   - User dashboard improvements
   - Advanced analytics

3. Optimize:
   - Add caching
   - Optimize database queries
   - Compress images
   - Minify CSS/JS

4. Scale:
   - Add load balancing
   - Use CDN for static files
   - Implement database replication
   - Add API endpoints

═══════════════════════════════════════════════════════════════════════

SUPPORT & RESOURCES

═══════════════════════════════════════════════════════════════════════

Render Documentation:
https://render.com/docs

PythonAnywhere Help:
https://help.pythonanywhere.com

Flask Deployment Guide:
https://flask.palletsprojects.com/en/2.3.x/deploying/

Gunicorn Documentation:
https://docs.gunicorn.org

═══════════════════════════════════════════════════════════════════════

DEPLOYMENT SUCCESS CHECKLIST

═══════════════════════════════════════════════════════════════════════

After deployment, verify:

- [ ] App is accessible via public URL
- [ ] Home page loads correctly
- [ ] All CSS and JavaScript load
- [ ] Navigation works
- [ ] Registration works
- [ ] Login works
- [ ] File upload works
- [ ] Predictions generate correctly
- [ ] Results display properly
- [ ] Logout works
- [ ] Mobile view is responsive
- [ ] HTTPS is enabled
- [ ] No console errors
- [ ] No server errors in logs

═══════════════════════════════════════════════════════════════════════

CONGRATULATIONS! 🎉

═══════════════════════════════════════════════════════════════════════

Your ASD Detection System is ready for production deployment!

Choose your platform and follow the guide above.

For quickest deployment: Use RENDER
For Python-focused: Use PYTHONANYWHERE
For modern platform: Use RAILWAY

Good luck with your deployment! 🚀

═══════════════════════════════════════════════════════════════════════
