# 🔑 How to Get Google Cloud Credentials

## 📋 **Step-by-Step Guide**

### **Step 1: Go to Google Cloud Console**
```
https://console.cloud.google.com/
```
- Sign in with your Google account
- This is FREE - Google provides a free tier

### **Step 2: Create a New Project**
1. Click on the project dropdown (top left)
2. Click "NEW PROJECT"
3. Project Name: `mini-bash-voice`
4. Click "CREATE"
5. Wait for project to be created

### **Step 3: Enable Required APIs**
1. Go to: https://console.cloud.google.com/apis/library
2. Search and enable each of these APIs:

   **a) Cloud Speech-to-Text API**
   - Search: "Speech-to-Text"
   - Click on "Cloud Speech-to-Text API"
   - Click "ENABLE"
   
   **b) Cloud Translation API**
   - Search: "Translation"
   - Click on "Cloud Translation API"
   - Click "ENABLE"
   
   **c) Cloud Text-to-Speech API**
   - Search: "Text-to-Speech"
   - Click on "Cloud Text-to-Speech API"
   - Click "ENABLE"

### **Step 4: Create Service Account**
1. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts
2. Click "CREATE SERVICE ACCOUNT"
3. Fill in details:
   - Service account name: `mini-bash-voice`
   - Service account ID: (auto-filled)
   - Description: `Voice control for mini bash shell`
4. Click "CREATE AND CONTINUE"
5. Grant role: Select "Project" > "Editor"
6. Click "CONTINUE"
7. Click "DONE"

### **Step 5: Create and Download JSON Key**
1. Find your service account in the list
2. Click on the service account email
3. Go to "KEYS" tab
4. Click "ADD KEY" > "Create new key"
5. Select "JSON"
6. Click "CREATE"
7. A JSON file will download automatically

### **Step 6: Place the Credentials File**
1. Rename the downloaded file to: `credentials.json`
2. Move it to: `/Users/abhisheksinghrawat/Desktop/bash/`
3. Or run this command (replace YOUR_DOWNLOADED_FILE):
```bash
mv ~/Downloads/mini-bash-voice-*.json /Users/abhisheksinghrawat/Desktop/bash/credentials.json
```

## 💰 **Pricing (Free Tier)**

Google Cloud provides FREE tier limits:
- **Speech-to-Text**: 60 minutes/month FREE
- **Translation**: 500,000 characters/month FREE  
- **Text-to-Speech**: 1 million characters/month FREE

For typical usage, you'll stay within free limits!

## ✅ **Verify Installation**

After placing credentials.json, test:
```bash
cd /Users/abhisheksinghrawat/Desktop/bash
source venv/bin/activate
python3 test_voice.py
```

You should see: **6/6 tests passed!**

## 🚀 **Start Voice Control**

Once credentials.json is in place:
```bash
cd /Users/abhisheksinghrawat/Desktop/bash
source venv/bin/activate
python3 voice_enhanced.py
```

Then speak your commands! 🎤

## 🆘 **Troubleshooting**

**Error: "credentials.json not found"**
- Make sure file is named exactly `credentials.json`
- Place in `/Users/abhisheksinghrawat/Desktop/bash/`
- Check with: `ls -la /Users/abhisheksinghrawat/Desktop/bash/credentials.json`

**Error: "Permission denied"**
- Check service account has "Editor" role
- Make sure all 3 APIs are enabled

**Error: "Quota exceeded"**
- You've used free tier limits
- Check usage at: https://console.cloud.google.com/apis/dashboard

## 📝 **Quick Links**

- Google Cloud Console: https://console.cloud.google.com/
- APIs Library: https://console.cloud.google.com/apis/library
- Service Accounts: https://console.cloud.google.com/iam-admin/serviceaccounts
- Billing (to check free tier): https://console.cloud.google.com/billing

## 🎯 **What You'll Get**

After completing these steps:
- ✅ Speak commands in Hindi or English
- ✅ Real-time voice recognition
- ✅ Automatic translation
- ✅ Voice feedback
- ✅ Full voice-controlled shell

**Total setup time: ~5-10 minutes**

---

**Need help? Check the official docs:**
https://cloud.google.com/docs/authentication/getting-started
