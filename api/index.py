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
        "message": "Sanatan Master Engine is running.",
        "usage": "/api/lookup?query=NUMBER&apikey=YOUR_KEY"
    })

@app.route('/api/lookup', methods=['GET'])
def mobile_info_2():
    # API Key Authentication
    user_key = request.args.get('apikey') or request.headers.get('x-api-key')
    if not user_key or user_key not in VALID_API_KEYS:
        return jsonify({"status": "unauthorized", "error": "Access Denied."}), 401

    # Number Query Check
    number = request.args.get('query')
    if not number:
        return jsonify({"status": "bad_request", "error": "Query number missing."}), 400

    try:
        url = f"https://exploitsindia.site/track/live.php?term={number}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        res = requests.get(url, headers=headers, timeout=10).text

        # --- ADVANCED EXACT-MATCH PARSING LOGIC ---
        # HTML tags ko clean text me convert karna taki regex perfectly match ho
        clean_text = re.sub(r'<[^>]+>', '', res)
        clean_text = re.sub(r'&zwj;', '', clean_text)  # Zero-width joiners clean karna

        # Sabhi fields ko alag-alag extract karna (Multiple records handle karne ke liye)
        names = re.findall(r"Name:\s*([^\n]+)", clean_text)
        fathers = re.findall(r"Father Name:\s*([^\n]+)", clean_text)
        mobiles = re.findall(r"Mobile:\s*([^\n]+)", clean_text)
        addresses = re.findall(r"Address:\s*([^\n]+)", clean_text)
        alternates = re.findall(r"Alternate:\s*([^\n]+)", clean_text)
        circles = re.findall(r"Circle:\s*([^\n]+)", clean_text)
        aadhars = re.findall(r"Aadhaar:\s*([^\n]+)", clean_text)

        # 🎯 EXACT MATCH OUTPUT FORMAT GENERATION
        output = []
        output.append("✨ SANATAN NUMBER LOOKUP RESULT")
        output.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        output.append(f"Lookup Result for: {number}")
        output.append("────────────────────────\n")

        # 1st Record (Primary Profile)
        if len(names) > 0:
            output.append(f"👤 Name: {names[0].strip()}")
            output.append(f"👨‍👦 Father Name: {fathers[0].strip() if len(fathers) > 0 else 'NA'}")
            output.append(f"📱 Mobile: {mobiles[0].strip() if len(mobiles) > 0 else number}")
            output.append(f"🏠 Address: {addresses[0].strip() if len(addresses) > 0 else 'NA'}")
            output.append(f"📞 Alternate: {alternates[0].strip() if len(alternates) > 0 else 'NA'}")
            output.append(f"📡 Circle: {circles[0].strip() if len(circles) > 0 else 'NA'}")
            
            # Security Policy Compliance Masking for System Output
            raw_aadh = aadhars[0].strip() if len(aadhars) > 0 else 'NA'
            display_aadh = "[Aadhaar Masked]" if raw_aadh != 'NA' and raw_aadh.isdigit() else raw_aadh
            output.append(f"🪪 Aadhaar: {display_aadh}")

        # 2nd Record (Additional Result)
        if len(names) > 1:
            output.append("\n────────────────────────")
            output.append("📌 Additional Result:\n")
            output.append(f"👤 Name: {names[1].strip()}")
            output.append(f"👨‍👦 Father Name: {fathers[1].strip() if len(fathers) > 1 else 'NA'}")
            output.append(f"📱 Mobile: {mobiles[1].strip() if len(mobiles) > 1 else 'NA'}")
            output.append(f"🏠 Address: {addresses[1].strip() if len(addresses) > 1 else 'NA'}")
            output.append(f"📞 Alternate: {alternates[1].strip() if len(alternates) > 1 else 'NA'}")
            output.append(f"📡 Circle: {circles[1].strip() if len(circles) > 1 else 'NA'}")
            
            raw_aadh2 = aadhars[1].strip() if len(aadhars) > 1 else 'NA'
            display_aadh2 = "[Aadhaar Masked]" if raw_aadh2 != 'NA' and raw_aadh2.isdigit() else raw_aadh2
            output.append(f"🪪 Aadhaar: {display_aadh2}")

        output.append("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        final_response_text = "\n".join(output)

        return jsonify({
            "status": "success",
            "service": "mobile_info_2",
            "data": {
                "primary_name": names[0].strip() if names else "N/A",
                "primary_mobile": mobiles[0].strip() if mobiles else number,
                "primary_address": addresses[0].strip() if addresses else "N/A"
            },
            "response": final_response_text
        })

    except Exception as e:
        return jsonify({"status": "server_error", "error": str(e)}), 500

sub_app = app
