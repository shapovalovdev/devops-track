# Self-Check Rubric — Pack 02

Ask yourself these questions aloud after completing each task. If you cannot answer clearly without notes, the task is not yet closed.

---

## Task 2.1: Multi-stage Dockerfile
- **Question:** Why do we separate the build into `builder` and `runtime` stages?
  - 🟢 *Green flag:* "To exclude gcc, compilers, source code, and build caches from the final image, reducing image size by up to 90% and shrinking the attack surface."
  - 🔴 *Red flag:* "Because Docker documentation says to do so."
- **Question:** Why should containers never run as `root`?
  - 🟢 *Green flag:* "The host and container share the Linux kernel. A vulnerability exploited under root privileges enables container escape, giving full host control to an attacker."
  - 🔴 *Red flag:* "Root processes consume more CPU."

---

## Task 2.2: CD Pipeline and SSH Deploy
- **Question:** Why is deploying with the `:latest` tag an antipattern in GitLab CI?
  - 🟢 *Green flag:* "It destroys traceability to Git history, makes deterministic rollbacks impossible, and Docker pull caching may skip updating changed layers."
  - 🔴 *Red flag:* "Because latest is slower."
- **Question:** How do you securely transmit SSH keys during CI/CD deployment?
  - 🟢 *Green flag:* "Store the private key as a Protected and Masked CI/CD Variable in GitLab, then inject it dynamically into `ssh-agent` in memory via `ssh-add`."
  - 🔴 *Red flag:* "Commit `id_rsa` into the repository."

---

## Task 2.3: Fast Rollback Runbook
- **Question:** What is your immediate action if a release causes HTTP 500 errors across production?
  - 🟢 *Green flag:* "Immediately open `runbook-rollback.md`, locate the last stable commit SHA, and redeploy using `IMAGE_TAG=<STABLE_SHA> docker compose up -d`, completing recovery in MTTR <1 min."
  - 🔴 *Red flag:* "Start frantically writing a hotfix commit on main."

---

## Task 2.4: PR Conventions
- **Question:** What are the three mandatory fields in each Merge Request description?
  - 🟢 *Green flag:* "1. Summary of changes; 2. Blast Radius; 3. Rollback Plan."
  - 🔴 *Red flag:* "Just a link to the issue tracker."

---

## Task 2.5: Nginx Reverse Proxy
- **Question:** What happens if Nginx fails to pass the `X-Forwarded-For` header to backend containers?
  - 🟢 *Green flag:* "The backend sees only Nginx's proxy IP (127.0.0.1) in its logs, obscuring actual client IP addresses."
  - 🔴 *Red flag:* "The server returns HTTP 502 Bad Gateway."
