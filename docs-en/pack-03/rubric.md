# Self-Check Rubric — Pack 03

Ask yourself these questions aloud after completing each task. If you cannot answer without checking notes, the task is not yet fully mastered.

---

## Task 1.1: Network Diagnostics
- **Question:** What does `sudo ss -tulpn` do, and why does the kernel hide process PIDs if run without `sudo`?
  - 🟢 *Green flag:* Accurately expands each flag: TCP, UDP, Listening, Processes, Numeric. Explains that foreign process socket descriptors are protected by Linux kernel permissions.
  - 🔴 *Red flag:* Confuses flag letters or vaguely states "it just lists ports".
- **Question:** If a service binds to `127.0.0.1:5000`, can another VM on the local network reach it?
  - 🟢 *Green flag:* "No. Loopback only listens within the local kernel stack. To accept external traffic, it must bind to `0.0.0.0` or the specific IP of the local network interface."
  - 🔴 *Red flag:* "Yes, if they use the host's IP address."

---

## Task 1.2: Monitoring Architecture Diagram in Excalidraw
- **Question:** Using your diagram, trace the path of an HTTP request from a browser on the laptop to the containerized application on `vm1-simpleapp`.
  - 🟢 *Green flag:* Details the exact path: Host Browser $\to$ Host-Only IP `vm1` $\to$ port 80 (Nginx reverse proxy) $\to$ Docker bridge network $\to$ port 5000 of simpleapp container.
  - 🔴 *Red flag:* Misattributes IP addresses or cannot explain Nginx reverse proxying.
- **Question:** In which direction do metric collection arrows point between Prometheus and exporters, and why?
  - 🟢 *Green flag:* "Strictly from Prometheus to `node_exporter` / `cAdvisor`, because Prometheus initiates the scheduled HTTP GET requests to `/metrics` (Pull model)."
  - 🔴 *Red flag:* "From nodes to Prometheus, because nodes push their metrics."
- **Question:** How does an alert flow through the architecture from failure detection to Telegram notification?
  - 🟢 *Green flag:* Service failure $\to$ Prometheus registers `up == 0` during Scrape Loop $\to$ Alerting Rule fires upon `evaluation_interval` $\to$ Prometheus sends POST to `Alertmanager :9093` $\to$ Alertmanager groups/deduplicates and sends HTTPS Webhook to Telegram Bot API.
  - 🔴 *Red flag:* "Prometheus sends messages directly to Telegram."

---

## Task 2.1: Prometheus + `node_exporter`
- **Question:** How does Prometheus detect that virtual machine `vm3-runner` went down?
  - 🟢 *Green flag:* "Prometheus issues periodic HTTP GET requests to `http://192.168.56.30:9100/metrics`. If the request times out or returns a connection refused error, Prometheus sets the synthetic metric `up{instance="192.168.56.30:9100"}` to 0."
  - 🔴 *Red flag:* "The VM pushes an alert to Prometheus."

---

## Task 2.2: `cAdvisor`
- **Question:** Why do we need `cAdvisor` if `node_exporter` is already running?
  - 🟢 *Green flag:* "`node_exporter` monitors host OS-level telemetry across the entire machine, whereas `cAdvisor` inspects Linux cgroups to isolate per-container resource consumption and limits."
  - 🔴 *Red flag:* "`cAdvisor` is identical to `node_exporter`, just built by Google."

---

## Task 2.3: CI/CD Tagging
- **Question:** Why is deploying with the `:latest` tag an antipattern in GitLab CI?
  - 🟢 *Green flag:* "It severs the link to the Git commit hash, prevents deterministic rollbacks, and local Docker image caches may skip layer pulls."
  - 🔴 *Red flag:* "Because `:latest` uses more disk space."
