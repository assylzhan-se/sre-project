from flask import Flask, request, jsonify
import time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUEST_COUNT = Counter('userprofile_requests_total', 'Total requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('userprofile_request_duration_seconds', 'Request latency')

profiles = {}

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "user-profile"})

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/profiles/<username>', methods=['GET'])
@REQUEST_LATENCY.time()
def get_profile(username):
    if username not in profiles:
        profiles[username] = {
            "username": username,
            "email": f"{username}@example.com",
            "created_at": time.time(),
            "orders_count": 0
        }
    REQUEST_COUNT.labels('GET', '/profiles', '200').inc()
    return jsonify(profiles[username])

@app.route('/profiles/<username>', methods=['PUT'])
def update_profile(username):
    data = request.get_json()
    if username not in profiles:
        profiles[username] = {"username": username, "created_at": time.time()}
    profiles[username].update(data)
    REQUEST_COUNT.labels('PUT', '/profiles', '200').inc()
    return jsonify(profiles[username])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006)
