# PythonAnywhere Deployment Guide - Staff Attendance System

## 📋 Prerequisites

- ✅ PythonAnywhere account (free or paid)
- ✅ GitHub repository with your code
- ✅ SQLite database (already configured)

## 🚀 Step-by-Step Deployment

### Step 1: Create PythonAnywhere Account

1. Go to https://www.pythonanywhere.com/
2. Sign up for a free account (or login if you have one)
3. Your username will be part of your URL: `https://yourusername.pythonanywhere.com`

### Step 2: Open a Bash Console

1. From PythonAnywhere dashboard, click **"Consoles"**
2. Click **"Bash"** to start a new bash console

### Step 3: Clone Your Repository

In the bash console, run:

```bash
# Clone your repository
git clone https://github.com/Emmydantoch/staff_attendance.git

# Navigate to the project directory
cd staff_attendance
```

### Step 4: Create Virtual Environment

```bash
# Create a virtual environment
mkvirtualenv --python=/usr/bin/python3.10 staff_attendance_env

# The virtual environment will be automatically activated
# You should see (staff_attendance_env) in your prompt
```

### Step 5: Install Dependencies

```bash
# Make sure you're in the project directory
cd ~/staff_attendance

# Install all requirements
pip install -r requirements.txt
```

### Step 6: Setup Database

```bash
# Run migrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser
# Follow the prompts to create your admin account

# Create staff profiles for all users
python manage.py create_staff_profiles

# Collect static files
python manage.py collectstatic --noinput
```

### Step 7: Configure Web App

1. Go to **"Web"** tab in PythonAnywhere dashboard
2. Click **"Add a new web app"**
3. Choose **"Manual configuration"** (NOT Django)
4. Select **Python 3.10**

### Step 8: Configure WSGI File

1. In the **Web** tab, find the **"Code"** section
2. Click on the **WSGI configuration file** link (something like `/var/www/yourusername_pythonanywhere_com_wsgi.py`)
3. **Delete all content** and replace with:

```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/yourusername/staff_attendance'  # ⚠️ REPLACE 'yourusername' with your actual username
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variable to tell Django where your settings are
os.environ['DJANGO_SETTINGS_MODULE'] = 'staff_attendance.settings'

# Activate your virtual environment
activate_this = '/home/yourusername/.virtualenvs/staff_attendance_env/bin/activate_this.py'  # ⚠️ REPLACE 'yourusername'
exec(open(activate_this).read(), {'__file__': activate_this})

# Import Django's WSGI handler
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**⚠️ IMPORTANT:** Replace `yourusername` with your actual PythonAnywhere username in BOTH places!

4. Click **"Save"** (top right)

### Step 9: Configure Virtual Environment

1. Still in the **Web** tab, find **"Virtualenv"** section
2. Enter the path to your virtual environment:
   ```
   /home/yourusername/.virtualenvs/staff_attendance_env
   ```
   (Replace `yourusername` with your actual username)
3. Click the checkmark to save

### Step 10: Configure Static Files

In the **Web** tab, scroll to **"Static files"** section:

1. Click **"Enter URL"** and add:
   - **URL:** `/static/`
   - **Directory:** `/home/yourusername/staff_attendance/staticfiles`
   
2. Click **"Enter URL"** again and add:
   - **URL:** `/media/`
   - **Directory:** `/home/yourusername/staff_attendance/media`

(Replace `yourusername` with your actual username)

### Step 11: Reload Web App

1. Scroll to the top of the **Web** tab
2. Click the big green **"Reload yourusername.pythonanywhere.com"** button
3. Wait for it to finish reloading

### Step 12: Test Your Site

1. Click on the link at the top: `https://yourusername.pythonanywhere.com`
2. Your site should now be live! 🎉

## 📊 Your SQLite Database

Your SQLite database (`db.sqlite3`) will be located at:
```
/home/yourusername/staff_attendance/db.sqlite3
```

### Uploading Your Local Database (Optional)

If you want to use your local database with all existing data:

1. In PythonAnywhere, go to **"Files"** tab
2. Navigate to `/home/yourusername/staff_attendance/`
3. Click **"Upload a file"**
4. Upload your local `db.sqlite3` file
5. Reload your web app

## 🔧 Common Tasks

### Update Your Code

When you push changes to GitHub:

```bash
# In PythonAnywhere bash console
cd ~/staff_attendance
git pull origin main

# If you changed models
python manage.py migrate

# If you changed static files
python manage.py collectstatic --noinput

# Reload web app from Web tab
```

### View Logs

If something goes wrong:

1. Go to **Web** tab
2. Scroll to **"Log files"** section
3. Check:
   - **Error log** - for Python errors
   - **Server log** - for server issues
   - **Access log** - for request logs

### Run Management Commands

```bash
# Open bash console
cd ~/staff_attendance
workon staff_attendance_env

# Run any command
python manage.py create_staff_profiles
python manage.py generate_barcodes
python manage.py createsuperuser
```

### Backup Your Database

```bash
# In bash console
cd ~/staff_attendance
cp db.sqlite3 db.sqlite3.backup_$(date +%Y%m%d)
```

Or download it:
1. Go to **Files** tab
2. Navigate to `/home/yourusername/staff_attendance/`
3. Click on `db.sqlite3`
4. Click **"Download"**

## 🎯 Important URLs

After deployment, your URLs will be:

- **Main Site:** `https://yourusername.pythonanywhere.com/`
- **Admin Panel:** `https://yourusername.pythonanywhere.com/admin/`
- **Sign In/Out:** `https://yourusername.pythonanywhere.com/sign-in-out/`
- **Barcode Scanner:** `https://yourusername.pythonanywhere.com/barcode-scan/`
- **My QR Code:** `https://yourusername.pythonanywhere.com/my-barcode/`

## ⚠️ Important Notes

1. **Free Account Limitations:**
   - Your app will sleep after 3 months of inactivity
   - Limited CPU time per day
   - One web app only
   - Must reload app every 3 months

2. **Database Backups:**
   - SQLite database is a single file - easy to backup!
   - Download regularly from Files tab
   - Or use bash console to create backups

3. **HTTPS:**
   - PythonAnywhere provides free HTTPS automatically
   - Your QR code scanner will work perfectly with camera access

4. **Static Files:**
   - Already configured with WhiteNoise
   - Run `collectstatic` after any static file changes

## 🔐 Security Checklist

Before going live, consider:

1. **Change SECRET_KEY** in settings.py (generate a new one)
2. **Set DEBUG = False** for production (use environment variable)
3. **Review ALLOWED_HOSTS** (already configured)
4. **Create strong admin password**
5. **Regular database backups**

## 📱 Testing Features

After deployment, test:

- ✅ User registration
- ✅ Login/logout
- ✅ Sign in/out functionality
- ✅ QR code generation (visit /my-barcode/)
- ✅ Barcode scanner (visit /barcode-scan/)
- ✅ Camera access for QR scanning
- ✅ Admin panel (/admin/)
- ✅ Leave requests
- ✅ Dashboard

## 🆘 Troubleshooting

### "ImportError" or "ModuleNotFoundError"
```bash
workon staff_attendance_env
pip install -r requirements.txt
```

### Static files not loading
```bash
python manage.py collectstatic --noinput
# Then reload web app
```

### Database errors
```bash
python manage.py migrate
python manage.py create_staff_profiles
```

### 502 Bad Gateway
- Check error log in Web tab
- Make sure WSGI file has correct paths
- Make sure virtual environment is configured

## 🎉 Success!

Your staff attendance system with barcode scanning is now live on PythonAnywhere with SQLite database!

All your existing data (users, staff profiles, barcodes) will work perfectly.

**Your site:** `https://yourusername.pythonanywhere.com`

Enjoy! 🚀
