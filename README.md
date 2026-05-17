# SRE End-Term Project
## End-to-End SRE Implementation for Distributed Microservices

---

## Architecture

```
User → Frontend (Nginx:80) → Microservices
                              ├── Auth Service        :5001
                              ├── Product Service     :5002
                              ├── Order Service       :5003
                              ├── Payment Service     :5004
                              ├── Notification Service:5005
                              └── User Profile Service:5006
                              
Infrastructure:
  PostgreSQL :5432 | Redis :6379
  Prometheus :9090 | Grafana :3000
```

---

## Quick Start

### 1. Clone repo
```bash
git clone https://github.com/YOUR_USERNAME/sre-project.git
cd sre-project
```

### 2. Run with Docker Compose
```bash
docker compose up -d --build
```

### 3. Verify services
```bash
bash scripts/health_check.sh
```

### 4. Access dashboards
| Service | URL |
|---------|-----|
| Frontend | http://localhost:80 |
| Grafana | http://localhost:3000 (admin/admin123) |
| Prometheus | http://localhost:9090 |

---

## Docker Swarm (Assignment 6)

```bash
docker swarm init
docker stack deploy -c swarm-stack.yml sre
docker service ls
```

## Kubernetes (Assignment 6)

```bash
# Build images first
docker build -t sre-auth:latest services/auth/
docker build -t sre-product:latest services/product/
docker build -t sre-order:latest services/order/
docker build -t sre-payment:latest services/payment/
docker build -t sre-notification:latest services/notification/
docker build -t sre-user-profile:latest services/user-profile/
docker build -t sre-frontend:latest frontend/

# Deploy to Kubernetes
kubectl apply -f kubernetes/deployments.yml
kubectl get pods -n sre-app
```

## Terraform (Assignment 5)

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

## Ansible (Assignment 6)

```bash
cd ansible
ansible-playbook -i inventory.ini site.yml
ansible-playbook -i inventory.ini deploy.yml
```

---

## Incident Simulation (Assignment 4)

```bash
# Trigger Order Service failure
bash scripts/simulate_incident.sh

# Resolve incident
bash scripts/resolve_incident.sh
```

---

## Load Test (Capacity Planning)

```bash
bash scripts/load_test.sh 60 5   # 60 seconds, 5 workers
```

---

## Project Structure

```
sre-project/
├── services/
│   ├── auth/           # Authentication Service
│   ├── product/        # Product Catalog Service
│   ├── order/          # Order Processing Service
│   ├── payment/        # Payment Service
│   ├── notification/   # Notification Service
│   └── user-profile/   # User Profile Service
├── frontend/           # Nginx frontend
├── monitoring/
│   ├── prometheus/     # prometheus.yml + alerts.yml
│   └── grafana/        # Dashboards + datasources
├── kubernetes/         # K8s manifests
├── terraform/          # Infrastructure as Code
├── ansible/            # Configuration management
├── scripts/            # Automation scripts
├── docs/               # SLI/SLO, postmortem, capacity planning
├── docker-compose.yml  # Main compose file
└── swarm-stack.yml     # Docker Swarm stack
```
