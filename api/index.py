from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

# Vercel par routing errors se bachne ke liye hum direct root '/' par hi handle kar rahe hain
@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "live", "message": "Sanatan API is running successfully!"})

@app.route('/api/lookup', methods=['GET'])
def mobile_info_2():
    number = request.args.get('query')
    if not number:
        return jsonify({"error": "Number missing"}), 400

    try:
        url = f"https://exploitsindia.site/track/live.php?term={number}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        res = requests.get(url, headers=headers, timeout=10).text

        def extract_data(pattern):
            match = re.search(pattern, res)
            return match.group(1).strip() if match else "N/A"

        name = extract_data(r"Name[:\-]?\s*([^<\n]+)")
        address = extract_data(r"Address[:\-]?\s*([^<\n]+)")

        return jsonify({
            "status": "success",
            "response": f"NAME: {name}\nNUMBER: {number}\nADDRESS: {address}"
        })
    except Exception as e:
        return jsonify({"status": "error", "response": str(e)}), 500

# Vercel ko server object chahiye hota hai
sub_app = app
