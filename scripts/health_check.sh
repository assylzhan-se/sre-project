#!/bin/bash
# ─────────────────────────────────────────────────────────────
# health_check.sh — Check all microservices health
# ─────────────────────────────────────────────────────────────

services=(
  "auth:5001"
  "product:5002"
  "order:5003"
  "payment:5004"
  "notification:5005"
  "user-profile:5006"
)

echo "╔═══════════════════════════════════════════╗"
echo "║      SRE Services Health Check            ║"
echo "╠═══════════════════════════════════════════╣"

HEALTHY=0
TOTAL=${#services[@]}

for svc in "${services[@]}"; do
  NAME="${svc%%:*}"
  PORT="${svc##*:}"
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://localhost:$PORT/health)
  if [ "$STATUS" == "200" ]; then
    echo "║ ✅ $NAME (port $PORT): HEALTHY            ║"
    HEALTHY=$((HEALTHY+1))
  else
    echo "║ ❌ $NAME (port $PORT): UNHEALTHY ($STATUS)  ║"
  fi
done

echo "╠═══════════════════════════════════════════╣"
echo "║ Result: $HEALTHY/$TOTAL services healthy               ║"

# Availability SLO check
AVAILABILITY=$(echo "scale=1; $HEALTHY * 100 / $TOTAL" | bc)
echo "║ Availability: $AVAILABILITY%                        ║"
echo "╚═══════════════════════════════════════════╝"

echo ""
echo "📊 Monitoring:"
echo "  Prometheus: http://localhost:9090"
echo "  Grafana:    http://localhost:3000 (admin/admin123)"
echo "  Frontend:   http://localhost:80"
