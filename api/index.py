from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

# 🔑 APNI CUSTOM API KEY YAHAN SET KAREIN
# Aap isse badal kar apna koi bhi secret word ya code rakh sakte hain
VALID_API_KEYS = {
    "SANATAN_SUPER_KEY_2026",
    "JATIN_PORTAL_SECURE_99",
}

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "active",
        "message": "Sanatan Mobile Info 2 Custom API Engine is live.",
        "usage": "/api/lookup?query=NUMBER&apikey=YOUR_KEY"
    })

@app.route('/api/lookup', methods=['GET'])
def mobile_info_2():
    # 1. API Key check karne ka logic (URL parameter ya Headers dono se chalega)
    user_key = request.args.get('apikey') or request.headers.get('x-api-key')
    
    if not user_key or user_key not in VALID_API_KEYS:
        return jsonify({
            "status": "unauthorized",
            "error": "Invalid or Missing API Key. Access Denied."
        }), 401

    # 2. Query (Mobile Number) check karna
    number = request.args.get('query')
    if not number:
        return jsonify({
            "status": "bad_request",
            "error": "Mobile number query parameter is missing."
        }), 400

    try:
        # Target endpoint se data fetch karna
        url = f"https://exploitsindia.site/track/live.php?term={number}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        res = requests.get(url, headers=headers, timeout=10).text

        # Regex parsing logic
        def extract_data(pattern):
            match = re.search(pattern, res)
            return match.group(1).strip() if match else "N/A"

        name = extract_data(r"Name[:\-]?\s*([^<\n]+)")
        address = extract_data(r"Address[:\-]?\s*([^<\n]+)")

        # Professional Clean Structured JSON output jo aap kisi bhi website me easily use kar sakein
        return jsonify({
            "status": "success",
            "service": "mobile_info_2",
            "data": {
                "name": name,
                "mobile": number,
                "address": address
            },
            "raw_text": f"NAME: {name}\nNUMBER: {number}\nADDRESS: {address}"
        })

    except Exception as e:
        return jsonify({
            "status": "server_error",
            "error": str(e)
        }), 500

sub_app = app
