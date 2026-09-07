# Checklist: 1–14 September 2026

## Track 1 — Foundations: Networking and Architecture
- [ ] **1.1 Linux Network Diagnostics (Minimum)**
  - [ ] Executed and analyzed `sudo ss -tulpn` flags
  - [ ] Identified listening process via `lsof -i :80` and `lsof -i -P -n | grep LISTEN`
  - [ ] Inspected kernel routing table via `ip route show` and `ip route get <IP>`
  - [ ] Created cheat sheet `docs/network-cheatsheet.md` with examples
- [ ] **1.2 Building Monitoring Architecture Diagram in Excalidraw (Minimum)**
  - [ ] Step 1: Illustrated 3 VMs (`vm1-simpleapp`, `vm2-gitlab`, `vm3-runner`) and Host Laptop with IP addresses
  - [ ] Step 2: Delineated network boundaries (`Host-Only`, `Internal Network`, `NAT`, `Docker Bridge`)
  - [ ] Step 3: Placed workloads (`Nginx`, `Simpleapp`, `PostgreSQL`, `Redis`, `GitLab`, `Registry`, `Runner`)
  - [ ] Step 4: Placed telemetry agents (`node_exporter` on 3 VMs, `cAdvisor` on vm1/vm3, `Promtail`)
  - [ ] Step 5: Illustrated Prometheus Server with Scraper, TSDB engine, and PromQL API
  - [ ] Step 6: Illustrated Pull metric scrape flows (`Prometheus` $\to$ `:9100`, `:8080`, `:9090`)
  - [ ] Step 7: Illustrated Alertmanager (`:9093`), alert dispatch flow, and Telegram Bot notifications
  - [ ] Step 8: Illustrated Push log flow (`Promtail` $\to$ `Loki :3100`) for model contrast
  - [ ] Step 9: Illustrated Grafana (`:3000`) with PromQL/LogQL sources and engineer access
  - [ ] Step 10: Formatted legend, verified readability, and exported `assets/stand-topology-v2.png`

## Track 2 — Practice: Prometheus & CI/CD Pipeline
- [ ] **2.1 Prometheus + node_exporter on 3 VMs (Minimum)**
  - [ ] Created `prometheus.yml` with static target scraping
  - [ ] Prometheus running in Docker on `vm2-gitlab`
  - [ ] `node_exporter` active on all 3 VMs
  - [ ] Verified `http://<prometheus-ip>:9090/targets` — all 3 targets report `UP`
- [ ] **2.2 Container Metrics via cAdvisor**
  - [ ] `cAdvisor` running on `vm1-simpleapp`
  - [ ] `cadvisor` scrape job added to `prometheus.yml`
  - [ ] Verified `container_cpu_usage_seconds_total` and `container_memory_usage_bytes` in Prometheus
- [ ] **2.3 Eliminating CI/CD Debt (Tagging by SHA)**
  - [ ] Configured `$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA` in `.gitlab-ci.yml`
  - [ ] Updated deployment step to target the commit hash
  - [ ] Confirmed container execution in `docker ps` on `vm1-simpleapp`

## Track 3 — Stretch and Spoken Articulation
- [ ] **3.1 [+] Basic PromQL (Stretch)**
  - [ ] Authored 5 PromQL queries (CPU %, Mem %, Disk %, Network rate, Instance Down)
- [ ] **4.1 Spoken Narration Aloud (Articulation)**
  - [ ] Rep 1 (15 min): Stand architecture and network topologies
  - [ ] Rep 2 (15 min): Prometheus pull model and exporter architecture
