# Interview Questions — Pack 03

These questions are representative of real-world technical screening questions for Junior+/Middle DevOps and SRE positions.

---

## Linux Networking & Sockets
1. Which command displays listening network ports and the corresponding processes? How does `ss` differ architecturally from `netstat`?
2. What does address `0.0.0.0` mean in `ss` output? How does it differ from `127.0.0.1`?
3. What happens at the kernel level if two separate processes attempt to `bind` to the exact same IP and port simultaneously?
4. How do you inspect the Linux kernel routing table? Which command simulates the kernel route selection for packets directed to `1.1.1.1`?
5. What is a default gateway, and why can adding a secondary network interface suddenly disconnect a host from the Internet?
6. What is the TCP 3-way handshake (SYN $\to$ SYN-ACK $\to$ ACK)? What does it indicate if an incoming connection receives a packet with the `RST` flag?

---

## Prometheus & Observability
7. What is the architectural difference between Pull and Push metric collection models? What are the advantages of Prometheus's pull-based design?
8. What are the core metric types in Prometheus? Give real-world examples for `Counter`, `Gauge`, and `Histogram`.
9. How does Prometheus calculate rates of increase using `rate()`? How does `rate()` handle counter resets when a service restarts?
10. What is the distinction between `node_exporter` and `cAdvisor`?
11. What is High Cardinality in Prometheus metric labels, and why is adding unbounded strings (like user IDs or raw IP addresses) hazardous to TSDB?
12. How is the `/metrics` endpoint formatted? Which transport protocol is used during scraping?

---

## CI/CD & Production Practices
13. Why is using the `:latest` tag in CI/CD build and delivery pipelines considered an antipattern?
14. How do you engineer a deterministic rollback procedure in automated deployments?
15. What are immutable delivery artifacts, and how do they enforce reproducibility?
