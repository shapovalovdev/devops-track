# Pack 01: Networking, Linux & Stand Recovery

!!! success "Status: Completed (Aug 4–17, 2026)"
    All core objectives of the first sprint have been successfully achieved. The testing stand is operational, the ext4 filesystem has been restored, an isolated GitLab Runner is registered, and the first working CI/CD pipeline is running.

---

## 🎯 What Was Accomplished

During sprint 01, we transitioned from ad-hoc manual management to a reproducible engineering infrastructure, establishing a solid Linux foundation:

1. **ext4 Filesystem Disaster Recovery**
    * Diagnostic analysis of corrupted superblocks using `fsck` and `e2fsck`.
    * Configured `/etc/fstab` with reliable block device UUIDs and mount options.
    * Data integrity recovery without configuration loss.

2. **GitLab & Runner Infrastructure (Stand 1)**
    * Deployed a standalone GitLab CE instance on a dedicated VM.
    * Registered and configured GitLab Runner using Docker-in-Docker (dind) executor.
    * Security threat model: Docker socket mounting (`/var/run/docker.sock`) vs isolated dind with TLS daemon.

3. **Linux Network Stack & Sockets**
    * Hands-on tracing of TCP 3-way handshake (SYN $\to$ SYN-ACK $\to$ ACK) and 4-way teardown (FIN/ACK).
    * Investigated socket lifecycles: `LISTEN`, `ESTABLISHED`, `TIME_WAIT`, `CLOSE_WAIT`.
    * Deep network diagnostics using modern Linux tooling: `ss -tulpn`, `ip route`, `tcpdump -nn -i any`.

4. **SSH Authentication & Key Management**
    * Key formats and cryptography: legacy PEM PKCS#1 vs modern OpenSSH, Ed25519 vs RSA 4096.
    * Strict filesystem permissions: `chmod 700 ~/.ssh` and `chmod 600 ~/.ssh/authorized_keys`.
    * Protocol and cipher negotiation debugging with `ssh -vvv`.

5. **First Production Pipeline**
    * Declarative `.gitlab-ci.yml` architecture with defined execution stages.
    * Artifact packaging and passing between downstream stages.

---

## 📚 Pack 01 Navigation

| Section | Description |
| :--- | :--- |
| 📋 **[Tasks](tasks.md)** | Hands-on sprint assignments |
| ✅ **[Checklist](checklist.md)** | Step-by-step acceptance criteria |
| 💡 **[Fundamentals & Why](fundamentals.md)** | Deep-dive architectural rationales |
| 📖 **[Theory](theory.md)** | Theory: Linux kernel, sockets, processes |
| 🔍 **[Self-Check Rubric](rubric.md)** | Evaluation criteria and red flags |
| 💬 **[Interview Questions](questions.md)** | Real-world Middle DevOps screening questions |
| 📑 **[Materials](materials.md)** | Curated RFCs, documentation, and references |
| 🗄️ **[Question Bank](bank.md)** | Additional technical practice questions |
