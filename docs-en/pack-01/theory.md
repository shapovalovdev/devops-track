# Pack 01 theory — exactly what you'll know by 17 August

> **English edition.** The Russian version is the original — if the two disagree, Russian wins.

The list of what gets closed in two weeks. Not "topics to read" — concepts that have to be in working order by the end of the pack.

**How to use this.** Tick ✓ only when you can explain the concept out loud in your own words **and** show it on your own stand. Knowing the wording and being able to show it are different states, and an interview tests the second one.

> This file answers **what**. The question of **why the industry arrived at these particular solutions** is answered by a separate one: "Why it all works this way". Better to read it before you start — it explains what each practice in the list below exists for, and it's where the strong interview answers come from.

Everything below is tied to the tasks in the pack. Nothing extra to read — the theory runs underneath the work, not alongside it.

---

## Block 1 — Docker networking

*Closed by tasks 1.1, 1.2, 2.1*

| ☐ | Concept | What "I know it" means |
|---|---|---|
| ☐ | **Network namespace** | Why a container has its own `localhost`, its own interfaces and its own routing table — and why that makes `127.0.0.1` inside a container unrelated to the host and unrelated to the neighbour |
| ☐ | **The `bridge` driver** | What Docker creates on the host: a virtual bridge, a subnet, NAT outbound |
| ☐ | **Default bridge vs user-defined** | Name resolution exists only on the second; on the first it's IP only. This is the cause of most "can't see its neighbour" |
| ☐ | **Docker's embedded DNS** | The resolver at `127.0.0.11` inside the container; it's what turns a service name into an address |
| ☐ | **The `host` driver** | Container in the host's namespace: no network isolation, no port publishing, port conflicts are real |
| ☐ | **The `none` driver** | Know it exists and when it's used |
| ☐ | **Publishing a port (`ports:`)** | A `host:container` forward through NAT — the only way in from outside the VM |
| ☐ | **`expose:`** | A declaration, not a publication. It opens nothing to the outside |
| ☐ | **Interface binding** | `0.0.0.0:8080` listens on every interface, `127.0.0.1:8080` only locally. The difference between "works on my machine" and "open to the internet" |
| ☐ | **Networks in Compose** | The project's default network, named networks, `external: true`, and why two separate `docker compose up` runs don't end up on the same network |
| ☐ | **Service name as an address** | In Compose you address `service_name:internal_port`, not the published port |
| ☐ | **Inspection** | `docker network ls`, `docker network inspect`, `docker inspect` — where to look at the actual state rather than the assumed one |

**Block check:** take any two containers on your stand and, without running a single command, predict whether they'll see each other by name. Then check. Matched — block closed.

---

## Block 2 — TCP, DNS and diagnostics

*Closed by task 1.3, applied in 2.1*

| ☐ | Concept | What "I know it" means |
|---|---|---|
| ☐ | **Three-way handshake** | SYN → SYN-ACK → ACK; why three packets and not two; what the two sides agree on |
| ☐ | **TCP flags in tcpdump output** | `[S]` = SYN, `[S.]` = SYN-ACK, `[.]` = ACK, `[R]` = RST, `[F]` = FIN |
| ☐ | **RST vs timeout** | A refused port is different from "the packet never arrived". The first is instant, the second hangs. This is the first fork in debugging connectivity |
| ☐ | **Listening socket** | What "a process is listening on a port" means, on which interface, by which process — the whole `ss -tulpn` output |
| ☐ | **Name resolution order** | `/etc/hosts` → DNS resolver → answer; and that inside a container this path is different from the host's |
| ☐ | **A record, TTL, authority** | Enough to read `dig` output instead of guessing |
| ☐ | **Default route** | `ip route`: where a packet goes when the destination isn't on the local network |
| ☐ | **The stages of `curl -v`** | Name resolution → TCP established → (TLS) → request sent → response. Be able to point at the boundary of each stage in the output |
| ☐ | **BPF filter** | Enough to write `port 3000`, `host X`, `tcp` and combinations — no more |
| ☐ | **The four failure points of connectivity** | Went the wrong way → never arrived → nobody to accept it → the answer never came back. Diagnosis is choosing between them |

**Block check:** break connectivity on the stand on purpose (stop a container, change a port, take it off the network) and, from the tool output alone, say what exactly is broken — before you look at what you did.

---

## Block 3 — CI/CD, the first concepts

*Closed by tasks 2.1, 2.2, 2.3, 2.4*

| ☐ | Concept | What "I know it" means |
|---|---|---|
| ☐ | **Runner** | A separate process that picks jobs up from GitLab. It lives anywhere, but it **has to be able to call** GitLab — that's the whole breakage |
| ☐ | **Registering a runner** | Token, binding, `gitlab-runner verify`, where it shows up in the UI |
| ☐ | **Executor** | What a job runs on and where (`shell`, `docker`, …) — and what that does to network reachability |
| ☐ | **`external_url` / clone URL** | Why an address that works from a browser can be unreachable from inside a container. The classic cause of "the runner won't connect" |
| ☐ | **Pipeline, stage, job** | The hierarchy and the order; what runs in parallel, what runs in sequence |
| ☐ | **`.gitlab-ci.yml`** | The structure: `stages`, `image`, `script`, `only/rules`. Be able to read someone else's file |
| ☐ | **Container registry** | What it is, what a full image address looks like, why authentication |
| ☐ | **Image tag** | A version identifier. `latest` is a moving reference, not a version |
| ☐ | **Reproducibility** | Why a commit-SHA tag gives you an unambiguous "code ↔ image" match and `latest` doesn't. One of the most frequent interview questions |
| ☐ | **Predefined variables** | `CI_COMMIT_SHORT_SHA`, `CI_REGISTRY_IMAGE`, `CI_COMMIT_REF_SLUG` — where the values come from |
| ☐ | **Build artifact** | The image as the unit of delivery: built once, after that it only gets promoted across environments |

**Block check:** explain in three minutes what happens between `git push` and a running container on the VM. Step by step, naming where each thing executes.

---

## Block 4 — Method

*Closed by tasks 2.1, 3.1, 4.1. Formally not "theory", but this is exactly what separates an engineer from someone who follows guides*

| ☐ | Concept | What "I know it" means |
|---|---|---|
| ☐ | **Falsifiable hypothesis** | Before you run the command, know **which result would disprove** the hypothesis. Otherwise it isn't a check, it's a confirmation |
| ☐ | **Halving** | Every check cuts the search space in half instead of testing one candidate at a time |
| ☐ | **Negative result** | A hypothesis that fell narrows the search just as much as one that held. Deleting it is throwing away work |
| ☐ | **Observation vs assumption** | "The container is on network X" (you looked) and "the container should be on network X" (from the config) are different statements. Debugging breaks exactly where they get confused |
| ☐ | **Agentic harness** | The agent sees files, runs commands, works in a loop — unlike a chat. And: every claim it makes gets verified by hand |

---

## What this pack deliberately leaves out

Kubernetes · Terraform · Ansible · clouds · TLS and certificates · Prometheus and metrics · SLO · orchestration · networking beyond Docker (VLAN, routing, host-level firewall)

All of it is coming. Three of those in September and October already. Right now they compete for the same 20 hours with the things nothing works without.

---

## Reporting format for the theory

Nothing separate to write. One line in the 17 August report:

> Closed ___ of 38 from the theory list. Not closed: ___ (numbers or names).

Whatever didn't close becomes a pack 02 task. That's an expected outcome, not a debt.
