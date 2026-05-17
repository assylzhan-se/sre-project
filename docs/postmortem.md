# Incident Postmortem Report
**Incident ID:** INC-2024-001  
**Date:** [Your date here]  
**Severity:** SEV-2 (Partial Outage)  
**Status:** Resolved  

---

## 1. Executive Summary

On [date], the **Order Service** became unavailable for approximately 5 minutes due to an incorrect database host configuration (`DB_HOST`) introduced during a deployment. Order creation was completely unavailable, affecting ~16.7% of total service availability. No data loss occurred.

---

## 2. Timeline

| Time | Event |
|------|-------|
| T+0:00 | Order Service deployed with incorrect `DB_HOST=wrong-host` |
| T+0:30 | Prometheus alert `OrderServiceUnavailable` fired |
| T+1:00 | PagerDuty notification sent to on-call engineer |
| T+1:30 | Engineer acknowledged incident, began investigation |
| T+3:00 | Root cause identified: wrong `DB_HOST` env variable |
| T+4:00 | Fix applied: corrected `DB_HOST=postgres` in compose config |
| T+4:30 | Order Service restarted successfully |
| T+5:00 | Health checks passing, metrics normalized |
| T+5:00 | Incident resolved. All SLOs restored. |

**MTTR (Mean Time To Resolve):** 5 minutes  
**MTTD (Mean Time To Detect):** 30 seconds  

---

## 3. Impact

- **Affected Service:** Order Service (port 5003)
- **Impact Duration:** ~5 minutes
- **Users Affected:** All users attempting to create orders
- **Availability during incident:** 83.3% (5/6 services healthy)
- **SLO Breach:** Availability dropped below 99% target

---

## 4. Root Cause Analysis (5 Whys)

1. **Why** did the Order Service fail?  
   → Because it could not connect to the database.

2. **Why** could it not connect to the database?  
   → Because `DB_HOST` was set to `wrong-host` instead of `postgres`.

3. **Why** was `DB_HOST` set incorrectly?  
   → Because the environment variable was manually edited and not validated before deployment.

4. **Why** was there no validation?  
   → Because the deployment process lacked automated configuration validation.

5. **Why** was there no automated validation?  
   → Because config validation was not included in the CI/CD pipeline.

**Root Cause:** Incorrect `DB_HOST` environment variable due to manual configuration without automated validation.

---

## 5. Resolution

1. Identified wrong `DB_HOST` value in running container logs
2. Corrected `DB_HOST=postgres` in `docker-compose.yml`
3. Restarted Order Service: `docker compose up -d --no-deps order`
4. Verified health endpoint returned 200
5. Confirmed Prometheus alerts resolved

---

## 6. Action Items

| Action | Owner | Priority | Due |
|--------|-------|----------|-----|
| Add env variable validation to CI/CD pipeline | DevOps | HIGH | 1 week |
| Add pre-deployment health check script | DevOps | HIGH | 1 week |
| Add Ansible lint for env var correctness | DevOps | MEDIUM | 2 weeks |
| Create runbook for Order Service DB failures | SRE | MEDIUM | 2 weeks |
| Add integration test: Order Service → DB connectivity | Dev | HIGH | 1 week |

---

## 7. Lessons Learned

- **What went well:** Fast detection via Prometheus (30s), clear alert message, quick resolution
- **What went poorly:** Manual config changes without validation; no pre-deploy smoke test
- **Where we got lucky:** No data loss; incident occurred during low-traffic period

---

## 8. Metrics

| Metric | During Incident | Normal | SLO Target |
|--------|----------------|--------|------------|
| Availability | 83.3% | 99.9% | ≥ 99% |
| Error Rate | 100% (Order) | 0.1% | ≤ 1% |
| Latency | N/A (503) | 45ms | ≤ 200ms |
