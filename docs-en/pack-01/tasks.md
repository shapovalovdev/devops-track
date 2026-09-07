# Tasks for two weeks: 4–17 August 2026

> **Six more documents go with this pack:**
> [checklist](checklist.md) — the same thing without the explanations, to work from ·
> why it's all set up this way — the grounding under networking and CI/CD ·
> self-check rubric — questions to ask yourself after each task ·
> [theory](theory.md) — what exactly you'll know by 17 August ·
> interview questions — what you'll be able to answer ·
> [materials](materials.md) — what to read and when.
>
> Order: this file end to end first (once), then **"why it's all set up this way"**, then work from the checklist.
>
> **English edition.** The Russian version is the original — if the two disagree, Russian wins.

**Theme of this pack:** fix what's already broken, and close the networking gap — the one you identified yourself.

This is the first batch, not the whole roadmap. The next one arrives in two weeks and is built from what you send in your report.

---

## Why this, and not something else

You said the important thing in our session: you need to understand why each specific action matters. So every task below has a **Why** block. If it doesn't convince you, say so directly — that's a legitimate question, not fussiness.

The logic of the whole pack:

1. **You already have a stand** — VM, Docker Compose, Nginx, Grafana, Loki. That isn't nothing, it's a foundation. Building something new from scratch right now would be waste. We're finishing what exists.
2. **You already have something broken** — GitLab and the runner won't connect. That isn't a failure, it's a gift: a real production problem you arranged for yourself.
3. **You diagnosed it yourself** — "I'm short on networking skills." The diagnosis is correct. So networking comes first, but not as separate dull theory — directly underneath this breakage.
4. And separately, the thing that came out of the session as most painful: **you knew the material and couldn't explain it.** That is the cheapest thing here to fix, and we start fixing it now, not "when you're ready".

**Not in this pack, don't touch:** Kubernetes, Terraform, Ansible, clouds, certifications, Go. All of it is coming. Not now. Reach for it and you'll scatter and close nothing.

---

## How this fits your schedule

You don't have a "week", you have a shift cycle. Planning in hours-per-week is meaningless, so tasks are sorted by slot type:

| Slot | What it is | How much | What goes there |
|---|---|---|---|
| **A — large** | Day off after day shifts (two of them) | 4–5 h | Real work: debugging, building, configuring |
| **B — recovery day (отсыпной)** | After night shifts | **0 h** | Nothing. At all. See below |
| **C — small** | Day off after the recovery day | 2 h | Reading, notes, narration, the report |
| **D — night shift** | If you're working from home and it's quiet | 1–1.5 h | Light only: reading, video, flashcards. **No debugging** |

**About the recovery day — separately, and seriously.** You said it yourself: afterwards you're a vegetable. So it isn't in the plan. This isn't leniency, it's an engineering decision: schedule work into a day you won't work, and what you get isn't work — it's guilt, and you'll drop the whole plan two weeks in. The recovery day is officially struck out.

**About night shifts.** You mentioned that nights from home can get dull and there's time. That's your hidden reserve — but light tasks only. Debugging a network at 4 a.m. after eight hours on shift is a way to lose three hours and your confidence.

### Volume

- **Core (required):** ~20–24 hours across two weeks. This is what should get done.
- **Stretch (if you have it in you):** +10–12 hours. Marked **[+]**.

If the cycle falls apart — work, health, animals, life — there's a **minimum**: tasks **2.1, 2.2 and 3.1**. Do only those and don't count the pack as failed. That isn't consolation, it's prioritisation: they're the most valuable.

---

# TRACK 1 — FOUNDATION: networking, under a specific breakage

## 1.1 Draw a map of your stand — before fixing anything

Slot: **A** · ~1.5 h

Take your stand and draw the diagram: which containers exist, which docker networks they're on, which ports are published externally, which are internal only, who talks to whom and at what address. Nginx, Grafana, Loki, the database, GitLab, the runner — all of them.

Draw it with anything: Excalidraw, draw.io, pencil on paper photographed. What matters isn't the picture quality, it's that you reconstructed this yourself rather than from memory and a vague sense that "it all works".

**Why.** Three reasons, all real:

1. You can't fix connectivity you can't see. You'll most likely find the bug during the drawing itself — this happens more often than you'd think.
2. This diagram is the first exhibit in your portfolio. When an interviewer says "tell me about your project", you show a diagram instead of reciting from memory. Half of your interview failure was having nothing to lean on.
3. Being able to draw the system you operate is exactly what separates an engineer from someone who followed a guide.

**Done when:** the diagram is in the project repository, and it answers "how does Grafana reach Loki?" in under a minute.

---

## 1.2 Docker networking — narrowly

Slot: **A** or **D** · ~2 h

Work through exactly this list, no wider:

- Default `bridge` vs a user-defined bridge network vs `host` — and how they actually differ
- Why containers on a user-defined network find each other **by service name**, and don't on the default one
- `ports:` vs `expose:` in Compose — what is published externally and what isn't
- Why `localhost` inside a container is NOT your machine and not another container
- How to see which networks a container is on: `docker network ls`, `docker network inspect`, `docker inspect`

Verify everything by hand on your own stand, not on examples from an article. Get inside the containers (`docker exec -it ... sh`) and ping neighbours by name and by IP.

**Why.** There's roughly an eighty percent chance your GitLab and runner failed to connect exactly here: they were brought up separately, so they're almost certainly on different networks, and the runner is reaching for an address that doesn't exist from where it's standing. It's the most common mistake there is, and it needs to be *touched* once rather than read about — after that it never eats another evening.

**Done when:** you can point at your 1.1 diagram and say why a specific container can or can't see another.

---

## 1.3 How a request actually travels: TCP and diagnostics

Slot: **A** · ~2 h

Don't read the theory separately. Do this instead: take one real request on your stand (say browser → Nginx → Grafana) and trace it with tools.

- `curl -v` — read the output in full, line by line: what `* Connected to` means, where the handshake ends, where the headers begin
- `ss -tulpn` — who is listening on which port, on which interface (`0.0.0.0` vs `127.0.0.1` — an important difference, work it out)
- `dig` / `nslookup` — how a name resolves, and how that works inside a docker network
- `tcpdump -i any port 3000 -nn` — see SYN → SYN-ACK → ACK with your own eyes. Watching the handshake live once is worth three articles about it
- `ip route`, `ip addr` — where traffic actually goes

**Why.** You've already been asked about the TCP handshake in an interview. A recital of a diagram from an article is audible within a second, and it sounds bad. "I watched it in tcpdump on my own stand, here's what it looked like" sounds entirely different, because it's true. Beyond that: without `ss` and `tcpdump` you will never debug CI/CD, or Kubernetes, ever.

**Done when:** you have your own `network-cheatsheet.md` — commands **you ran yourself**, with sample output and notes on what each line means. Not copied from someone else's cheat sheet.

**[+] Stretch:** work out why `127.0.0.1` and `0.0.0.0` in `ports:` behave differently from outside the VM, and what that means for security.

---

# TRACK 2 — PRACTICE: fix GitLab + runner, build the first pipeline

This is the main work of the pack.

## 2.1 Diagnose the breakage — with your reasoning written down

Slot: **A** · ~2–3 h · **PART OF THE MINIMUM**

Don't fix it immediately. Investigate first, and write as you go into `debug-gitlab-runner.md`:

```
Hypothesis 1: the runner can't resolve the name "gitlab"
  How I checked: docker exec runner ping gitlab
  Result:        ...
  Conclusion:    confirmed / ruled out

Hypothesis 2: ...
```

Worth checking (not exhaustive — think for yourself):

- Are GitLab and the runner on the same docker network
- What URL is the runner using to reach GitLab, and is that URL reachable **from inside the runner container**
- What's in the logs: `docker logs` for both, `gitlab-runner verify`
- Did registration actually complete, and is the runner visible in the GitLab UI (Admin → Runners)
- Is GitLab's `external_url` the problem — it's often set so that it works from outside but not from inside the network

**Why.** There are two outcomes here and the second matters more. The first is a working runner. The second is a document showing that you **think in hypotheses** rather than poking at random. SRE/DevOps interviews test exactly this: they hand you a broken system and watch not whether you know the answer, but how you narrow the search. A file like this is rare in a junior portfolio, and it works harder than another green dashboard.

Plus, personally: it's practice at **articulating what you're doing**. The thing that fell apart in your interview.

**Done when:** the file exists and shows at least 3–4 tested hypotheses, including the ones that were ruled out. Don't delete those — they're the most valuable part.

---

## 2.2 Fix it

Slot: **A** · ~1–2 h · **PART OF THE MINIMUM**

Runner registered, visible in GitLab, picking up jobs. Write the simplest possible `.gitlab-ci.yml` with one job that does `echo "hello"` and get it to a green run.

**Why.** "Hello world" isn't a toy here: it separates a connectivity problem from a build problem. When the image build fails tomorrow, you'll know for certain that the runner↔GitLab channel works, and you won't be searching in two places at once. That is the skill — cutting the problem in half.

**Done when:** green pipeline in the UI. Screenshot in the report.

---

## 2.3 First meaningful pipeline: build an image

Slot: **A** · ~3 h

Have the pipeline build a Docker image of one of your services and push it to the GitLab Container Registry. Stages: `build` → `push`. Tag by commit SHA, not `latest`.

**Why.** This is literally what you'll be doing in your first month on the job. And "walk me through how delivery works at your place" is an all but guaranteed interview question. On the tag: `latest` in a deployment is a classic junior mistake, and interviewers latch onto it, because it reveals whether you understand reproducibility. You'll be able to explain why yours isn't `latest` — and that counts in your favour.

**Done when:** the image appears in the registry after a push to a branch.

**[+] Stretch:** add a `lint` stage (hadolint for the Dockerfile) before the build. You'll also find out what's wrong with your Dockerfile.

---

## 2.4 [+] Auto-deploy to the stand

Slot: **A** · ~2–3 h · stretch

A `deploy` stage: the pipeline updates the container on your VM with the freshly built image. Over SSH is fine for a first pass, nothing shameful about it.

**Why.** It closes the loop: code → build → delivery → running. From that moment you don't have a "stand", you have a small real system with automated delivery, and you can talk about it in an entirely different tone. If you don't get to it, we move it — it's stretch, nothing lost.

---

## 2.5 Describe the project in a README

Slot: **C** · ~1.5 h

In the repository README: what this system is, the diagram from 1.1, what it's made of, how to bring it up, what you were solving and why this way, what you'd do differently.

**Why.** In two months you'll have forgotten half the details — and you'll flounder through your own project in an interview, as has already happened. The README is your notes to your future self. It's also the first thing a recruiter or a team lead opens, if they open anything.

---

# TRACK 3 — CAREER: the thing that failed in the interview

This track takes under two hours across two weeks and will probably out-return everything else. Don't skip it.

## 3.1 Narrate the project aloud — 4 times this pack

Slot: **C** or **D** · 15 min each, 4 times · **PART OF THE MINIMUM**

Put your phone on record and, **aloud, with no notes, for 3 minutes**, describe your project: what it is, why, what it's made of, what was hard. Then listen to yourself. Yes, it's unpleasant. The first one will be bad. The fourth will be noticeably better.

A different angle each time:

1. Simply what I built
2. What broke and how I fixed it (after 2.1 you'll have something to tell)
3. Why I made these decisions rather than others
4. Everything together, whole, in 3 minutes

**Why.** You said it yourself: "I forgot even what I knew, because I was nervous." That isn't a knowledge problem — it's the absence of a rehearsed route. Under stress the brain doesn't assemble a narrative from scratch, it replays a worn path. The only way to wear a path is repetition aloud. Same principle as "know it at 200% to deliver 100%": the account has to be so well-worn that nerves can't knock it over.

This is the cheapest and highest-yielding task in the whole pack. Fifteen minutes against hours of Terraform.

**Done when:** 4 recordings made. You don't have to send them if you don't want to. One line in the report: what changed between the first and the fourth.

---

## 3.2 Find a community and sign up for one event

Slot: **C** or **D** · ~40 min

Find something in Kazakhstan (Astana/Almaty; online counts): DevOps Days, Kubernetes meetups, local IT Telegram chats, communities at universities and companies. Join at least two chats. If there's an event in the next month, register.

**Why.** Cold applications almost never get a junior with no commercial experience through right now — that isn't pessimism, it's what the market looks like. The real way in is through people. The interview you already had came via someone you knew; that isn't luck, that's the mechanism working. You have to start now, because connections don't convert instantly — they need time to settle.

You don't need to do anything in those chats yet. Just be there and read.

**Done when:** 2 community links in the report, plus one event with a date if you found one.

---

## 3.3 Five lines for your CV

Slot: **C** or **D** · ~40 min

Describe your project in five bullets, each in the form "what I did → what resulted". Don't embellish — but don't undersell either. "Set up a VM" is underselling. "Deployed monitoring infrastructure across 4 services with centralised log collection" is the same event, told truthfully.

**Why.** You're most likely underrating what you've already done — that was visible in the session. At the same time, lying is categorically out: invented experience collapses at the first follow-up question, and that ends the conversation. The task is learning to call real things by their correct names. That's a separate skill, and it's trainable.

**Done when:** 5 bullets in the report. I'll go through them.

---

# TRACK 4 — TOOLING: the agentic harness

A small block, but it makes everything after it faster.

## 4.1 Install Claude Code and point it at your repository

Slot: **A** or **D** · ~1.5 h

You said you use Claude and ChatGPT in chat form. A harness is different: the agent sees your files, runs commands on your own machine, and works in a loop rather than answering in a single reply.

Install Claude Code, open it in your project folder, and give it a first task: **"read my docker-compose.yml and explain how the networks are set up here, and what might stop two containers from seeing each other."**

**Iron rule: verify every single claim it makes, by hand.** It says "the containers are on different networks" — go and check with `docker network inspect`. Doesn't match? Excellent, you found the agent's mistake rather than the other way round.

**Why.** Two reasons:

1. The difference between "a chat" and "an agent that can see the system" isn't convenience, it's orders of magnitude in speed. In your situation, where time is objectively short, it's the cheapest leverage available.
2. The verification rule isn't paranoia. The agent will write you a working config in a minute, and you'll end up with a working stand and **zero understanding**. Then you'll sit down to an interview and what already happened will happen again. So: the agent explains and shows you where to look; **you do it with your hands.** For these two weeks at minimum, strictly this way.

**Done when:** installed, run against your project, and one line in the report: what it got right and what it got wrong.

---

## 4.2 [+] Write it instructions for the project

Slot: **D** · ~40 min · stretch

Create a `CLAUDE.md` in the repository: what the project is, what it consists of, how it starts, any quirks. From then on the agent reads it itself on every run.

**Why.** The side effect matters more than the main one: to explain the system to an agent you first have to formulate it yourself. It's the same skill as 1.1 and 3.1 — being able to describe what you built. You're just training it again under a different pretext.

---

# The report

**When:** the evening of Monday 17 August (or your nearest normal day — tell me if it shifts).

**Format:** free-form. A diary is fine. But it should contain:

1. **What you did** — by task number
2. **What you didn't do and why** — honestly. "Didn't have the energy" is a valid answer, and more useful than silence: I'll adjust the load from it
3. **Where you got stuck** — with detail: what you did, what you expected, what you got
4. **Questions** — everything accumulated. Collect them in a file as you go rather than trying to recall them at the end
5. **How many hours it actually took** — by A/C/D slot. This is what makes the next batch realistic rather than invented

The next batch is built **from your report**. If the volume didn't work — say so, we'll cut it. If it was easy — we'll add. Both answers are correct.

---

## One last thing

The rule for these two weeks: **three tasks done and understood beats eight followed from a guide.**

If a task looks pointless, tell me. "Why am I doing this" is a legitimate question here, and without an answer to it you'll drop the plan, as has happened before. That isn't a whim, it's the condition for the plan working at all.

And: the recovery day — we don't work. That's part of the plan, not a departure from it.
