# Theory: What You Will Know by 31 August

30 concepts and terms covered by Pack 02. You should be able to articulate each concept clearly in an interview without looking at notes.

---

## Block 1 · Docker and Containerization
1. **Multi-stage build:** Dockerfile optimization technique separating build-time dependencies from a minimal runtime image.
2. **`COPY --from=<stage>`:** Directive copying built artifacts between distinct Docker build stages.
3. **Non-root user (USER):** Running container processes with unprivileged UIDs to prevent host-level container escapes.
4. **HEALTHCHECK:** Dockerfile instruction periodically validating application responsiveness inside a running container.
5. **PID 1 and Signal Handling:** Process 1 in the container process namespace, responsible for intercepting `SIGTERM` and `SIGKILL`.
6. **Graceful Shutdown:** Process termination workflow allowing active network sockets to close cleanly and state to persist.
7. **Docker Layer Caching:** Mechanism caching intermediate filesystem layers based on instruction and content hashes.
8. **`.dockerignore`:** Configuration file excluding temporary files, `.git`, and local virtualenvs from the Docker build context.

---

## Block 2 · CI/CD and Delivery
9. **CI/CD Pipeline:** Automated series of sequential execution stages (build, test, deploy) for continuous integration and delivery.
10. **GitLab Runner (dind):** Execution agent supporting Docker-in-Docker workflows for building container images.
11. **Commit SHA Tagging:** Tagging container images with Git short commit hashes (`$CI_COMMIT_SHORT_SHA`) instead of mutable `:latest`.
12. **Immutable Artifacts:** Principle that compiled binary images remain unchanged across all environments.
13. **SSH-Agent:** In-memory key management utility allowing SSH authentication without writing plaintext private keys to disk.
14. **`known_hosts` and `ssh-keyscan`:** Host key verification mechanism protecting against Man-in-the-Middle (MitM) attacks.
15. **CI/CD Variables (Secrets):** Secure injection mechanism for tokens and keys using Protected and Masked flags.
16. **DORA Metrics:** Four core metrics evaluating DevOps team performance (Deployment Frequency, Lead Time, Change Failure Rate, MTTR).

---

## Block 3 · Reliability, Rollback, and Networking
17. **Rollback:** Deterministic process of reverting infrastructure to a known stable release.
18. **Rollback Runbook:** Step-by-step operating procedure for executing emergency rollbacks.
19. **Mean Time to Recovery (MTTR):** Average time taken to restore services following a production outage.
20. **PR Conventions (Rule #2):** Merge Request policy requiring summaries of Changes, Blast Radius, and Rollback Plans.
21. **Blast Radius:** Scope of potential failure or service disruption caused by a flawed modification.
22. **Reverse Proxy:** Intermediary server (such as Nginx) routing external traffic to internal backend services.
23. **`Host` Header:** HTTP request header specifying the requested server domain.
24. **`X-Real-IP` Header:** Header conveying the direct client IP to upstream services.
25. **`X-Forwarded-For` Header:** Header preserving the chain of proxy IP addresses.
26. **`X-Forwarded-Proto` Header:** Header indicating the protocol (HTTP or HTTPS) of the original client connection.
27. **TCP Handshake (SYN -> SYN-ACK -> ACK):** Three-way handshake sequence establishing reliable TCP connections.
28. **`RST` Flag (Reset):** Packet immediately terminating or rejecting invalid connection attempts to closed ports.
29. **Socket Inspection (`ss -tulpn`):** Fast Linux kernel Netlink diagnostic tool for analyzing open listening sockets.
30. **No manual mutation (Rule #1):** Core principle banning untracked manual edits on production infrastructure.
