from flask import Flask, request, Response, render_template_string
import requests
import re

app = Flask(__name__)

# 🔑 Active API Keys
VALID_API_KEYS = {
    "SANATAN_SUPER_KEY_2026",
    "JATIN_PORTAL_SECURE_99",
    "TEST_KEY_FREE"
}

# 📄 PREMIUM DOCUMENTATION TEMPLATE (UPDATED)
DOCS_HTML = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sanatan Info API Docs</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Poppins', sans-serif; }
        body { background-color: #0f172a; color: #e2e8f0; padding: 40px 20px; line-height: 1.6; }
        .container { max-width: 900px; margin: 0 auto; }
        header { border-bottom: 2px solid #1e293b; padding-bottom: 20px; margin-bottom: 30px; }
        h1 { color: #38bdf8; font-size: 2.2rem; font-weight: 700; margin-bottom: 5px; }
        .subtitle { color: #94a3b8; font-size: 1rem; }
        .card { background-color: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 25px; margin-bottom: 25px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
        h2 { color: #38bdf8; font-size: 1.4rem; font-weight: 600; margin-bottom: 15px; display: flex; align-items: center; gap: 10px; }
        p { margin-bottom: 15px; color: #cbd5e1; }
        .method { background: #0284c7; color: white; padding: 3px 8px; border-radius: 6px; font-size: 0.85rem; font-weight: bold; margin-right: 10px; }
        .endpoint { font-family: monospace; background: #0f172a; padding: 10px 15px; border-radius: 8px; color: #38bdf8; display: block; overflow-x: auto; font-size: 0.95rem; border: 1px solid #1e293b; margin: 15px 0; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; text-align: left; }
        th, td { padding: 12px; border-bottom: 1px solid #334155; }
        th { background-color: #0f172a; color: #38bdf8; font-weight: 600; }
        .code-block { background: #0f172a; border: 1px solid #1e293b; padding: 15px; border-radius: 8px; font-family: monospace; color: #a7f3d0; overflow-x: auto; font-size: 0.9rem; margin-top: 10px; }
        .footer { text-align: center; color: #64748b; font-size: 0.85rem; margin-top: 5px; border-top: 1px solid #1e293b; padding-top: 20px; }
        .tg-link { color: #38bdf8; font-weight: 600; text-decoration: none; border-bottom: 1px dashed #38bdf8; }
        .tg-link:hover { color: #0ea5e9; border-bottom-style: solid; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Sanatan Super Info API</h1>
            <div class="subtitle">Official Documentation for Developers & Portal Integration</div>
        </header>

        <div class="card">
            <h2>🌐 API Endpoint</h2>
            <span class="endpoint"><span class="method">GET</span>https://{{ host }}/api/lookup?query=NUMBER&amp;apikey=YOUR_KEY</span>
        </div>

        <div class="card">
            <h2>📋 Request Parameters</h2>
            <table>
                <thead>
                    <tr>
                        <th>Parameter</th>
                        <th>Type</th>
                        <th>Required</th>
                        <th>Description</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="font-family: monospace; color: #f43f5e;">query</td>
                        <td>String</td>
                        <td>YES</td>
                        <td>10-digit mobile number</td>
                    </tr>
                    <tr>
                        <td style="font-family: monospace; color: #f43f5e;">apikey</td>
                        <td>String</td>
                        <td>YES</td>
                        <td>For API keys, contact on Telegram: <a href="https://t.me/sanatansuperinfo" target="_blank" class="tg-link">@sanatansuperinfo</a></td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="card">
            <h2>⚡ Integration Example (JavaScript Fetch)</h2>
            <div class="code-block"><pre>
const number = "1234567890";
const apiKey = "YOUR_API_KEY_HERE"; // Put your secret key here
const url = `https://{{ host }}/api/lookup?query=${number}&apikey=${apiKey}`;

fetch(url)
  .then(response => response.text()) // .text() use karein kyunki output plain text hai
  .then(rawData => {
      console.log(rawData);
      // Iframe ya pre-tag ke andar rawData ko direct display karein
  })
  .catch(error => console.error("Error fetching data:", error));</pre></div>
        </div>

        <div class="footer">
            © 2026 Sanatan Super Info. All Rights Reserved. Master Secure Gateway Network.
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def home():
    # Vercel par chal rahe host name ko dynamically uthana taaki documentation me links automatic sahi dikhein
    current_host = request.headers.get('Host', 'sanatan-info-api.vercel.app')
    return render_template_string(DOCS_HTML, host=current_host)

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

        # 1. HTML tags aur extra lines ko clean karke raw text string nikalna
        clean_text = re.sub(r'<[^>]+>', '', res).strip()

        # 2. Main Title Header ko badalna
        if "NUMBER LOOKUP RESULT" in clean_text:
            clean_text = clean_text.replace("NUMBER LOOKUP RESULT", "SANATAN NUMBER LOOKUP RESULT")

        # 3. Telegram marketing text ko footer border tak slice/remove karna
        clean_text = re.sub(r'━+\s*💳 BUY API.*', '━━━━━━━━━━━━━━━━━━━━━━━━━━━', clean_text, flags=re.DOTALL).strip()

        # Pure Plain Text format me response return karna bina kisi masking ke
        return Response(clean_text, mimetype='text/plain')

    except Exception as e:
        return Response(f"Server Error: {str(e)}", status=500, mimetype='text/plain')

sub_app = app
