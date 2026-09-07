# Checklist: 18–31 August 2026

## Track 1 — Build and Optimization
- [ ] **2.1 Multi-stage Dockerfile (Minimum)**
  - [ ] Written builder and runtime stages
  - [ ] Configured unprivileged `appuser`
  - [ ] Added container `HEALTHCHECK`
  - [ ] Verified final image size (<100 MB)

## Track 2 — CI/CD Pipeline & Rollback
- [ ] **2.2 Continuous Delivery via SSH (Minimum)**
  - [ ] Configured `CI/CD Variables` (`SSH_PRIVATE_KEY`, `DEPLOY_HOST`, `DEPLOY_USER`)
  - [ ] Added `deploy` stage in `.gitlab-ci.yml` using `ssh-agent`
  - [ ] Configured image tagging by `$CI_COMMIT_SHORT_SHA`
  - [ ] Verified automated remote deployment to `vm1-simpleapp`
- [ ] **2.3 Fast Rollback Runbook (Minimum)**
  - [ ] Authored `docs/runbook-rollback.md`
  - [ ] Simulated broken release and executed rollback in <60s
  - [ ] Measured Mean Time to Recovery (MTTR)

## Track 3 — Practices & Articulation
- [ ] **2.4 PR Conventions (Rule #2)**
  - [ ] Authored and merged 4 MRs with Changes / Blast Radius / Rollback Plan
- [ ] **2.5 [+] Nginx Reverse Proxy Headers (Stretch)**
  - [ ] Configured `Host`, `X-Real-IP`, `X-Forwarded-For`, `X-Forwarded-Proto`
- [ ] **3.1 Spoken Narration Aloud (Articulation)**
  - [ ] Rep 1 (15 min): CI/CD pipeline architecture and eliminating `:latest`
  - [ ] Rep 2 (15 min): Emergency rollback procedures and DORA metrics
