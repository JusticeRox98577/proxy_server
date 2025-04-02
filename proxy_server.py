from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/')
def proxy():
    target_url = request.args.get('url')
    if not target_url:
        return "Missing 'url' parameter", 400

    try:
        resp = requests.get(target_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        return Response(resp.content, status=resp.status_code, headers=dict(resp.headers))
    except Exception as e:
        return f"Proxy error: {e}", 500
