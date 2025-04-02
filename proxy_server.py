from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

@app.route('/')
def proxy():
    target_url = request.args.get('url')
    if not target_url:
        return "<h1>Missing 'url' parameter</h1>", 400

    try:
        # Make the real request
        resp = requests.get(target_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)

        # Filter out problematic headers
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.headers.items() if name.lower() not in excluded_headers]

        return Response(resp.content, status=resp.status_code, headers=headers)
    except Exception as e:
        return f"Proxy error: {e}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # 👈 This is the Render fix
    app.run(host='0.0.0.0', port=port)
