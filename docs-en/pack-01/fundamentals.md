# Why it all works this way — the reasoning under pack 01

> **English edition.** The Russian version is the original — if the two disagree, Russian wins.

The theory list answers the question "what will I know". This file answers a different one: **why the industry arrived at these solutions and not others.**

This isn't extra reading for the curious. The difference between a junior and an engineer in an interview sits exactly here. A junior explains **how** to configure it; an engineer explains **what problem** it solves and what happens if you do it differently. The first you can google in a minute; the second you can't.

Read it once, end to end, ideally in slot **C** or **D**, before you start work. Then come back to it whenever a task looks pointless.

---

# Part 1 · Networking: why it's like this

## Why the network is split into layers

Data going out onto the network gets wrapped in several layers of protocol. A packet is born, the first protocol wraps it in its own header, the next wraps that whole thing, then the next. On the receiving side it's unwrapped in reverse order: the hardware strips Ethernet, the kernel strips IP and TCP, the application gets the data.

**Why the nesting.** No layer knows, or wants to know, what's inside its neighbour. So a layer can be replaced without touching the others: the same code runs over Ethernet, over Wi-Fi and over fibre, because the layers below deal with that. You don't rewrite the application when the physical medium changes.

**What this gets you in practice.** Debugging becomes **layer by layer**. Not "the network is broken" — but a question of which layer it breaks at. Ping works, the port won't open — the problem is above IP. The port is listening, the application doesn't answer — the problem is above TCP. That turns an unbounded "something isn't working" into four or five statements you check one at a time.

📖 [Beej's Guide to Network Concepts — layered network model](https://beej.us/guide/bgnet0/html/split/the-layered-network-model.html)

## Why the handshake is three packets and not two

You'll be asked this almost every time. The right answer isn't which flags come in which order, it's **what the two sides are working out**.

Each side needs to be sure of two things: that it is heard, and that it can hear. Two packets are enough for the **initiator** to know that: it sent, it got a reply — so the channel works both ways. But after two packets the receiving side only knows that something reached it. It doesn't know whether its reply got back. The third packet closes exactly that.

On top of that, both sides agree on initial sequence numbers — without them there's nothing to order the bytes by and nothing to acknowledge.

**The practical consequence, and the reason this is worth understanding.** Where the handshake breaks tells you what's broken:

| What you see | What it means |
|---|---|
| SYN went out, nothing came back | The packet didn't arrive, or the reply didn't come back. Firewall, route, wrong network |
| SYN → RST | It arrived, but there's nobody to accept it. Port closed, process not listening, or listening on a different interface |
| SYN → SYN-ACK → ACK, then silence | The connection is up, the problem is **above** TCP. The application is alive but not answering |

That's the reason task 1.3 exists. Not "have a look at a handshake", but to get hold of a tool that halves the search space with one command.

## Why a container has its own localhost

A container isn't a small virtual machine, it's an ordinary process on your host that the kernel handed an isolated set of resources. One of them is a **network namespace**: its own network interfaces, its own routing table, its own `127.0.0.1`.

Everything else follows from that, including almost everything counterintuitive:

- `localhost` inside a container is **the container itself**. Not the host, not a neighbour. A database on `localhost:5432` isn't visible from the application container, because those are two different `localhost`s.
- Ports don't clash between containers — each one has its own set.
- To reach it from outside you have to **publish the port**: an explicit forward through NAT on the host. Without it everything works from inside and nothing from outside.

**Why have this isolation at all.** So that two services, each of which wants port 8080, can run on one machine without negotiating with each other. The price is having to state explicitly what's open to the outside. That price is the source of most "works on my machine" errors.

## Why you address things by name, not by IP

On a user-defined bridge network Docker runs a built-in DNS on `127.0.0.11`, and containers find each other by service name. The default network has none of that — IP only.

**Why by name is better.** A container's IP is handed out at start and changes when it's recreated. A config with a hardcoded IP breaks at the first `docker compose up --force-recreate`. A name is a layer of indirection: the address is resolved at the moment you use it, not at the moment you wrote the config.

It's the same principle you'll meet later in Kubernetes (Service instead of Pod IP) and in load balancers. Understanding it once here, on two containers, is cheaper than understanding it later on a cluster.

**And this is most likely your breakage.** GitLab and the runner were brought up separately → almost certainly on different networks → the runner is going to an address that doesn't exist from where it stands.

📖 [Docker: bridge network driver](https://docs.docker.com/engine/network/drivers/bridge/)

## The four points of failure

Any connectivity problem comes down to one of four:

1. **Went to the wrong place** — wrong address, wrong port, wrong network, wrong route
2. **Didn't arrive** — firewall, missing route, different networks
3. **Nobody to accept it** — the process isn't listening, is listening on `127.0.0.1` instead of `0.0.0.0`, or has died
4. **The reply didn't come back** — asymmetric route, NAT, reverse firewall rule

The value of the model is that each check should **eliminate** one or two options rather than confirm one. `ss -tulpn` closes the third. `tcpdump` on the receiving side separates the second from the fourth. `curl` from inside the container closes the first.

And that's the skeleton of your `debug-gitlab-runner.md`: the hypotheses aren't random, they follow these four.

---

# Part 2 · CI/CD: why pipelines look like this

## The problem CI solves is called "integration hell"

Before CI, developers worked for weeks each in their own branch. Merging got put off, because merging hurt. The longer it was put off, the wider the divergence, the more painful the merge, the stronger the urge to put it off again. Projects got stuck in the integration phase for weeks, and nobody could say how long it would last.

The essence of continuous integration is that **every member of the team integrates frequently, at least daily, into a shared controlled repository**. Every commit is verified in a reference environment by a service that watches the main branch: on each commit it takes the current state and does a full build. Integration only counts as finished after a successful build.

**The key thought, worth being able to say out loud:** CI isn't about the tool. It's a practice — integrating often. The server only makes the practice feasible. A team with GitLab CI and three-week branches **does not have** continuous integration. That answer in an interview separates you immediately from the people who read the definition.

📖 [Martin Fowler — Continuous Integration](https://martinfowler.com/articles/continuousIntegration.html) · [Deployment Pipeline](https://www.martinfowler.com/bliki/DeploymentPipeline.html)

## Why the build runs on someone else's machine and not on yours

It looks like unnecessary complication: everything already builds locally. What's the runner for?

**Because "works on my machine" isn't a fact, it's a coincidence.** Your machine has accumulated things: installed packages, environment variables, caches, a runtime version, files you forgot to commit. Building on a clean machine out of what's in the repository is the only way to find out whether the repository is **complete**.

Which gives you a direct consequence for debugging: if the pipeline fails and it builds locally, then almost always something exists on your machine and not in the repository. That's the first hypothesis, not the last.

## Why the runner is a separate thing, and why that's your breakage

GitLab stores the code and decides what needs to be executed. The runner is a separate process that picks that work up and does it. It lives anywhere: on the same machine, on a different one, in a different data centre.

The split gives you scaling (many runners against one GitLab), isolation (a build doesn't take down the main service) and specialisation (different runners for different hardware).

**The price of the split is a network dependency.** The runner has to reach GitLab, and the build container has to reach GitLab **and** everything the build needs. That architectural decision, all by itself, produces the class of error you've landed in: an address that works from the browser and doesn't work from inside a container, because those are different network contexts.

The GitLab documentation describes this case directly: Docker containers can fail to reach GitLab even when the runner daemon itself has access — because DNS is configured on the host, for instance, and isn't passed into the container.

📖 [GitLab Runner troubleshooting](https://docs.gitlab.com/runner/faq/) · [Docker executor](https://docs.gitlab.com/runner/executors/docker/)

## Why you build once and promote it onward — "build once, deploy many"

**The central principle of the whole of delivery.** The artefact (for you, the image) is built **once**, versioned, put into storage, and after that **never rebuilt** — it's promoted through environments unchanged. To test, then to staging, then to prod. The only thing that changes is the environment it runs in; promotion moves a label, it doesn't produce a new build.

**The anti-pattern that looks perfectly natural:** building a separate artefact for each environment. Then what ends up in prod is something nobody ever tested — they tested something similar, built separately. And the difference surfaces at the least convenient moment.

Three things an immutable artefact gives you:

- **No configuration drift.** No half-applied rollouts, no "that server is on a different version".
- **Testing means something.** Tested once, deployed many times. Otherwise the check applies to a different object.
- **Traceability.** From a running container you can find, unambiguously, the commit it was built from.

📖 [MinimumCD — Immutable Artifact](https://minimumcd.org/minimumcd/immutable/) · [Home Office — immutable artefacts](https://engineering.homeoffice.gov.uk/patterns/immutable-artefacts/)

## Why you tag by commit SHA and not `latest`

A direct consequence of the previous point, not a separate rule of good manners.

`latest` isn't a version, it's a **moving pointer**. It points at whatever was pushed last. Which means:

- "We run `latest` in prod" doesn't answer the question of what is in prod.
- There's nowhere to roll back to: the previous image exists, but it has no name.
- Two servers started an hour apart can be running different versions with the same name.
- An incident can't be investigated: it's unclear which code was running when it broke.

Tagging by SHA gives you an unambiguous code ↔ image correspondence. The GitLab documentation says it outright: use the Git SHA in the tag and every job is unique, so there's never a stale image.

**How to phrase it in an interview** — through the consequence, not the rule:
> "`latest` is a moving pointer. I can't tell you what's actually running in prod, and I can't roll back to a specific version. Tagging by SHA ties the image to the commit, so from any running container I find the code in a second."

## Why a pipeline is split into stages

Stages aren't decoration. They order the checks on one principle: **fast and cheap before slow and expensive**.

The point is the cost of feedback. If a linter catches an error in 10 seconds and the build takes 6 minutes, the linter has to go first. Otherwise you wait six minutes for a failure that was knowable at the start.

Hence the usual order: `lint` → `build` → `test` → `push` → `deploy`. And hence the requirement that a stage fail honestly: a pipeline that "fails sometimes", and that everyone habitually restarts, stops being a source of information. A red nobody believes is worse than no red at all.

## Why you don't fix prod by hand

Rule 1 of the practice constitution, and here is what it rests on.

A manual change on a server **exists nowhere except that server**. It isn't in git, isn't in the history, isn't in the description of the system. From which it follows:

- The next rollout will wipe it — and bring back a bug that was "already fixed".
- Nobody, including you in a month, will know it's there.
- The incident investigation misses: reality differs from the description, and the difference is invisible.
- You can't rebuild the server from scratch — part of the state exists only in the head of whoever edited it.

That is exactly the difference between a system you can rebuild and a system people are afraid to touch. The second is called a snowflake server, and it's what any infrastructure edited by hand turns into.

**Why this matters more in the lab than at work.** At work you won't be handed prod — there are processes for that. Solo in your own lab, `ssh` and an edit in place is always faster, which is why the habit breaks down here fastest of all. The rule comes in at pack 03, and it holds not through willpower but because write access is taken away.

## How you measure whether delivery works

There's a research programme, DORA, that has spent years measuring what separates strong teams from weak ones. Out of it came **four key metrics**:

| Metric | What it measures | Group |
|---|---|---|
| Deployment frequency | How often things reach prod | throughput |
| Lead time from commit to prod | How long a change takes to get there | throughput |
| Change failure rate | What share of deploys break prod | stability |
| Time to restore | How long the recovery takes after an incident | stability |

**The counterintuitive result — and the best answer to a common interview question.** Intuition says speed and stability are opposites: the more often you deploy, the more often you break things. The data says the reverse — strong teams deploy more often **and** break things less.

The mechanics are simple. Frequent deploys mean small changes. A small change is easier to check, it has a smaller blast radius, it's faster to roll back, and when something breaks it's obvious what broke it. Rare deploys mean big batches of change, where an incident leaves you unable to tell which of forty changes is at fault.

By the 2024 report's benchmarks: the strongest teams deploy on demand, get a change to prod in under a day, and have a change failure rate of around 5%. The weakest spend between a month and six months on one change.

**Why this matters to you now, alone and with no prod.** Because it answers the question "what is the whole pipeline for, if I can deploy by hand in two minutes". The answer: the pipeline doesn't exist to automate two minutes, it exists so that changes are small, reversible and traceable. Which is also a ready-made answer to "how do you tell whether a delivery process is a good one".

📖 [Google Cloud — Four Keys](https://cloud.google.com/blog/products/devops-sre/using-the-four-keys-to-measure-your-devops-performance)

---

# Part 3 · How to use this in an interview

Three things that turn this file into a result.

**1. To any "how" question, add one "why" sentence.**
> "I tag by commit SHA." → "I tag by commit SHA so that from a running container I can find the commit, and so that I can roll back to a specific version."

The second version takes four seconds longer and sounds like a different level.

**2. Keep "and what if you did the opposite" ready.** For every practice in this file you should have an answer for what breaks without it. That's exactly how understanding gets tested — with "why not do it more simply".

**3. Don't pretend you did things you didn't.** "I know about build once, deploy many; on my own stand I still build and deploy straight into one environment — there simply isn't a second one" is a strong answer. It shows you understand the principle and that you describe the limits of your own use of it honestly. An attempt to act out experience falls apart at the first follow-up question.

---

## What to read in full, if it caught you

- **[Continuous Integration — Martin Fowler](https://martinfowler.com/articles/continuousIntegration.html)** — the primary source for the practice. Long, but it's the text everything else grew out of.
- **[Beej's Guide to Network Concepts](https://beej.us/guide/bgnet0/html/split/the-layered-network-model.html)** — networking from the very bottom, no prior knowledge assumed.
- **[MinimumCD](https://minimumcd.org/minimumcd/immutable/)** — the minimum set of things that have to be true before you can call it CD. Short and uncompromising.

Not now — in slot **D**, when you have nothing left for debugging but enough for reading.
