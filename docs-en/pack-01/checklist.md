# Pack 01 · 4–17 August 2026 — checklist

The dry list. The reasoning is in the [full version](tasks.md). Self-check questions are in the rubric. Materials are [here](materials.md).

**Core:** ~20–24 h · **Stretch [+]:** +10–12 h · **The minimum:** 2.1, 2.2, 3.1
**Report:** the evening of Monday 17 August.

Slots: **A** day off after day shifts (4–5 h) · **B** recovery day (отсыпной), 0 h · **C** day off after the recovery day (2 h) · **D** night shift from home (1–1.5 h, light only).

---

## Track 1 — Foundation

### ☐ 1.1 Diagram of the stand · A · ~1.5 h
- Draw: containers, docker networks, published ports, internal ports, who talks to whom and at what address.
- Cover: Nginx, Grafana, Loki, the database, GitLab, the runner.
- Any tool (Excalidraw, draw.io, paper + a photo).
- **Done:** the diagram is in the repository.

### ☐ 1.2 Docker networking · A or D · ~2 h
- Default `bridge` vs a user-defined bridge vs `host`.
- Resolution by service name: where it works, where it doesn't.
- `ports:` vs `expose:` in Compose.
- `localhost` inside a container.
- `docker network ls`, `docker network inspect`, `docker inspect`.
- Check all of it on your own stand: `docker exec -it <c> sh`, ping neighbours by name and by IP.
- **Done:** on the 1.1 diagram you can show why container X does or doesn't see container Y.

### ☐ 1.3 TCP and diagnostics · A · ~2 h
Trace one real request (browser → Nginx → Grafana):
- `curl -v` — take the output apart line by line.
- `ss -tulpn` — who's listening, on which interface (`0.0.0.0` vs `127.0.0.1`).
- `dig` / `nslookup` — resolution from outside and from inside the docker network.
- `tcpdump -i any port 3000 -nn` — see SYN → SYN-ACK → ACK.
- `ip route`, `ip addr`.
- **Done:** a `network-cheatsheet.md` file — commands you ran yourself, with sample output and notes.

### ☐ [+] 1.3s · Work out the difference between `127.0.0.1` and `0.0.0.0` in `ports:` from outside the VM, and what it means for security.

---

## Track 2 — Practice

### ☐ 2.1 Diagnose the breakage · A · ~2–3 h · **MINIMUM**
- Start `debug-gitlab-runner.md`, keep it as you go:
  ```
  Hypothesis N: ...
    How I checked: ...
    Result:        ...
    Conclusion:    confirmed / ruled out
  ```
- Check at minimum: whether GitLab and the runner share a docker network; what URL the runner uses to reach GitLab and whether it's reachable from inside the runner container; `docker logs` for both; `gitlab-runner verify`; whether the runner is visible in Admin → Runners; GitLab's `external_url`.
- Don't delete ruled-out hypotheses.
- **Done:** ≥ 3–4 tested hypotheses, including the ruled-out ones.

### ☐ 2.2 Fix it · A · ~1–2 h · **MINIMUM**
- Runner registered, visible in GitLab, picking up jobs.
- `.gitlab-ci.yml` with one job: `echo "hello"`.
- **Done:** green pipeline. Screenshot in the report.

### ☐ 2.3 Pipeline: build an image · A · ~3 h
- Stages `build` → `push`.
- An image of one of your services goes to the GitLab Container Registry.
- Tag by commit SHA, not `latest`.
- **Done:** the image appears in the registry after a push to a branch.

### ☐ [+] 2.3s · A `lint` stage (hadolint) before the build.

### ☐ [+] 2.4 Auto-deploy · A · ~2–3 h
- `deploy` stage: update the container on the VM with the freshly built image. SSH is acceptable.

### ☐ 2.5 Project README · C · ~1.5 h
- What the system is, the diagram from 1.1, what it's made of, how to bring it up, what decisions and why, what you'd do differently.

---

## Track 3 — Career

### ☐ 3.1 Narrating aloud · C or D · 4 × 15 min · **MINIMUM**
Phone recording, aloud, no notes, 3 minutes:
- ☐ Round 1 — what I built
- ☐ Round 2 — what broke and how I fixed it (after 2.1)
- ☐ Round 3 — why these decisions and not others
- ☐ Round 4 — everything whole, in 3 minutes

Listen back to yourself every time.
**Done:** 4 recordings. One line in the report: what changed between the first and the fourth.

### ☐ 3.2 Communities · C or D · ~40 min
- Find, across Kazakhstan and online: DevOps Days, Kubernetes meetups, IT chats on Telegram, communities at universities and companies.
- Join at least two chats.
- If there's an event in the next month — register.
- **Done:** 2 links in the report + the event with its date, if you found one.

### ☐ 3.3 Five lines for the CV · C or D · ~40 min
- 5 bullets in the form "what I did → what resulted".
- **Done:** 5 bullets in the report.

---

## Track 4 — Tooling

### ☐ 4.1 Claude Code on your own repository · A or D · ~1.5 h
- Install it, open it in the project folder.
- First task: "read my docker-compose.yml and explain how the networks are set up here, and what might stop two containers from seeing each other".
- **Rule: verify every claim by hand.**
- **Done:** one line in the report — what it got right, what it got wrong.

### ☐ [+] 4.2 `CLAUDE.md` · D · ~40 min
- What the project is, what it consists of, how it starts, any quirks.

---

## Don't touch in this pack

Kubernetes · Terraform · Ansible · clouds · certifications · Go

---

## Report — 17 August

- ☐ What you did (by number)
- ☐ What you didn't do and why
- ☐ Where you got stuck (what you did / what you expected / what you got)
- ☐ Accumulated questions
- ☐ Hours by slot: A ___ · C ___ · D ___
- ☐ What hardware you have besides this VM
- ☐ How much a month you're willing to spend on the stand
