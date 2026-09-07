# Why Things Are Built This Way — Foundations for Pack 02

The theory list answers "what I will know." This document answers: **why the industry settled on these exact engineering solutions.**

The difference between a junior and an experienced engineer in an interview is right here. A junior recites **how** to copy a command from documentation; an engineer explains **what problem** it solves and what breaks under the hood if designed differently.

---

# Part 1 · Docker: Security and Layer Optimization

## Why Multi-stage Builds Are Necessary

When compiling applications or installing dependencies with native extensions (such as Python packages requiring C compilers), building requires `gcc`, `make`, `python3-dev`, and compiler toolchains.

If these tools remain in the final production image:
1. **Image size bloats by 5–10x** (from 80 MB to 800+ MB), drastically increasing transfer times between GitLab Container Registry and production virtual machines.
2. **Attack surface expands:** if an attacker exploits an application vulnerability, compiler tools present inside the container allow building local exploits on the fly.

**Multi-stage builds** solve this structurally: the `builder` stage compiles dependencies, while the final `runtime` stage copies only compiled artifacts into a clean, minimal base image (such as Alpine or Debian Slim).

## Why Containers Must Not Run as Root

By default, Docker launches container processes as UID 0 (`root`).
Although containers isolate namespaces and cgroups, the Linux kernel is shared with the host. If a process running as root experiences a container escape (via system call vulnerabilities or exposed `/var/run/docker.sock`), the attacker gains root privileges across the entire host.

Executing processes as an unprivileged user (`USER appuser`) is a fundamental security requirement in production environments.

---

# Part 2 · CI/CD: Delivery Determinism

## Why `:latest` Is Banned in Production

A container image is an immutable build artifact.
Deploying with the `:latest` tag in CI/CD pipelines creates severe operational hazards:
1. It is impossible to identify from logs or `docker ps` which Git commit created the container in production.
2. Fast and reliable rollbacks become impossible because the prior `:latest` tag was overwritten in the registry.
3. Local caching in `docker compose pull` may assume `:latest` is unchanged and skip downloading updated image layers.

Tagging images with `$CI_COMMIT_SHORT_SHA` ensures strict determinism: every Git commit maps 1-to-1 to a unique, immutable image tag.

## Secure Secret Management in CI/CD

Never commit passwords, tokens, or private keys into Git repositories or bake them into `Dockerfile` layers.
Secrets must be injected dynamically via CI/CD environment variables with **Protected** and **Masked** attributes enabled.

For SSH deployments, the private key is held temporarily in memory using `ssh-agent` and wiped after delivery completes.

---

# Part 3 · Operations: Rollbacks and Proxying

## Reliability and DORA Metrics

Deployment performance is measured by industry-standard **DORA (DevOps Research and Assessment)** metrics:
- **Deployment Frequency:** how often code is successfully deployed to production.
- **Lead Time for Changes:** elapsed time from commit creation to production release.
- **Change Failure Rate:** percentage of deployments causing production degradation.
- **Mean Time to Recovery (MTTR):** time required to restore service after an incident.

Maintaining an automated `runbook-rollback.md` reduces MTTR from hours to under 60 seconds.

## Nginx Reverse Proxy Headers

When Nginx acts as a reverse proxy in front of backend containers:
- `Host $host` — forwards the original domain name requested by the client.
- `X-Real-IP $remote_addr` — supplies the actual IP address of the client connection.
- `X-Forwarded-For $proxy_add_x_forwarded_for` — maintains the list of proxy IPs in the request path.
- `X-Forwarded-Proto $scheme` — notifies the backend whether the initial connection was HTTP or HTTPS.

Understanding these headers and how sockets establish connections via the TCP handshake (SYN -> SYN-ACK -> ACK) is essential for diagnosing networking issues.
