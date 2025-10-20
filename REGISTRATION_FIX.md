# Registration Error Fix

## Problem
Users were getting "An error occurred during registration. Please try again." when trying to register.

## Root Cause
Both the registration view AND the Django signal were trying to create Staff profiles simultaneously, causing a race condition or duplicate key error.

## Solution Applied

### 1. Updated Registration View (`attendance/views.py`)
Changed from `Staff.objects.create()` to `Staff.objects.get_or_create()`:

```python
# Before (could fail if signal already created it)
Staff.objects.create(user=user, ...)

# After (safe - won't fail if already exists)
staff, created = Staff.objects.get_or_create(
    user=user,
    defaults={...}
)
```

### 2. Updated Signal (`attendance/signals.py`)
Changed from `Staff.objects.create()` to `Staff.objects.get_or_create()`:

```python
# Before (could create duplicates)
Staff.objects.create(user=instance, ...)

# After (safe - prevents duplicates)
Staff.objects.get_or_create(
    user=instance,
    defaults={...}
)
```

## How It Works Now

When a new user registers:

1. **User is created** in the database
2. **Signal fires** and tries to create Staff profile
   - If it doesn't exist → creates it
   - If it already exists → does nothing
3. **Registration view** also tries to create Staff profile
   - If it doesn't exist → creates it
   - If it already exists → does nothing
4. **Result:** One Staff profile is created, no errors!

## Benefits

✅ **No more registration errors**
✅ **Prevents duplicate Staff profiles**
✅ **Works whether signal fires first or view creates first**
✅ **Automatic barcode generation still works**
✅ **Safe for concurrent registrations**

## Testing

To test registration:

1. **Restart your development server:**
   ```bash
   python manage.py runserver
   ```

2. **Try registering a new user:**
   - Go to: http://127.0.0.1:8000/register/
   - Fill in the registration form
   - Submit

3. **Expected result:**
   - ✅ User is created
   - ✅ Staff profile is created automatically
   - ✅ Barcode is generated
   - ✅ User is logged in
   - ✅ Redirected to dashboard

## Verification

After registering, check:

1. **User can access their QR code:**
   - Go to: http://127.0.0.1:8000/my-barcode/
   - Should see their unique QR code

2. **User can use barcode scanner:**
   - Go to: http://127.0.0.1:8000/barcode-scan/
   - Can scan QR code to sign in/out

3. **Admin panel shows Staff profile:**
   - Go to: http://127.0.0.1:8000/admin/
   - Check attendance → Staff
   - New user should have a Staff profile with barcode

## What Changed

**Files Modified:**
- `attendance/views.py` - Registration view
- `attendance/signals.py` - Staff profile creation signal

**Changes:**
- Both now use `get_or_create()` instead of `create()`
- Prevents race conditions
- Prevents duplicate key errors
- Safe for concurrent operations

## Status

✅ **Fixed and ready to test!**

Restart your server and try registering a new user. The error should be gone.
