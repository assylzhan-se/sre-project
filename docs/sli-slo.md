# SLI / SLO Definitions
## Assignment 2 — SRE Project

---

## Service Level Indicators (SLIs)

### 1. Availability SLI
**Definition:** Percentage of time each service returns a successful HTTP response (2xx) to health checks.

**Formula:**
```
Availability = (successful_requests / total_requests) × 100%
```

**Prometheus Query:**
```promql
avg_over_time(up[1h]) * 100
```

---

### 2. Latency SLI
**Definition:** 95th percentile (P95) response time for HTTP requests per service.

**Formula:**
```
Latency_P95 = histogram_quantile(0.95, rate(request_duration_seconds_bucket[5m]))
```

**Prometheus Query:**
```promql
histogram_quantile(0.95, rate(order_request_duration_seconds_bucket[5m])) * 1000
```

---

### 3. Error Rate SLI
**Definition:** Percentage of requests resulting in 5xx HTTP errors.

**Formula:**
```
Error Rate = (5xx_requests / total_requests) × 100%
```

**Prometheus Query:**
```promql
rate(order_requests_total{status=~"5.."}[5m]) / rate(order_requests_total[5m]) * 100
```

---

### 4. Request Success Rate SLI
**Definition:** Percentage of requests resulting in 2xx HTTP responses.

**Formula:**
```
Success Rate = (2xx_requests / total_requests) × 100%
```

---

## Service Level Objectives (SLOs)

| SLO | Target | Measurement Window | Alert Threshold |
|-----|--------|-------------------|-----------------|
| **Availability** | ≥ 99.0% | 30-day rolling | < 99.0% |
| **Latency P95** | ≤ 200 ms | 5-minute rolling | > 200ms for 2min |
| **Error Rate** | ≤ 1.0% | 5-minute rolling | > 1% for 2min |
| **Request Success Rate** | ≥ 99.0% | 5-minute rolling | < 99% for 5min |

---

## Error Budget

**Monthly Error Budget (Availability SLO ≥ 99%):**
```
Error Budget = (1 - 0.99) × 30 days × 24 hours × 60 minutes
             = 0.01 × 43,200 minutes
             = 432 minutes/month (~7.2 hours)
```

**Error Budget Consumption:**
```promql
1 - avg_over_time(up[30d])
```

If error budget is consumed > 50%, freeze non-critical deployments.

---

## SLO Compliance Dashboard

Grafana panels to create:
1. **Availability gauge** — current vs 99% target
2. **Latency timeseries** — P50, P95, P99 per service  
3. **Error rate timeseries** — by service
4. **Error budget burn rate** — 1h, 6h, 24h windows
