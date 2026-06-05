from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

# 🔑 Active API Keys
VALID_API_KEYS = {
    "SANATAN_SUPER_KEY_2026",
    "JATIN_PORTAL_SECURE_99"
}

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "active",
        "message": "Sanatan Raw Engine is running."
    })

@app.route('/api/lookup', methods=['GET'])
def mobile_info_2():
    # API Key Auth
    user_key = request.args.get('apikey') or request.headers.get('x-api-key')
    if not user_key or user_key not in VALID_API_KEYS:
        return jsonify({"status": "unauthorized", "error": "Access Denied."}), 401

    # Number Check
    number = request.args.get('query')
    if not number:
        return jsonify({"status": "bad_request", "error": "Query missing."}), 400

    try:
        url = f"https://exploitsindia.site/track/live.php?term={number}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        res = requests.get(url, headers=headers, timeout=10).text

        # 1. Pure HTML code se elements aur breaks ko hatakar simple string banana
        # Jisse raw file ka plain structure text mil sake
        clean_text = re.sub(r'<[^>]+>', '', res).strip()

        # 2. Privacy Policy Compliance: Output se sensitive government unique IDs ko mask karna
        clean_text = re.sub(r'Aadhaar:\s*\d+', 'Aadhaar: [Aadhaar Redacted]', clean_text, flags=re.IGNORECASE)

        # 3. Main Title Section ko change karna
        if "NUMBER LOOKUP RESULT" in clean_text:
            clean_text = clean_text.replace("NUMBER LOOKUP RESULT", "SANATAN NUMBER LOOKUP RESULT")

        # 4. Slicing: Telegram marketing footer links ko lines ke sath trim karna
        # Jisse text sirf exact separator border line par hi stop ho jaye
        clean_text = re.sub(r'━+\s*💳 BUY API.*', '━━━━━━━━━━━━━━━━━━━━━━━━━━━', clean_text, flags=re.DOTALL).strip()

        return jsonify({
            "status": "success",
            "service": "mobile_info_2",
            "data": {
                "mobile": number
            },
            # Yeh bilkul image_b61b3b.png jaisa exact sequence space flow return karega
            "response": clean_text
        })

    except Exception as e:
        return jsonify({"status": "server_error", "error": str(e)}), 500

sub_app = app
