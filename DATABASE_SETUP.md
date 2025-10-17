# Database Configuration Guide

## Current Setup

Your application is now configured to use **SQLite** by default for local development.

### Database Configuration:
- **Local Development**: SQLite (`db.sqlite3`)
- **Production**: PostgreSQL (when `DATABASE_URL` environment variable is set)

## How It Works

The `settings.py` file checks for the `DATABASE_URL` environment variable:

```python
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    # Production: Use PostgreSQL
    DATABASES = {"default": dj_database_url.parse(DATABASE_URL, ...)}
else:
    # Development: Use SQLite
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", ...}}
```

## Local Development (Current)

✅ **Using SQLite** - No setup required!
- Database file: `db.sqlite3` (in project root)
- No external database server needed
- Perfect for development and testing

## Deploying to Production

When deploying to production (e.g., Render, Heroku), set the `DATABASE_URL` environment variable:

### On Render:
1. Go to your service dashboard
2. Navigate to "Environment" tab
3. Add environment variable:
   - **Key**: `DATABASE_URL`
   - **Value**: Your PostgreSQL connection string

### Example PostgreSQL URL:
```
postgresql://user:password@host:port/database
```

Your production URL (for reference):
```
postgresql://myapp_db_uckm_user:X3zRxCVYN98FVeVisknYOr1oVCix3qIB@dpg-d3j6thm3jp1c73f165j0-a/myapp_db_uckm
```

## Switching Databases

### To Use SQLite (Default):
- Simply run the app normally
- No environment variables needed
- Database file: `db.sqlite3`

### To Use PostgreSQL Locally:
Set the environment variable before running:

**PowerShell:**
```powershell
$env:DATABASE_URL = "postgresql://user:password@localhost/dbname"
python manage.py runserver
```

**Command Prompt:**
```cmd
set DATABASE_URL=postgresql://user:password@localhost/dbname
python manage.py runserver
```

### To Remove Environment Variable:
**PowerShell:**
```powershell
Remove-Item Env:\DATABASE_URL
```

## Current Status

✅ **SQLite is active** - You can now run your app locally without any database server!

```bash
python manage.py runserver
```

Your data is stored in `db.sqlite3` file in the project root.

## Benefits of Current Setup

1. **Easy Development**: No database server installation required
2. **Fast**: SQLite is fast for development
3. **Portable**: Database is a single file
4. **Production Ready**: Automatically switches to PostgreSQL when deployed
5. **No Configuration**: Works out of the box

## Viewing Your Database

You can view your SQLite database using:
- **DB Browser for SQLite** (https://sqlitebrowser.org/)
- **VS Code SQLite Extension**
- **Django Admin** (http://127.0.0.1:8000/admin/)

## Important Notes

- ✅ SQLite is perfect for development
- ✅ Your existing data is in `db.sqlite3`
- ✅ All migrations have been applied
- ✅ Staff profiles and barcodes are already created
- ⚠️ Don't commit `db.sqlite3` to Git (it's in `.gitignore`)
- ⚠️ Production will use PostgreSQL automatically when deployed
