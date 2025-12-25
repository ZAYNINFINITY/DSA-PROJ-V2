# Mobile App Fix Summary

## ✅ What Was Fixed

The mobile app has been fixed to connect to the Flask backend. All necessary changes have been completed:

### 1. **API Configuration System** ✅
   - **File**: `frontend/public/config.js`
   - Centralized API base URL management
   - Uses `localStorage` to persist settings
   - Default URL: `http://192.168.1.100:5000` (can be changed)

### 2. **All API Calls Updated** ✅
   - **File**: `frontend/public/index.html`
   - All API endpoints now use `getApiUrl()` function:
     - `/api/queue` - Load queue
     - `/api/add` - Add patient
     - `/api/serve` - Serve patient
     - `/api/sort` - Sort queue
     - `/api/clear` - Clear queue
     - `/api/remove_served` - Remove served patient
     - `/api/export` - Export data

### 3. **Settings UI** ✅
   - Settings modal with API URL input
   - Test connection button
   - Save functionality that persists to localStorage
   - Accessible via ⚙️ Settings button

### 4. **Android HTTP Support** ✅
   - **File**: `capacitor.config.json`
     - Changed `androidScheme` from `https` to `http` to allow HTTP connections
   
   - **Files**: 
     - `android/app/src/main/res/xml/network_security_config.xml` (created)
     - `app/src/main/res/xml/network_security_config.xml` (created)
     - Network security config allows cleartext (HTTP) traffic for local networks
   
   - **Files**: 
     - `android/app/src/main/AndroidManifest.xml` (updated)
     - `app/src/main/AndroidManifest.xml` (updated)
     - Added `android:networkSecurityConfig` and `android:usesCleartextTraffic="true"`

### 5. **Web App Compatibility** ✅
   - The same `frontend/public` folder is used for both web and mobile
   - `config.js` works in both browsers and mobile webviews
   - Web app functionality is preserved

---

## 📝 How to Update API Base URL

### Option 1: In-App Settings (Recommended)
1. Open the mobile app
2. Tap the **⚙️ Settings** button
3. Enter the backend server URL (e.g., `http://192.168.1.50:5000`)
4. Tap **💾 Save**
5. The app will reload with the new URL

### Option 2: Edit Config File
1. Open `frontend/public/config.js`
2. Change line 13:
   ```javascript
   const DEFAULT_API_BASE_URL = "http://YOUR_IP_HERE:5000";
   ```
3. Rebuild the app (see instructions below)

### Finding Your IP Address
- **Windows**: Run `ipconfig` in Command Prompt, look for "IPv4 Address"
- **Mac/Linux**: Run `ifconfig` or `ip addr`, look for your network interface IP

---

## 🔨 Rebuilding the APK

After making changes, rebuild the Android app:

```bash
# 1. Sync Capacitor (copies web files to native project)
npx cap sync

# 2. Open Android Studio
npx cap open android

# 3. In Android Studio:
#    - Wait for Gradle sync to complete
#    - Click "Build" → "Build Bundle(s) / APK(s)" → "Build APK(s)"
#    - Or click "Run" → "Run 'app'" to install on connected device/emulator
```

**Alternative (Command Line Build):**
```bash
cd android
./gradlew assembleDebug
# APK will be in: android/app/build/outputs/apk/debug/app-debug.apk
```

---

## 🧪 Testing

1. **Start Flask Backend**:
   ```bash
   # In your Flask project directory
   python app.py
   # Or however you start your Flask server
   # Make sure it's accessible on your network (not just localhost)
   ```

2. **Update API URL in Mobile App**:
   - Use Settings → Enter your computer's IP (e.g., `http://192.168.1.50:5000`)
   - Or edit `config.js` before building

3. **Test Connection**:
   - Use the "🔌 Test Connection" button in Settings
   - Or try adding a patient to verify connectivity

---

## 📁 Files Changed

### Modified Files:
- `frontend/public/index.html` - All API calls use `getApiUrl()`
- `capacitor.config.json` - Changed scheme to `http`
- `android/app/src/main/AndroidManifest.xml` - Added network security config
- `app/src/main/AndroidManifest.xml` - Added network security config

### New Files:
- `frontend/public/config.js` - API configuration system
- `android/app/src/main/res/xml/network_security_config.xml` - Network security config
- `app/src/main/res/xml/network_security_config.xml` - Network security config

---

## ⚠️ Important Notes

1. **Backend Must Be Accessible**: The Flask server must be running and accessible on your network. Make sure:
   - Firewall allows connections on port 5000
   - Flask is bound to `0.0.0.0` not `127.0.0.1` (e.g., `app.run(host='0.0.0.0', port=5000)`)

2. **Web App Still Works**: The web app uses the same files, so it will also use the config system. If you need localhost for web:
   - Use the Settings UI to change it
   - Or edit `config.js` default URL

3. **Network Security**: The app now allows HTTP traffic for local networks. This is safe for development but consider HTTPS for production.

---

## ✅ Verification Checklist

- [x] All API calls use `getApiUrl()`
- [x] No hardcoded localhost/127.0.0.1 in app code
- [x] Settings UI allows changing API URL
- [x] Android network security config created
- [x] AndroidManifest updated
- [x] Capacitor config updated
- [x] Web app compatibility maintained

---

## 🚀 Ready to Use!

The mobile app is now ready to connect to your Flask backend. Just:
1. Update the API URL (via Settings or config.js)
2. Rebuild the APK
3. Install and test!



