# Why Things Are Built This Way — Foundations for Pack 03

The theory topics answer "what you will know". This document answers: **why the industry converged on these specific engineering patterns.**

The difference between a junior and an experienced engineer in an interview lies right here. A junior explains **how** to copy-paste a command; an engineer explains **what problem** it solves and what breaks under the hood if done otherwise.

---

# Part 1 · Networking and Sockets in Linux: Why So

## Why Sockets Are Files in Linux, and Why `ss` Replaced `netstat`

In Unix-like operating systems, the classic philosophy holds: *"everything is a file"*. A network connection for a process is represented as a socket file descriptor. A process opens a socket, binds it to an address and port (`bind`), switches it into listening mode (`listen`), and accepts incoming packets via kernel system calls.

Historically, engineers used `netstat` to inspect network connections. `netstat` parsed text files in pseudo-filesystems such as `/proc/net/dev` and `/proc/net/tcp`. When a system handles tens of thousands of active connections, string-parsing `/proc` in user-space causes severe kernel lock contention and performance degradation.

The **`ss` (Socket Statistics)** utility uses the **Netlink** interface — a direct binary protocol communicating with the Linux kernel. Consequently, `ss` executes instantaneously even under heavy loads with tens of thousands of active sockets.

## Why the `ss -tulpn` Flags Matter

This command is asked on virtually every technical screening. Each flag enforces kernel-level filtering:
- `-t` (**TCP**) — filter only TCP sockets.
- `-u` (**UDP**) — filter UDP sockets (DNS, DHCP, WireGuard).
- `-l` (**Listening**) — display only sockets actively listening for incoming connections (hiding established client connections).
- `-p` (**Processes**) — show the process name and PID (requires `sudo`, otherwise the kernel hides foreign processes).
- `-n` (**Numeric**) — bypass reverse DNS lookups and port name translation (displaying numeric port `80` rather than `http`).

## `0.0.0.0` vs `127.0.0.1`: The Fundamental Distinction

- `127.0.0.1` (loopback) — packets never leave the host's kernel network stack. If a service binds to `127.0.0.1:5000`, it cannot be reached from another VM, external network, or host machine browser.
- `0.0.0.0` (INADDR_ANY) — the kernel accepts incoming packets on this port arriving at **any** active network interface on the host (eth0, eth1, docker0, host-only).

When defining `ports: "80:5000"` in Docker Compose, Docker by default binds the proxy to `0.0.0.0:80`.

## Packet Routing: Why a Secondary Network Adapter Breaks Default Gateway

In the Linux kernel, the routing table (`ip route`) dictates which network interface and gateway (`gateway`) forward packets when the destination IP resides outside the local subnet.

Only one default gateway (`default via X.X.X.X dev eth0`) can be active with the lowest metric.
When adding a secondary network interface in virtualization (e.g., Host-Only for inter-VM communication alongside NAT for WAN access), the virtual DHCP server may inject a default route over the secondary adapter. If that gateway lacks Internet connectivity, outgoing packets vanish into a routing black hole.

## TCP 3-Way Handshake & Socket Lifecycle

Establishing a TCP connection between a client and a listening socket always traverses a 3-way handshake:
1. `SYN` — client sends synchronization request with initial sequence number.
2. `SYN-ACK` — server acknowledges and sends its own sequence number.
3. `ACK` — client acknowledges, transitioning the socket state to `ESTABLISHED`.

If no process is listening on the port during `SYN`, the kernel returns a packet with the `RST` flag (Connection refused). If a packet is dropped by firewall rules (`iptables`/`nftables`) with a `DROP` policy, the client experiences a connection timeout. Understanding handshake phases allows isolating network failures with `tcpdump` in seconds.

---

# Part 2 · Observability and Prometheus: Why the Pull Model

## Why Pull over Push

In legacy monitoring architectures (Zabbix Trapper, Graphite), applications actively push metrics to a centralized server.
Prometheus adopted the inverse pattern: **Pull** — the monitoring server periodically sends HTTP GET requests to the `/metrics` endpoint of each target and scrapes metrics.

**Advantages of the Pull Model:**
1. **Liveness & Failure Detection:** If a service crashes or deadlocks, it stops responding to Prometheus HTTP scrapes. The server immediately registers `up == 0`. In a push model, a dead service goes silent, making it difficult to distinguish an outage from network latency.
2. **Overload Protection:** The scraper controls ingestion rate via configurable intervals (e.g., scrape every 15s). Even if an application handles 10,000 RPS, Prometheus never gets overwhelmed by inbound metric bursts.
3. **Decoupled Debugging:** Any metric exporter can be inspected directly with a standard `curl http://<target-ip>:9100/metrics`.

## `node_exporter` vs `cAdvisor`: Separation of Concerns

- **`node_exporter`** collects host OS metrics from `/proc` and `/sys`: CPU core utilization, memory allocations, disk I/O, network interface traffic. However, it cannot attribute container-specific resource usage.
- **`cAdvisor` (Container Advisor)** hooks directly into Linux control groups (`cgroups`) and the Docker daemon (`/var/run/docker.sock`), collecting exact resource limits and per-container metrics.

---

# Part 3 · CI/CD: Why `:latest` Is Forbidden in Production

## Immutability of Release Artifacts

A container image is a binary release artifact. Tagging production images with `:latest` introduces severe operational risks:
1. It is impossible to identify which Git commit is running on production servers.
2. During an incident, instant rollbacks to a previous stable release fail because the `:latest` tag has been overwritten.
3. Local Docker caches (`docker compose pull`) may skip layer downloads if the `:latest` tag already exists locally.

Deploying with `$CI_COMMIT_SHORT_SHA` guarantees an immutable 1-to-1 link between Git commits and running production containers.

---

# Part 4 · Observability Architecture: How to Build & Read Telemetry Topologies

## Why System Topologies Must Be Built Layer-by-Layer

During technical screenings or architecture reviews, an engineer is frequently handed a whiteboard marker with the prompt: *"Draw the monitoring architecture of your production stack"*.

A messy diagram lacking clean boundaries or flow directions signals superficial knowledge. A production-grade architecture diagram is systematically structured across 10 layers:

1. **Infrastructure Nodes (Nodes & VMs):** Clear division of roles across VMs (`vm1-app`, `vm2-monitoring/gitlab`, `vm3-runner`).
2. **Network Boundaries:** Isolated subnet zones (Host-Only for workstation access, Internal for VM interconnect, NAT for egress).
3. **Application Workloads:** Containers and daemons labeled with published and private ports (`:80`, `:5000`, `:5432`, `:6379`).
4. **Telemetry Agents (Exporters):** Host-level `node_exporter` (`:9100`) and container-level `cAdvisor` (`:8080`).
5. **Prometheus Server (Scraper & TSDB):** Scrape loop engine, local TSDB storage blocks with WAL, and PromQL API (`:9090`).
6. **Pull Scrape Flows:** Request arrows point **from Prometheus to targets**.
7. **Alerting Pipeline (Alertmanager & Telegram):** Rule evaluation $\to$ POST to Alertmanager (`:9093`) $\to$ grouping/deduplication $\to$ Webhook to Telegram Bot.
8. **Log Pipelines (Loki & Promtail):** Contrasting with metrics — logs are pushed via **Push** model (`Promtail` $\to$ `Loki :3100`).
9. **Visualization Layer (Grafana):** Single-pane dashboard UI (`:3000`) querying Prometheus via PromQL and Loki via LogQL.
10. **Legend & Protocol Mapping:** Strict color coding preventing architectural ambiguity.

