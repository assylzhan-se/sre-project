from flask import Flask, request, jsonify
import time, os
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUEST_COUNT = Counter('order_requests_total', 'Total requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('order_request_duration_seconds', 'Request latency')

# Simulate DB config issue (for incident simulation)
DB_HOST = os.environ.get('DB_HOST', 'postgres')
DB_BROKEN = os.environ.get('DB_BROKEN', 'false').lower() == 'true'

orders = []
order_counter = 1

@app.route('/health')
def health():
    if DB_BROKEN:
        return jsonify({"status": "unhealthy", "service": "order", "error": "DB connection failed"}), 503
    return jsonify({"status": "healthy", "service": "order"})

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/orders', methods=['POST'])
@REQUEST_LATENCY.time()
def create_order():
    global order_counter
    if DB_BROKEN:
        REQUEST_COUNT.labels('POST', '/orders', '503').inc()
        return jsonify({"error": "Database connection failed", "db_host": DB_HOST}), 503

    data = request.get_json()
    if not data or 'product_id' not in data:
        REQUEST_COUNT.labels('POST', '/orders', '400').inc()
        return jsonify({"error": "Missing product_id"}), 400

    order = {
        "id": order_counter,
        "product_id": data['product_id'],
        "quantity": data.get('quantity', 1),
        "status": "pending",
        "created_at": time.time()
    }
    orders.append(order)
    order_counter += 1
    REQUEST_COUNT.labels('POST', '/orders', '201').inc()
    return jsonify(order), 201

@app.route('/orders', methods=['GET'])
def list_orders():
    REQUEST_COUNT.labels('GET', '/orders', '200').inc()
    return jsonify({"orders": orders, "total": len(orders)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
