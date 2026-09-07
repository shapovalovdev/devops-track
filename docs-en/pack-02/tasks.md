# Tasks for 2 Weeks: 18–31 August 2026

> **Six other documents accompany this pack:**
> [checklist](checklist.md) — the same list without commentary, for work ·
> why things are built this way — foundations under multi-stage builds, SHA tagging, and rollbacks ·
> self-check rubric — questions to ask yourself aloud after each task ·
> [theory](theory.md) — exactly what you will know by 31 August ·
> interview questions — what you will be able to answer ·
> [materials](materials.md) — what to read and when.
>
> Order: read this file in full once, then **"why things are built this way"**, and then work from the checklist.

**Pack Theme:** Closing the delivery loop — from commit to running container — and adopting production engineering workflows.

This is the second pack. In the first pack, you repaired broken infrastructure and configured the GitLab runner. In Pack 02, we complete the CI/CD pipeline: automated builds, remote deployment over SSH, healthcheck validation, and deterministic rollbacks.

---

## Why this specifically, and not something else

In the previous pack, you restored connectivity and built a Docker image. But the image remained in the container registry:
1. **Closing the delivery loop.** As long as deployments are executed manually via SSH terminals, you do not have Continuous Delivery (CD) — you have a manual assembly shop.
2. **Mastering rollbacks.** Shipping code is only half of the engineering discipline. The other half is reliably reverting to a known-good release when production degrades.
3. **Working through PRs / MRs.** No direct commits to main. Every infrastructure change is introduced through a Merge Request with explicit risk analysis and a rollback plan (Rule #2).

---

## How this fits your schedule (August)

| Slot | What it is | How much | What goes there |
|---|---|---|---|
| **A — large** | Day off after day shifts | 4–5 h | Multi-stage Dockerfile, CI/CD deploy stage, rollback runbook |
| **B — recovery day (отсыпной)** | After night shifts | **0 h** | **Strictly zero.** No tasks and no guilt |
| **C — small** | Day off after recovery day | 2 h | PR Conventions, MR reviews, Nginx & networking notes |
| **D — night shift** | If on duty and quiet | 1–1.5 h | Docs, Unix signals, TCP handshake, `ss` flags |

### Volume
- **Core (mandatory):** ~18–20 hours across two weeks.
- **Stretch (optional):** +4–6 hours (marked **[+]**).
- **Minimum (if shifts crush your schedule):** Tasks **2.1, 2.2, and 2.3**.

---

# TRACK 1 — BUILD AND OPTIMIZATION

## 2.1 Multi-stage Dockerfile Build · Slot A · ~4 h · MINIMUM

### Why
Bloated Docker images containing compilers, build tools, and package caches waste bandwidth across the network, consume disk space, and increase the attack surface. Multi-stage builds decouple the build-time environment from a minimal runtime image.

### What to do by hand
1. Refactor `Dockerfile` for `simpleapp` using multi-stage builds:
   - **Stage 1 (`builder`):** install gcc/compilers, build wheels and Python dependencies.
   - **Stage 2 (`runtime`):** lean base image (`python:3.11-slim` or `alpine`), copying only compiled artifacts (`COPY --from=builder ...`).
2. Add a non-privileged system user:
   ```dockerfile
   RUN addgroup -S appgroup && adduser -S appuser -G appgroup
   USER appuser
   ```
3. Add a native `HEALTHCHECK` directive:
   ```dockerfile
   HEALTHCHECK --interval=10s --timeout=3s --retries=3 \
     CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:5000/health || exit 1
   ```
4. Verify that image size is under **100 MB** and processes execute as non-root.

**Done when:** The image is <100MB, containers run as `appuser`, and `docker inspect` shows status `healthy`.

---

# TRACK 2 — CONTINUOUS DELIVERY (CD) AND ROLLBACK

## 2.2 Continuous Delivery via SSH in GitLab CI · Slot A · ~5 h · MINIMUM

### Why
Manual SSH commands on production hosts cause human error and configuration drift. An automated pipeline should securely connect to target hosts and deploy containers versioned strictly by commit SHA.

### What to do by hand
1. In `.gitlab-ci.yml`, declare `build` and `deploy` stages.
2. Set SHA-based image versioning:
   ```yaml
   variables:
     IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
   ```
3. In GitLab repository settings (Settings -> CI/CD -> Variables), store protected, masked variables:
   - `SSH_PRIVATE_KEY` (PEM-format private key)
   - `DEPLOY_HOST` (IP of `vm1-simpleapp`)
   - `DEPLOY_USER` (deploy user with Docker permissions)
4. Implement secure SSH dispatch in the deploy job using `ssh-agent`:
   ```yaml
   deploy:
     stage: deploy
     image: alpine:latest
     before_script:
       - apk add --no-cache openssh-client
       - eval $(ssh-agent -s)
       - echo "$SSH_PRIVATE_KEY" | tr -d '\r' | ssh-add -
       - mkdir -p ~/.ssh && chmod 700 ~/.ssh
       - ssh-keyscan -H "$DEPLOY_HOST" >> ~/.ssh/known_hosts
     script:
       - ssh $DEPLOY_USER@$DEPLOY_HOST "docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY"
       - ssh $DEPLOY_USER@$DEPLOY_HOST "export IMAGE_TAG=$IMAGE_TAG && docker compose pull && docker compose up -d"
   ```
5. Commit, verify pipeline execution, and confirm `docker ps` on `vm1` reflects the commit SHA.

**Done when:** Pushing to main automatically updates containers on `vm1`, and the pipeline turns green.

---

## 2.3 Fast Deterministic Rollback (Rollback Runbook) · Slot A · ~3 h · MINIMUM

### Why
When a release introduces a critical failure, an engineer should not improvise under pressure. You need a tested, documented runbook to rollback within 60 seconds.

### What to do by hand
1. Author `docs/runbook-rollback.md`:
   - Identifying the last stable commit SHA.
   - Emergency redeployment command:
     `IMAGE_TAG=<STABLE_SHA> docker compose up -d`
   - Verification procedures after rollback.
2. Simulate a production incident:
   - Deploy a broken commit (e.g., immediate exit 1 on startup).
   - Time the recovery using your runbook.
   - Record the Mean Time to Recovery (MTTR).

**Done when:** You can execute a complete rollback in under 1 minute following `runbook-rollback.md`.

---

# TRACK 3 — PRACTICES AND EXTENSION

## 2.4 PR Conventions (Practice Constitution, Rule #2) · Slot C · ~2 h

### What to do
Route all code and infrastructure modifications through Merge Requests. Each MR description must fulfill three required fields:
1. **Changes:** (Summary of modifications).
2. **Blast Radius:** (Potential impact if flawed).
3. **Rollback Plan:** (Exact commands to revert).

Merge at least 4 MRs structured with these conventions.

---

## 2.5 [+] Nginx Reverse Proxy Headers · Slot D · ~2 h · STRETCH

### What to do
1. Inspect reverse proxy configuration in Nginx:
   ```nginx
   proxy_set_header Host $host;
   proxy_set_header X-Real-IP $remote_addr;
   proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
   proxy_set_header X-Forwarded-Proto $scheme;
   ```
2. Understand why omitting `Host` breaks virtual hosting, and how `X-Forwarded-For` preserves client IP addresses.
3. Validate access logs across Nginx and backend services.

---

## 3.1 Spoken Narration Aloud (Articulation) · Slot C · ~1 h

### What to do
Record your voice on your phone and speak for 15 minutes per topic without notes:
- **Rep 1:** "How my CI/CD delivery pipeline works: build stages, why we tag by SHA, how SSH keys and secrets are handled, and why `:latest` is prohibited."
- **Rep 2:** "My emergency response workflow during broken deployments: healthchecks, rollback runbooks, and DORA metrics."
