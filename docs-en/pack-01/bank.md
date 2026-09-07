# The question bank — for track 1

> **English edition.** The Russian version is the original — if the two disagree, Russian wins.

There is an open bank of interview questions — [devops-interview-questions](https://shapovalovdev.github.io/devops-interview-questions/): 307 questions across 19 themes. Below are seven. The other three hundred are not about you and not about these two weeks.

The rule is the same one as in [materials](materials.md): **try it on the stand first, read when you're stuck.** That's why almost everything here is marked "after": you open a question not to learn the answer but to check your own. An answer read in advance gives you the feeling of knowing without the knowing — and that's the first thing to fall apart in an interview.

The bank is in English. That isn't a separate task: you read the Docker documentation in English anyway.

Markers: 🟢 required — read only these and you still take most of the value · **before** — open before the task, it frames the problem · **after** — open afterwards, it checks you · ⏱ time.

> This does not replace [your own list of questions](questions.md). That one is what you will **say out loud**. This one is somebody else's phrasing of the same topics. They're useful precisely because they're somebody else's: an interviewer won't ask in your words.

---

## 1.1 · The map of your stand

- **[Trace traffic to a published container port](https://shapovalovdev.github.io/devops-interview-questions/questions/container-networking/published-port-traffic-path.html)** — 🟢 **before** · ⏱ 10 min. Five questions your diagram is obliged to answer: what is listening inside the container and on which address, what is published outwards, which network the container is attached to, where address translation happens, and what the host's filter blocks. Draw it so all five can be answered off the diagram, and half of tasks 1.2 and 1.3 is done in advance.

That's all the bank gives you for 1.1. Why — see "What the bank doesn't have" below.

---

## 1.2 · Docker networking

- **[Trace a DNS lookup from an application to an answer](https://shapovalovdev.github.io/devops-interview-questions/questions/networking/dns-resolution-path.html)** — 🟢 **after** · ⏱ 10 min. Addressing a container by service name on a user-defined network is Docker's embedded DNS, and this question breaks down what resolution consists of at all: local cache, resolver configuration, recursive resolver, TTL. The part that matters most for you is the last point: a successful lookup does not prove there's a route to the address or that anything is listening there. That is the exact spot where you'll declare the runner fixed too early.
- **[Use private IPv4 address space safely](https://shapovalovdev.github.io/devops-interview-questions/questions/networking/private-address-space.html)** — **after** · ⏱ 5 min. Open it straight after your first `docker network inspect`: the `172.18.0.0/16` in the `Subnet` field is RFC 1918, and Docker hands out blocks like that itself, one per compose project. It also explains why overlapping ranges break connectivity for real, not in theory.

---

## 1.3 · How a request actually travels

- **[Explain ports and sockets](https://shapovalovdev.github.io/devops-interview-questions/questions/networking/ports-and-sockets.html)** — 🟢 **before** · ⏱ 10 min. The one deliberate exception to "hands first": `ss -tulpn` output is unreadable until you know that a listening socket and an established connection are different things, and that the bind address decides who can reach you at all. Ten minutes beforehand save you half a slot A.
- **[Diagnose a failed TCP three-way handshake](https://shapovalovdev.github.io/devops-interview-questions/questions/networking/tcp-three-way-handshake.html)** — 🟢 **after** · ⏱ 10 min. You've already been asked about the handshake — it's the case where you knew it and couldn't tell it. Here it isn't a diagram of three arrows but a diagnosis: SYN → RST means one thing, SYN → silence another, a SYN-ACK that is never acknowledged a third. Read it strictly **after** tcpdump: then every branch has your own capture from your own stand behind it, not somebody else's illustration.
- **[Map a request to network layers](https://shapovalovdev.github.io/devops-interview-questions/questions/networking/osi-and-tcp-ip-layers.html)** — **after** · ⏱ 10 min. It turns the five commands of task 1.3 into an order: start at the lowest layer that could plausibly have failed. That's the same discipline as 2.1 — narrow the search rather than poke at it. It also disposes of "ping works, so the network is fine".
- **[Debug a 502 response from a reverse proxy](https://shapovalovdev.github.io/devops-interview-questions/questions/web-servers/reverse-proxy-502-debugging.html)** — **after** · ⏱ 5 min. Your path exactly: browser → Nginx → Grafana. The question is short and the answer is four bullets — but it is the only place in the bank about "the proxy is alive and there's nothing behind it". You'll meet it the first time you move Grafana onto another network.

---

## 1.3s · [+] `127.0.0.1` vs `0.0.0.0` in `ports:`

There is no separate question for this. Re-read the last point of **[Explain ports and sockets](https://shapovalovdev.github.io/devops-interview-questions/questions/networking/ports-and-sockets.html)** — on binding to `127.0.0.1`, `0.0.0.0`, `::1`, `::`. That's the answer to the task in one line; everything else is your experiment: publish the same port both ways and knock on it from outside the VM.

The bank does not cover the security half of the stretch — everything it has is network segmentation at organisation scale. That's a year out.

---

## What the bank doesn't have

Five things track 1 needs and the bank doesn't give. This isn't a complaint about the bank — it's about interviews, not about your stand. But knowing where it goes quiet is more useful than assuming a topic is covered.

1. **Docker network drivers.** Not one question on the default bridge vs a user-defined one vs `host`, and not one on why name resolution works on one and not the other. That is the core of task 1.2 — and it simply isn't in the bank. Covered instead by the Docker documentation in [materials](materials.md), section 1.
2. **Compose.** `ports:` vs `expose:`, the `networks:` section, `external: true` — zero questions in the entire bank. Which is to say: exactly the topic that most likely kept GitLab and the runner from connecting.
3. **`localhost` inside a container.** Nothing on network namespaces. The nearest thing is a question about PID namespaces, which is something else.
4. **Reading tool output.** The bank says "inspect socket state", "take a capture" — but nowhere shows the output of `curl -v`, `ss`, `tcpdump`, `ip route`, or asks you to go through it line by line. Your `network-cheatsheet.md` from 1.3 has to be built from scratch; the bank has no model for it.
5. **Describing the system you operate.** Task 1.1 in its entirety. Not one question — even though that is precisely what interviewers ask.

Separately, for later: the `ci-cd` section holds twenty-five questions and not one about a runner that can't reach its coordinator. The bank is just as quiet for track 2.

---

## What was deliberately left out

So you don't go looking and lose an evening to it:

- **Everything marked senior and staff in the `networking` section** — ten questions out of twenty-five: BGP, multi-region, capacity models, change management, egress governance. Written for someone who owns an organisation's network. Not your class of problem, and it won't become one during this pack.
- **The TLS handshake** — useful once you put a certificate on the stand. Right now `curl -v` to Grafana won't show you one.
- **NAT, route asymmetry, path MTU, CIDR arithmetic** — real topics, but on a single VM with two bridge networks `ip route` is trivial, and there's nowhere to reproduce MTU problems or asymmetry. We'll come back when there's a second machine.
- **Kubernetes, cloud, Terraform** — by the rule of the pack. That's almost a quarter of the bank; don't go in there.

---

## How to fit it into your slots

⏱ About an hour for all seven. This is reading, not work: slot **D**, or the tail of slot **C**. Don't put any of it in slot **A** — A goes to the stand. The only two that open **before** a task are short ones: you'll fit them in around the edges.

Once you've closed a topic on the stand, run the questions on it out loud — first from [your own list](questions.md), then these. That order specifically: your own phrasing you should be able to produce freely, somebody else's you only need to recognise.
