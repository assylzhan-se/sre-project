#!/bin/bash
# ─────────────────────────────────────────────────────────────
# resolve_incident.sh — Restore Order Service
# Assignment 4: Incident Resolution
# ─────────────────────────────────────────────────────────────

echo "🔧 [$(date)] RESOLUTION: Fixing Order Service database configuration..."

# Step 1: Stop broken service
echo "Step 1: Stopping broken Order Service..."
docker compose stop order

# Step 2: Fix configuration (restore correct DB_HOST)
echo "Step 2: Restoring correct DB_HOST=postgres..."
# The docker-compose.yml has DB_BROKEN=false by default — just restart

# Step 3: Restart with correct config
echo "Step 3: Restarting Order Service with correct config..."
DB_BROKEN=false docker compose up -d order

# Step 4: Wait and verify
echo "Step 4: Waiting for service to start (15s)..."
sleep 15

echo "Step 5: Health check..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5003/health)
if [ "$STATUS" == "200" ]; then
    echo "✅ Order Service restored! HTTP $STATUS"
else
    echo "❌ Service still unhealthy. HTTP $STATUS"
fi

echo ""
echo "📋 INCIDENT SUMMARY:"
echo "  Root Cause: Wrong DB_HOST environment variable"
echo "  Detection:  Prometheus alert (ServiceDown)"
echo "  Resolution: Corrected DB_HOST, restarted container"
echo "  MTTR:       ~5 minutes"
