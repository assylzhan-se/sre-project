from flask import Flask, request, jsonify
import time, random
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUEST_COUNT = Counter('payment_requests_total', 'Total requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('payment_request_duration_seconds', 'Request latency')

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "payment"})

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/payments', methods=['POST'])
@REQUEST_LATENCY.time()
def process_payment():
    data = request.get_json()
    if not data or 'order_id' not in data or 'amount' not in data:
        REQUEST_COUNT.labels('POST', '/payments', '400').inc()
        return jsonify({"error": "Missing order_id or amount"}), 400

    # Simulate payment processing (95% success rate)
    success = random.random() > 0.05
    if success:
        REQUEST_COUNT.labels('POST', '/payments', '200').inc()
        return jsonify({
            "payment_id": f"pay-{int(time.time())}",
            "order_id": data['order_id'],
            "amount": data['amount'],
            "status": "completed"
        })
    else:
        REQUEST_COUNT.labels('POST', '/payments', '402').inc()
        return jsonify({"error": "Payment declined"}), 402

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
