# Materials for pack 01

> **English edition.** The Russian version is the original — if the two disagree, Russian wins.

A supplement to the tasks, not a replacement. The rule for this pack: **try it on the stand first, read when you're stuck.** Material read before the problem exists is gone in a week; the same material after two hours in a dead end stays for good.

Every item is marked: 🅟 primary source (official documentation — read these first) · 🅢 explainer (goes down faster, but check it against the primary source) · ⏱ rough time.

> **Don't start here.** Start with "Why it all works this way": the foundations under networking and CI/CD, ⏱ 40 min, slot C or D. The material below answers "how", and without the "why" it turns into a set of recipes.

---

## 0 · Foundations

- **[Continuous Integration — Martin Fowler](https://martinfowler.com/articles/continuousIntegration.html)** — 🅟 ⏱ 60 min. The primary source for the practice: the team integrates into a shared branch at least once a day, and every commit is verified by a full build in a reference environment. Everything CI systems do grew out of this. It's long — two sittings is fine.
- **[Deployment Pipeline — Martin Fowler](https://www.martinfowler.com/bliki/DeploymentPipeline.html)** — 🅟 ⏱ 15 min. A short note on why a pipeline is split into stages.
- **[MinimumCD — Immutable Artifact](https://minimumcd.org/minimumcd/immutable/)** — 🅟 ⏱ 10 min. The minimum without which you can't talk about continuous delivery at all. This is where "build once, promote onwards without rebuilding" comes from — and, as a consequence, dropping `latest`.
- **[Immutable artefacts — UK Home Office](https://engineering.homeoffice.gov.uk/patterns/immutable-artefacts/)** — 🅢 ⏱ 10 min. The same thing in the language of an organisation's engineering standard.
- **[Beej's Guide to Network Concepts — layered model](https://beej.us/guide/bgnet0/html/split/the-layered-network-model.html)** — 🅟 ⏱ 25 min. Why the network is layered, and what encapsulation is. Assumes nothing, reads easily — fits slot **D**.
- **[Google Cloud — Four Keys](https://cloud.google.com/blog/products/devops-sre/using-the-four-keys-to-measure-your-devops-performance)** — 🅢 ⏱ 15 min. The four DORA metrics, and the counterintuitive headline: frequent releases correlate with **fewer** incidents, not more. A ready answer to "how do you tell whether delivery is set up well".

---

## 1 · Docker networking

### 🅟 Primary sources

- **[Networking overview](https://docs.docker.com/engine/network/)** — ⏱ 20 min. The overall picture: drivers, what Docker does to the host's network. Start here.
- **[Bridge network driver](https://docs.docker.com/engine/network/drivers/bridge/)** — ⏱ 30 min. **The key text of this block.** It states outright the thing your breakage most likely rests on: on the default bridge network containers see each other **by IP only**, and name resolution works on a user-defined network alone.
- **[Networking in Compose](https://docs.docker.com/compose/how-tos/networking/)** — ⏱ 15 min. How Compose creates the project network, and why you address `service_name:internal_port` rather than the published port.
- **[Compose: the `networks` section](https://docs.docker.com/reference/compose-file/networks/)** — reference. Look at it selectively, when you need `external: true` — and you will need it, if GitLab and the stand were brought up by different compose files.
- **[`docker network create`](https://docs.docker.com/reference/cli/docker/network/create/)** — reference for the flags.

### 🅢 If the official documentation is heavy going

- **[Docker networks from the inside: iptables and Linux interfaces](https://habr.com/ru/post/333874/)** (Habr — **in Russian**) — ⏱ 40 min. What exactly Docker does to the host's network stack. It's a 2017 article: the version-specific detail is out of date, the mechanics aren't. Read it as "what's under the hood", not as instructions.
- **[A master container for a Docker network](https://habr.com/ru/articles/710126/)** (Habr — **in Russian**) — optional, network namespaces in practice.

**Don't read in this pack:** overlay, macvlan, Swarm, Kubernetes networking. Won't be useful, and will eat an evening.

---

## 2 · TCP, tcpdump, diagnostics

### 🅢 Start here — this is the rare case where the explainer beats the primary source

- **[Let's learn tcpdump! — Julia Evans](https://wizardzines.com/zines/tcpdump/)** — ⏱ 30 min. A 12-page comic zine: how to read the output, which flags matter, how to write BPF filters. The best introduction to tcpdump there is. Free to read [in the archive](https://archive.org/details/tcpdump-zine); the announcement, with the contents, is [on the author's blog](https://jvns.ca/blog/2017/04/29/new-zine--let-s-learn-tcpdump/).
- **[Linux debugging tools you'll love](https://jvns.ca/debugging-zine.pdf)** (PDF) — ⏱ 40 min. `strace`, `netstat`, `tcpdump`, `ngrep` and the rest. Goes down well in **slot D** — pictures, short pages, nothing you have to run. Also [in the archive](https://archive.org/details/debugging-zine).
- **[jvns.ca](https://jvns.ca/)** — the whole blog. For later: she writes about exactly what an SRE needs, and explains it the way you'd explain something to a colleague.

### Practice — for task 1.3

The commands from the checklist, plus some useful variants:

```
tcpdump -i any port 3000 -nn            # the one from the task
tcpdump -i any -nn 'tcp[tcpflags] & (tcp-syn|tcp-ack) != 0'   # handshakes only
tcpdump -i any -nn -v 'tcp[tcpflags] & tcp-syn != 0'          # with connection options
```

How to run it: `tcpdump` in one terminal, `curl -v` against the same address in another. You watch `[S]`, `[S.]`, `[.]` in real time. See it live once and the handshake question in an interview is closed for good.

- **[Making a Connection with tcpdump](https://www.linuxjournal.com/article/6447)** (Linux Journal) — 🅢 a line-by-line walk through the output. Old article; the output format hasn't changed since.
- **[TCP Internals: 3-way Handshake and Sequence Numbers](https://community.f5.com/kb/technicalarticles/tcp-internals-3-way-handshake-and-sequence-numbers-explained/281062)** (F5) — 🅢 if you want to get to grips with sequence numbers. Not required in this pack.

---

## 3 · GitLab Runner and CI/CD

### 🅟 For tasks 2.1 and 2.2 — the fix

- **[Troubleshooting GitLab Runner](https://docs.gitlab.com/runner/faq/)** — ⏱ 30 min. **Read this before you start fixing.** Half the hypotheses for `debug-gitlab-runner.md` come from here, including the case where the runner daemon can reach GitLab and the job container can't (the host's DNS isn't passed into the container).
- **[Docker executor](https://docs.gitlab.com/runner/executors/docker/)** — ⏱ 30 min. The key point: `network_mode` with the name of an existing network attaches the build container to it. This is most likely your missing line.
- **[Troubleshooting GitLab in Docker](https://docs.gitlab.com/install/docker/troubleshooting/)** and **[Configure GitLab in Docker](https://docs.gitlab.com/install/docker/configuration/)** — on `external_url`. Look here if the hypothesis "the address works from outside but not from inside the network" is confirmed.
- **[Advanced configuration](https://docs.gitlab.com/runner/configuration/advanced-configuration/)** — reference for `config.toml`. Selectively.

### 🅟 For task 2.3 — build and push

- **[Build and push container images](https://docs.gitlab.com/user/packages/container_registry/build_and_push_images/)** — ⏱ 40 min. The main text: authenticating to the registry, `docker build`, `docker push` from a job.
- **[Use Docker to build Docker images](https://docs.gitlab.com/ci/docker/using_docker_build/)** — ⏱ 30 min. The options (dind, socket binding) and what each one costs you. Pick one and be able to explain why — that's a question of its own in an interview.
- **[Run CI/CD jobs in Docker containers](https://docs.gitlab.com/ci/docker/using_docker_images/)** — how `image:` works in a job.

**On tags.** The GitLab documentation says it outright: use the Git SHA in the tag and every job is unique, so there's no stale image. The variable is `$CI_COMMIT_SHORT_SHA`, and the full address assembles as `$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA`. Separately: `$CI_COMMIT_REF_NAME` can contain slashes and an image tag can't, which is why `$CI_COMMIT_REF_SLUG` exists for tagging by branch. This is exactly the level of detail that separates "did it" from "read about it".

---

## 4 · The agentic harness

### 🅟 For task 4.1

- **[Claude Code — overview](https://code.claude.com/docs/en/overview)** — ⏱ 15 min. What it is and how it differs from a chat.
- **[Best practices](https://code.claude.com/docs/en/best-practices)** — ⏱ 20 min. Read it after your first run, not before.
- **[How Claude remembers a project (CLAUDE.md)](https://code.claude.com/docs/en/memory)** — ⏱ 20 min. For task 4.2. The main rule from it: if `CLAUDE.md` gets too long, half the instructions are ignored — write only what you'd otherwise have to explain every time. There's an `/init` command that drafts one from your project.

**More important than any material here:** the rule of the pack — you verify every claim the agent makes by hand. It explains and shows you where to look; you do it.

---

## 5 · Interviews

- **[Selected questions for track 1](bank.md)** — 🅟 seven questions from my own bank, sorted against tasks 1.1–1.3s: which question serves which task, whether to open it before or after, and why that one. Four are marked essential. Start here, not with the next link.
- **[devops-interview-questions](https://github.com/devops-interviews/devops-interview-questions)** (GitHub) — a third-party question bank with answers: Kubernetes, Docker, Linux, CI/CD, networking, Git, security, cloud.

**How to use it, and how not to.** Don't read it straight through — most of it is pitched at a level you're six months away from. Open it selectively: close a topic on the stand → find the matching questions → answer out loud → check yourself. Reading the answers before you've tried to answer yourself is useless: you get the feeling of knowing without the knowledge, and in an interview it falls apart.

Your own list of questions for this pack is in `interview-questions.md`. Start there; the selected set second; the third-party bank later.

---

## How to spread this across slots

| Slot | What fits here |
|---|---|
| **A** (4–5 h) | Official Docker and GitLab documentation **alongside work on the stand**. Read a paragraph → check it with a command |
| **C** (2 h) | The tcpdump zine, the Claude Code documentation, taking notes |
| **D** (1–1.5 h) | Julia Evans's zines, overview pages, the question bank. Nothing that needs you to run commands |
| **B** | — |

---

## What's deliberately not on this list

**Video courses.** Four hours a module — at 20 hours a pack, that's half the budget traded for a feeling of progress. We'll come back to them if the report shows that reading isn't working for you.

**Books.** There are good ones, but not one of them will close in two weeks, and a book abandoned a third of the way through demotivates harder than one never started.

**Material on Kubernetes, Terraform, clouds.** Not in this pack. Start them in parallel and you'll close none of them.
