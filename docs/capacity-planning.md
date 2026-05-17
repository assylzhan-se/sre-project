# Capacity Planning Report
## Assignment 6 — SRE Project

---

## 1. Current Resource Consumption

### Findings from Load Testing

| Service | CPU Usage | Memory Usage | Req/sec (avg) |
|---------|-----------|--------------|---------------|
| Order Service | HIGH (~60%) | 180MB | 45 |
| Payment Service | HIGH (~55%) | 175MB | 42 |
| Auth Service | MEDIUM (~30%) | 90MB | 80 |
| Product Service | LOW (~15%) | 75MB | 30 |
| Notification Service | LOW (~10%) | 60MB | 15 |
| User Profile Service | LOW (~20%) | 70MB | 25 |
| PostgreSQL (DB) | HIGH (~70%) | 512MB | **BOTTLENECK** |

**Key Finding:** Order Service and Payment Service consume the most resources. PostgreSQL is the primary bottleneck.

---

## 2. Bottleneck Analysis

### Primary Bottleneck: PostgreSQL
- High connection count from Order and Payment services
- Missing indexes on frequently queried columns
- Sequential scans on large tables

### Secondary: Order Service
- Stateless but CPU-intensive under concurrent load
- Needs horizontal scaling beyond 2 replicas

---

## 3. Scaling Strategies

### 3.1 Horizontal Scaling (Kubernetes HPA)
```yaml
# Already defined in kubernetes/deployments.yml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: order-hpa
spec:
  minReplicas: 2
  maxReplicas: 5
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

**Trigger:** CPU > 70% → scale up to max 5 replicas

### 3.2 Vertical Scaling
Increase resource limits for Order and Payment in Kubernetes:
```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "500m"
  limits:
    memory: "512Mi"
    cpu: "1000m"
```

### 3.3 Database Optimization
- Add connection pooling (PgBouncer)
- Add indexes on `orders(product_id)`, `orders(created_at)`
- Consider read replica for query offloading

### 3.4 Docker Swarm Scaling
```bash
# Scale Order Service to 5 replicas
docker service scale sre_order=5

# Scale Payment Service to 4 replicas
docker service scale sre_payment=4
```

---

## 4. Capacity Projections

| Growth Scenario | Current | 2x Load | 5x Load |
|----------------|---------|---------|---------|
| Order replicas | 2 | 4 | 8+ |
| Payment replicas | 2 | 4 | 6 |
| DB connections needed | 20 | 40 | 100 |
| DB solution | Single | Single + Pool | Read Replica |

---

## 5. Automation: Health Checks & Restart Policies

All services have Docker health checks:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:PORT/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

Swarm restart policy:
```yaml
deploy:
  restart_policy:
    condition: on-failure
    delay: 5s
    max_attempts: 3
```
