# Barcode/QR Code Attendance System

## Overview
The barcode scanning system allows staff members to sign in and out using QR codes instead of traditional username/password authentication. This provides a faster, more convenient way to track attendance.

## Features

### 1. **Personal QR Code**
- Each staff member has a unique QR code automatically generated upon account creation
- QR codes can be viewed at: `/my-barcode/` or via the user dropdown menu
- QR codes can be printed for physical badges or saved on mobile devices

### 2. **Barcode Scanner Page**
- Accessible at: `/barcode-scan/`
- Two scanning methods:
  - **Camera Scanning**: Use device camera to scan QR codes
  - **Manual Entry**: Type in the barcode manually (useful for hardware barcode scanners)

### 3. **Automatic Sign In/Out**
- System automatically determines whether to sign in or sign out based on current status
- Displays success message with user name and timestamp
- Works without requiring login (authentication via barcode)

## How to Use

### For Staff Members:

#### Getting Your QR Code:
1. Log in to your account
2. Click on your name in the top right corner
3. Select "My QR Code" from the dropdown
4. Print or save the QR code to your device

#### Signing In/Out with QR Code:
1. Go to the barcode scanner page (link in navigation: "Scan QR")
2. Choose your scanning method:
   - **Camera**: Click "Use Camera" and point your device at the QR code
   - **Manual**: Click "Manual Entry" and type the barcode ID
3. The system will automatically sign you in or out

### For Administrators:

#### Generating Barcodes for Existing Staff:
```bash
python manage.py generate_barcodes
```

#### Setting Up a Scanner Station:
1. Set up a tablet or computer at the entrance
2. Open the barcode scanner page in a browser
3. Keep the page open for staff to use
4. Staff can scan their QR codes or use a hardware barcode scanner

## Technical Details

### Database Changes:
- Added `barcode` field to `Staff` model
- Barcodes are automatically generated using UUID format: `STAFF-XXXXXXXXXXXX`
- Each barcode is unique and indexed for fast lookups

### New URLs:
- `/my-barcode/` - View your personal QR code
- `/barcode-scan/` - Scanner interface
- `/barcode-authenticate/` - API endpoint for barcode authentication (POST)

### Security:
- Barcodes are unique and cannot be guessed
- Only active staff accounts can use barcodes
- All authentication attempts are logged
- Barcodes are tied to user accounts and cannot be transferred

## Browser Compatibility
- Camera scanning requires HTTPS in production (works on localhost for development)
- Supported browsers: Chrome, Firefox, Safari, Edge (latest versions)
- Mobile devices: iOS Safari, Android Chrome

## Troubleshooting

### Camera Not Working:
- Check browser permissions for camera access
- Ensure you're using HTTPS (required for camera in production)
- Try using manual entry instead

### Barcode Not Recognized:
- Ensure the QR code is clear and well-lit
- Try manual entry with the barcode ID
- Contact admin if barcode is missing

### Already Signed In/Out:
- Each staff member can only sign in once and sign out once per day
- Check your current status on the sign-in page

## Future Enhancements
- Mobile app for easier QR code access
- NFC badge support
- Barcode expiration and rotation
- Multi-location support with location-specific QR codes
