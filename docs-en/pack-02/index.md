# Pack 02: Multi-stage Docker, CI/CD SSH Deploy & Rollback Runbook

!!! warning "Status: In Progress / Active Sprint (Aug 18–31, 2026)"
    Active working sprint. The focus is transitioning to zero-mutation automated deployments, deterministic Docker image builds, and disciplined incident rollback runbooks.

---

## 🎯 Key Sprint Objectives

1. **Multi-Stage Docker Image Builds**
    * Minimize final container image footprint (Alpine / Distroless base).
    * Container security: run as a non-root unprivileged user (`USER appuser`).
    * Exclude build dependencies, toolchains, and package caches from production artifacts.

2. **Automated CD via SSH with Immutable Commit SHAs**
    * Deploy explicit commit SHAs: `deploy_$CI_COMMIT_SHORT_SHA`.
    * Strict ban on mutable `latest` tags in production environments.
    * Secret and environment injection via GitLab CI Variables without committing secrets into Git.

3. **Rollback Runbook & Disaster Recovery**
    * Formalized emergency runbook for release regression recovery.
    * Instant rollback to a known-healthy SHA in $\le 60$ seconds.
    * Incident logging and runtime state capture.

4. **Nginx Reverse Proxy & Load Balancing**
    * Configure reverse proxying and upstream pass to backend containers.
    * Transparent header propagation: `Host`, `X-Real-IP`, `X-Forwarded-For`, `X-Forwarded-Proto`.
    * Upstream timeout tuning and 502/504 error handling.

5. **Pull Request Standards & Git Hygiene**
    * Structured PR descriptions detailing blast radius and validation steps.
    * Atomic semantic commits and clean git branch topology.

---

## 📚 Pack 02 Navigation

| Section | Description |
| :--- | :--- |
| 📋 **[Tasks](tasks.md)** | Active sprint assignments |
| ✅ **[Checklist](checklist.md)** | Step-by-step acceptance checklist |
| 💡 **[Fundamentals & Why](fundamentals.md)** | Architectural rationales for Docker & CI/CD standards |
| 📖 **[Theory](theory.md)** | Container architecture: namespaces, cgroups, UnionFS |
| 🔍 **[Self-Check Rubric](rubric.md)** | Self-assessment criteria and red flags |
| 💬 **[Interview Questions](questions.md)** | Common screening questions on Docker, CI/CD & Nginx |
| 📑 **[Materials](materials.md)** | Docker documentation, best practices & reference guides |
| 🗄️ **[Question Bank](bank.md)** | Technical interview question drill bank |
