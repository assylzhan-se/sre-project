from flask import Flask, request, jsonify
import time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUEST_COUNT = Counter('product_requests_total', 'Total requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('product_request_duration_seconds', 'Request latency')

PRODUCTS = [
    {"id": 1, "name": "Laptop", "price": 999.99, "stock": 50},
    {"id": 2, "name": "Phone", "price": 599.99, "stock": 100},
    {"id": 3, "name": "Tablet", "price": 399.99, "stock": 75},
]

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "product"})

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/products', methods=['GET'])
@REQUEST_LATENCY.time()
def get_products():
    REQUEST_COUNT.labels('GET', '/products', '200').inc()
    return jsonify({"products": PRODUCTS, "total": len(PRODUCTS)})

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        REQUEST_COUNT.labels('GET', f'/products/{product_id}', '404').inc()
        return jsonify({"error": "Product not found"}), 404
    REQUEST_COUNT.labels('GET', f'/products/{product_id}', '200').inc()
    return jsonify(product)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
