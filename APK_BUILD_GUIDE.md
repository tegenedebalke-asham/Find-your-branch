# Android APK Build Guide for Find Your Branch

## Prerequisites

### System Requirements
- Ubuntu 20.04+ or macOS 10.13+
- Java JDK 11 or higher
- Android SDK (API 31 minimum)
- Python 3.8+
- Git

### Installation Steps

#### 1. Install Java JDK
```bash
sudo apt-get install openjdk-11-jdk  # Ubuntu/Debian
# or
brew install openjdk@11  # macOS
```

#### 2. Install Android SDK
```bash
# Download from: https://developer.android.com/studio
# Set ANDROID_SDK_ROOT environment variable
export ANDROID_SDK_ROOT=/path/to/android-sdk
```

#### 3. Install Python Dependencies
```bash
pip install buildozer cython
pip install -r requirements.txt
```

---

## Local Build Instructions

### Build Debug APK
```bash
# Clone the repository
git clone https://github.com/tegenedebalke-asham/Find-your-branch.git
cd Find-your-branch
git checkout android-apk-build

# Install buildozer and dependencies
pip install buildozer cython
pip install -r requirements.txt

# Build the APK
buildozer android debug

# APK output: bin/findyourbranch-*-debug.apk
```

### Build Release APK (Signed)
```bash
# First, create a keystore for signing
keytool -genkey -v -keystore ~/.android/find_your_branch.keystore \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias findyourbranch

# Update buildozer.spec with keystore details
# Then build:
buildozer android release
```

---

## Testing the APK

### On Physical Device
1. Enable USB Debugging on your Android device
2. Connect device via USB cable
3. Run:
```bash
adb install bin/findyourbranch-*-debug.apk
```

### On Android Emulator
```bash
# Start emulator
emulator -avd <your_emulator_name>

# Install APK
adb install bin/findyourbranch-*-debug.apk
```

---

## Publishing to Google Play Store

### Step 1: Create Google Play Developer Account
- Visit: https://play.google.com/console
- Pay one-time registration fee ($25 USD)
- Complete store listing details

### Step 2: Generate Release Signing Key
```bash
keytool -genkey -v -keystore find_your_branch_release.keystore \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias findyourbranch_release
```

### Step 3: Update buildozer.spec
```ini
[app:services]
android.keystore = 1
android.keystore_alias = findyourbranch_release
android.keystore_path = /path/to/find_your_branch_release.keystore
android.keystore_passwd = your_keystore_password
android.key_passwd = your_key_password
```

### Step 4: Build Release APK
```bash
buildozer android release
```

### Step 5: Upload to Play Store
1. Go to Google Play Console
2. Create new app
3. Fill in app details, screenshots, and description
4. Upload signed APK
5. Set price and distribution
6. Submit for review

---

## Automated Builds with GitHub Actions

This repository includes a GitHub Actions workflow (`.github/workflows/build-apk.yml`) that:

✅ Automatically builds APK on every push to `android-apk-build` branch
✅ Uploads APK artifacts for download
✅ Creates releases for tagged commits

### Triggering Automated Build
```bash
git push origin android-apk-build
```

Then check: https://github.com/tegenedebalke-asham/Find-your-branch/actions

---

## Troubleshooting

### Build Fails - NDK Not Found
```bash
# Download NDK 25b
buildozer android debug -- --ndk-version=25b
```

### APK Installation Fails
```bash
# Check API compatibility
adb devices
adb shell getprop ro.build.version.sdk
```

### API Connection Issues
Update the API URL in `mobile_app.py`:
```python
self.api_url = "http://your-server-ip:8000"
```

---

## Next Steps

- 📱 Test on both Android emulator and real device
- 🔐 Set up signing keys for Google Play release
- 📝 Create compelling app store listing
- 🚀 Submit to Google Play for review
- 📊 Monitor app analytics and user feedback

For more help: https://buildozer.readthedocs.io/
