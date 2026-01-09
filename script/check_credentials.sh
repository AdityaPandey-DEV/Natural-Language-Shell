#!/bin/bash

# Advanced Mini Bash Shell - Credentials Checker
# This script checks if Google Cloud credentials are properly configured

echo "🔍 Checking Google Cloud Credentials Setup"
echo "==========================================="
echo

# Check if credentials.json exists
if [ -f "credentials.json" ]; then
    echo "✅ credentials.json found"
    
    # Check if it's valid JSON
    if python3 -c "import json; json.load(open('credentials.json'))" 2>/dev/null; then
        echo "✅ credentials.json is valid JSON"
        
        # Check required fields
        PROJECT_ID=$(python3 -c "import json; print(json.load(open('credentials.json')).get('project_id', 'NOT_FOUND'))" 2>/dev/null)
        CLIENT_EMAIL=$(python3 -c "import json; print(json.load(open('credentials.json')).get('client_email', 'NOT_FOUND'))" 2>/dev/null)
        
        if [ "$PROJECT_ID" != "NOT_FOUND" ]; then
            echo "✅ Project ID: $PROJECT_ID"
        else
            echo "❌ Project ID not found in credentials.json"
        fi
        
        if [ "$CLIENT_EMAIL" != "NOT_FOUND" ]; then
            echo "✅ Service Account: $CLIENT_EMAIL"
        else
            echo "❌ Service account email not found in credentials.json"
        fi
        
        echo
        echo "🎉 Credentials are properly configured!"
        echo
        echo "🚀 Ready to start voice control:"
        echo "   source venv/bin/activate"
        echo "   python3 voice_enhanced.py"
        echo
        
    else
        echo "❌ credentials.json is not valid JSON"
        echo
        echo "Please download a new credentials.json from:"
        echo "https://console.cloud.google.com/iam-admin/serviceaccounts"
    fi
else
    echo "❌ credentials.json not found"
    echo
    echo "📋 To get credentials:"
    echo "   1. Go to: https://console.cloud.google.com/"
    echo "   2. Create a project"
    echo "   3. Enable APIs: Speech-to-Text, Translation, Text-to-Speech"
    echo "   4. Create service account"
    echo "   5. Download JSON key"
    echo "   6. Rename to 'credentials.json'"
    echo "   7. Place in this directory"
    echo
    echo "📖 Detailed instructions: cat GET_CREDENTIALS.md"
fi

echo
echo "==========================================="
