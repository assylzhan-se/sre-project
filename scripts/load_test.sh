#!/bin/bash
# ─────────────────────────────────────────────────────────────
# load_test.sh — Generate load for capacity planning analysis
# Assignment 6: Capacity Planning
# ─────────────────────────────────────────────────────────────

DURATION=${1:-60}   # seconds
CONCURRENCY=${2:-5} # parallel workers

echo "🔥 Starting load test (${DURATION}s, ${CONCURRENCY} workers)..."

# Function to hit services repeatedly
run_load() {
    END=$((SECONDS + DURATION))
    while [ $SECONDS -lt $END ]; do
        curl -s http://localhost:5002/products > /dev/null &
        curl -s -X POST http://localhost:5001/auth/login \
          -H "Content-Type: application/json" \
          -d '{"username":"testuser"}' > /dev/null &
        curl -s -X POST http://localhost:5003/orders \
          -H "Content-Type: application/json" \
          -d '{"product_id":1,"quantity":2}' > /dev/null &
        curl -s http://localhost:5006/profiles/testuser > /dev/null &
        wait
        sleep 0.1
    done
}

# Start concurrent workers
for i in $(seq 1 $CONCURRENCY); do
    run_load &
done

echo "Load running... (Ctrl+C to stop)"
echo "Watch metrics at: http://localhost:9090"
echo "Watch Grafana at: http://localhost:3000"

wait
echo "✅ Load test complete"
