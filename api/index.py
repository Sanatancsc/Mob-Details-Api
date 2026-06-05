from flask import Flask, request, jsonify, Response
import requests
import re

app = Flask(__name__)

# 🔑 Active API Keys
VALID_API_KEYS = {
    "SANATAN_SUPER_KEY_2026",
    "JATIN_PORTAL_SECURE_99",
    "TEST_KEY_FREE"
}

@app.route('/', methods=['GET'])
def home():
    return "Sanatan Plain Text Engine is running successfully."

@app.route('/api/lookup', methods=['GET'])
def mobile_info_2():
    # API Key Auth
    user_key = request.args.get('apikey') or request.headers.get('x-api-key')
    if not user_key or user_key not in VALID_API_KEYS:
        return Response("Access Denied: Invalid API Key.", status=401, mimetype='text/plain')

    # Number Check
    number = request.args.get('query')
    if not number:
        return Response("Error: Query mobile number is missing.", status=400, mimetype='text/plain')

    try:
        url = f"https://exploitsindia.site/track/live.php?term={number}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        res = requests.get(url, headers=headers, timeout=10).text

        # 1. Pure HTML code se elements aur breaks ko hatakar simple raw string nikalna
        clean_text = re.sub(r'<[^>]+>', '', res).strip()

        # 2. Privacy Policy Compliance: Government unique ID values ko securely mask/redact karna
        clean_text = re.sub(r'Aadhaar:\s*\d+', 'Aadhaar: [Aadhaar Redacted]', clean_text, flags=re.IGNORECASE)

        # 3. Main Title Header badalna
        if "NUMBER LOOKUP RESULT" in clean_text:
            clean_text = clean_text.replace("NUMBER LOOKUP RESULT", "SANATAN NUMBER LOOKUP RESULT")

        # 4. Telegram marketing ad text ko end separator line tak split/slice karna
        clean_text = re.sub(r'━+\s*💳 BUY API.*', '━━━━━━━━━━━━━━━━━━━━━━━━━━━', clean_text, flags=re.DOTALL).strip()

        # 🎯 SABSE ZARURI BADLAV: Pure Plain Text output return karna (No JSON brackets)
        # Is mimetype='text/plain' ki wajah se image_b61343.png wala JSON format aur pretty-print option nahi aayega
        return Response(clean_text, mimetype='text/plain')

    except Exception as e:
        return Response(f"Server Error: {str(e)}", status=500, mimetype='text/plain')

sub_app = app
