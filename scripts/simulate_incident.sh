#!/bin/bash
# ─────────────────────────────────────────────────────────────
# simulate_incident.sh — Trigger Order Service DB failure
# Assignment 4: Incident Simulation
# ─────────────────────────────────────────────────────────────

echo "🔴 [$(date)] INCIDENT: Triggering Order Service database failure..."

# Set wrong DB config to simulate incident
docker compose stop order
docker compose run -d \
  -e DB_HOST=wrong-host \
  -e DB_BROKEN=true \
  --name order-broken \
  order 2>/dev/null || \
docker compose up -d --no-deps \
  -e DB_BROKEN=true order

# Alternative: set env in running container
docker compose stop order
DB_BROKEN=true docker compose up -d order

echo ""
echo "🚨 INCIDENT ACTIVE:"
echo "  - Order Service: DB_BROKEN=true"
echo "  - Health endpoint will return 503"
echo "  - Prometheus alert will fire in ~30s"
echo ""
echo "Check:"
echo "  curl http://localhost:5003/health"
echo "  Open Grafana: http://localhost:3000"
echo "  Open Prometheus Alerts: http://localhost:9090/alerts"
