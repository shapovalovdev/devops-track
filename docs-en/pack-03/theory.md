# Theory: What You Will Know by 14 September

32 concepts and technical terms covered in Pack 03. When any of these arise during an interview, you should be able to clearly explain them in your own words.

---

## Block 1 · Linux Networking & Sockets
1. **Network Socket:** A software endpoint for network communication, represented in Linux as a file descriptor.
2. **`ss -tulpn` Flags:** TCP, UDP, Listening, Process name/PID, Numeric format.
3. **`lsof` (List Open Files):** Diagnostic tool for locating open files, sockets, and active network ports of processes.
4. **`0.0.0.0` (INADDR_ANY) vs `127.0.0.1` (loopback):** Binding to all available network interfaces vs binding exclusively to the host loopback stack.
5. **Listening vs Established:** State of a socket waiting for incoming connections vs an active established data connection.
6. **Kernel Routing Table:** Kernel rules table (`ip route`) dictating packet forwarding paths.
7. **Default Gateway:** The IP address of the router handling traffic destined outside local subnets.
8. **Routing Metric:** Numerical priority assigned to routes when multiple gateways exist.
9. **`ip route get <IP>`:** Kernel diagnostic command to simulate and verify routing decisions for a specific destination.
10. **TCP 3-Way Handshake (SYN $\to$ SYN-ACK $\to$ ACK):** Three-step procedure establishing a reliable TCP connection, synchronizing sequence numbers and session parameters.
11. **Internal Network vs Host-Only vs NAT:** VirtualBox network adapter modes and their isolation semantics.

---

## Block 2 · Prometheus Architecture & Telemetry
12. **Pull Model:** Telemetry collection architectural pattern where the monitoring server actively scrapes target endpoints on a schedule.
13. **Scrape Interval & Evaluation Interval:** Frequency of target polling and alert rule evaluation cycles.
14. **Scrape Target:** An addressable endpoint (`IP:Port/metrics`) polled by Prometheus.
15. **Target Status (`UP` == 1 / `DOWN` == 0):** Internal synthetic metric `up` tracking endpoint reachability.
16. **`node_exporter`:** Linux host monitoring agent exposing OS-level metrics (CPU, memory, disk, network, load average).
17. **`cAdvisor`:** Container monitoring agent exposing Docker container resource metrics via cgroups.
18. **Time Series:** Sequence of timestamp and float value pairs identified by metric name and a set of key-value labels (`key=value`).
19. **Metric Types:**
    - **Counter:** Monotonically increasing counter (e.g., cumulative HTTP requests).
    - **Gauge:** Numerical value that fluctuates up and down (e.g., memory usage, temperature).
    - **Histogram:** Samples observations into configurable buckets to calculate percentiles (p95, p99 latency).
20. **PromQL:** Functional query language for Prometheus time series data.
21. **Instant Vector vs Range Vector:** Metric value snapshot at a specific point in time vs a buffer of values over a duration window (`[5m]`).
22. **`rate()` Function:** Computes per-second average rate of increase for counters, compensating for counter resets across restarts.
23. **`increase()` Function:** Calculates total counter increase over a specified time window.
24. **High Cardinality:** Antipattern of embedding unbounded values (e.g., user IDs, raw client IPs) in metric labels, causing catastrophic TSDB memory bloat.

---

## Block 3 · CI/CD & Operations
25. **Immutable Artifacts:** Principle ensuring container images remain unmutated once built and verified by CI.
26. **Commit SHA Tagging:** Tagging images with commit hashes (`$CI_COMMIT_SHORT_SHA`) instead of mutable `:latest`.
27. **Rollback Determinism:** Ability to reliably revert to a previous working state by deploying an explicit Git commit tag.
28. **Excalidraw Architecture Diagrams:** Visual diagramming of system services, subnets, and port mappings.
29. **Constitution Rule 1 (No Manual Mutation):** Strict prohibition of unversioned manual changes on production infrastructure.
30. **Constitution Rule 2 (PR & Blast Radius):** Explicit documentation of risks, scope, and rollback plans in every Pull Request.
31. **Time to Recovery (TTR):** Critical reliability metric measuring duration from incident onset to complete service restoration.
32. **Hand-Earned Skill:** Capability acquired through direct manual configuration and debugging without relying on unverified AI copy-pasting.
