# Pack 03: Prometheus from Scratch, 3-VM Monitoring & Observability Architecture

!!! info "Status: Planned for September (Sep 1–14, 2026)"
    September sprint. Focused on building production observability from the ground up, mastering time-series databases (TSDB), collecting operating system and container metrics, and crafting PromQL queries.

---

## 🎯 Key Sprint Objectives

1. **Deploying Prometheus from Scratch across 3 Virtual Machines**
    * Stand 1: Prometheus Server & TSDB storage engine.
    * Stand 2: GitLab Runner VM.
    * Stand 3: Production / Staging Application Server.
    * Explicit configuration of `prometheus.yml` (scrape targets, scrape intervals, evaluation cycles).

2. **Step-by-Step Architecture Diagram (Excalidraw)**
    * 10-tier topology: VMs, network boundaries (Host-Only, Internal, NAT), workloads, exporters (`node_exporter`, `cAdvisor`, `Promtail`).
    * Data flows: Prometheus Scrape Loop (Pull model), Alertmanager $\to$ Telegram (Alerting), Loki $\to$ Promtail (Log Push), and Grafana.
    * Cornerstone visual artifact in your portfolio for presenting and defending system architecture.

3. **OS and Container Metrics via `node_exporter` & `cAdvisor`**
    * Native installation and `systemd` daemonization of `node_exporter`.
    * Running `cAdvisor` for real-time Docker container profiling.
    * Monitoring kernel resource saturation: CPU iowait, memory cgroups, throttled tasks.

4. **PromQL Querying & System Performance Analysis**
    * Instant vectors vs range vectors and vector matching.
    * Computing true CPU utilization excluding idle time.
    * Tracking file descriptor exhaustion and disk write saturation.

5. **Alerting Rules & Notification Preparation**
    * Prometheus Alerting Rules syntax and threshold expressions.
    * Hysteresis with `for: 5m` window to prevent alert flapping.

---

## 📚 Pack 03 Navigation

| Section | Description |
| :--- | :--- |
| 📋 **[Tasks](tasks.md)** | September monitoring sprint assignments |
| ✅ **[Checklist](checklist.md)** | Verification and acceptance checklist |
| 💡 **[Fundamentals & Why](fundamentals.md)** | Architectural philosophy: Pull vs Push, TSDB, Golden Signals |
| 📖 **[Theory](theory.md)** | Prometheus internals: Counter, Gauge, Histogram, Summary |
| 🔍 **[Self-Check Rubric](rubric.md)** | Self-assessment criteria and PromQL quality indicators |
| 💬 **[Interview Questions](questions.md)** | Observability, PromQL, and metrics interview questions |
| 📑 **[Materials](materials.md)** | Official Prometheus docs, PromQL cheat sheets & references |
| 🗄️ **[Question Bank](bank.md)** | Advanced technical questions for self-drilling |
