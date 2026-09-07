# Interview questions — pack 01 level

> **English edition.** The Russian version is the original — if the two disagree, Russian wins.

The list of what you'll be able to answer by **17 August**. Not "someday" — two weeks from now.

**How to use this.** Answer **out loud and with no preparation**, the way you would in an interview. In your head you can answer everything — that tests nothing. Keep this list open while you work on the stand: close a topic, run its questions straight away.

Markers: 🟢 required by 17 August · 🟡 you'll answer partially, that's fine · 🔴 you'll answer this after pack 02.

You've already heard some of these — you were asked about the TCP handshake. This time the answer comes out of your own practice, not out of an article.

> Answers to the questions that start with "why" don't come from documentation, they come from "Why it all works this way". That's the difference between "I set it up" and "I understand it": how takes a minute to google, why doesn't.

---

## 1 · Docker and networking

**🟢 Basics — these should come out on reflex**

1. What is a container? How is it different from a virtual machine?
2. What happens when you run `docker run`?
3. What network drivers does Docker have, and when do you need which?
4. Two containers on the same user-defined network. How does one reach the other?
5. Why doesn't the same thing work on the default bridge network?
6. What does the line `ports: "8080:80"` do in a compose file? Which number is which?
7. What's the difference between `ports:` and `expose:`?
8. An application inside a container listens on `127.0.0.1:5000`. Can you reach it from outside? Why?
9. How do you check which networks a container is on?

**🟢 Scenario questions — asked more often than the basics**

10. Two containers can't see each other. Walk me through your first three steps.
11. An application in a container can't connect to a database on `localhost:5432`. The database is running. What's going on?
12. A service works on your machine but isn't reachable from outside the server. Where do you look?
13. You brought up two compose projects separately, and services in one can't see the other. Why, and how do you fix it?
14. How do you lay out your networks when some services have to be reachable from outside and some only internally?

**🟡 Deeper — a partial answer is already good**

15. What does Docker do to the host's networking when it creates a bridge network?
16. What is a network namespace, and how does it relate to a container having its own `localhost`?
17. When does `network_mode: host` make sense? What do you give up?

---

## 2 · Networking and diagnostics

**🟢 Required**

18. Tell me about the TCP handshake. *(The answer should sound like this: "SYN, SYN-ACK, ACK — I watched it in tcpdump on my own stand, it looks like this." The difference between that and reciting an article is audible immediately.)*
19. Why three packets and not two?
20. How is TCP different from UDP, and where is each used?
21. What happens when you type an address into a browser? Step by step.
22. How do you check whether anything is listening on a port on a server?
23. You see `0.0.0.0:8080` and `127.0.0.1:8080` in the output. What's the practical difference?
24. What do you use to look at traffic?
25. How do you check that a name resolves? What will `dig` show you?

**🟢 Scenario questions — the main format for DevOps/SRE**

26. A connection isn't being established. How do you tell "the packet never arrived" from "it arrived and was refused"?
27. `curl` hangs and then times out. What do you check, and in what order?
28. A service is responding slowly. Where do you start?
29. It works by IP, it doesn't work by name. What does that mean?
30. One client connects, another doesn't. Hypotheses?

**🟡 Deeper**

31. What is MTU, and when does it become a problem?
32. What does `ip route` do, and how do you work out where a packet will go?
33. What is a SYN flood, and what does it look like in tcpdump?

---

## 3 · CI/CD

**🟢 Required**

34. What is CI/CD and what is it for? *(No generalities. Answer through "what it would be like without it".)*
35. How is a pipeline put together in GitLab: pipeline, stage, job?
36. What is a runner, and how does it relate to GitLab?
37. What is an executor, and which ones are there?
38. Walk me through your pipeline: what happens between `git push` and the result?
39. Why do you tag your image by commit SHA and not `latest`? *(Answer through the consequences, not through "that's the correct way".)*
40. What is a container registry?
41. How do secrets get into a pipeline? Why not into the repository?

**🟢 Scenario questions**

42. A pipeline failed. What do you do?
43. The runner isn't picking up jobs. Where do you look?
44. It works for everyone except one person. Hypotheses?
45. An image build takes 15 minutes. How do you speed it up? *(🟡 naming layers and cache is enough.)*
46. How do you roll back to the previous version if you deployed something broken?

**🔴 After pack 02**

47. What's worse about deploying over SSH than doing it properly? *(You'll answer this partially even now — and that's a good answer, because it's honest.)*
48. What are blue-green and canary deployments?

---

## 3½ · The "why" questions — the strongest block

Far fewer people can answer these than can answer "how". This is exactly where you hear the difference between someone who finished a course and someone who understands what they're doing. The answers come from "Why it all works this way".

**🟢**

- Why is networking split into layers? What does that buy you in practice?
- Why is the handshake three packets and not two? *(The answer isn't about flags, it's about what each side establishes.)*
- Why does a container have its own `localhost`? What is that isolation for in the first place?
- Why is addressing a service by name better than by IP?
- Why do I need a CI server if I already build locally?
- Why is the runner a separate thing rather than part of GitLab?
- What does "build once, deploy many times" mean, and what breaks if you build separately for each environment?
- Why can't you fix production by hand, if it's faster that way?
- Why is a pipeline split into stages? What order should they run in, and why?

**🟡**

- How do you tell that a delivery process is set up well? What do you measure? *(The four DORA metrics.)*
- Are frequent releases riskier or safer? Why? *(The answer is counterintuitive; if you can justify it, people notice.)*
- What is a snowflake server and what's wrong with it?

**A move that works on any of these.** Answer through "what breaks if you do the opposite". It's both a check that you understood and the most convincing shape an answer can take.

---

## 4 · Linux

Your strong side, out of support experience. Run through them so the wording is working wording.

**🟢**

49. You've run out of disk space. What do you do?
50. A process is eating CPU. How do you find which one?
51. How do you look at a service's logs? Where do they live?
52. Permissions `755` and `644` — what do they mean?
53. What is a systemd unit? How do you restart one and check its status?
54. What's the difference between `kill` and `kill -9`?

---

## 5 · About your project — the most important part

This is where you were failed last time. Not because you didn't know it, but because you couldn't tell it. These questions are what task 3.1 runs through — they are its content.

**🟢 Required**

55. **Tell me about your project.** *(3 minutes. The opening rehearsed word for word — the first twenty seconds decide it, because after that the nerves let go.)*
56. Why did you build it?
57. What's it made of, and why those components?
58. What was the hardest part?
59. **Tell me about a time something broke and you fixed it.** *(Your answer is the GitLab and runner story, out of `debug-gitlab-runner.md`. Structure: what broke → what you suspected → how you checked → what it turned out to be → what you changed so it wouldn't happen again.)*
60. What would you do differently if you started over?
61. What are you going to add next, and why that?
62. How do you find out your system has broken? *(🟡 the honest answer right now is "I look at Grafana by hand, there are no alerts yet, that's the next step". That's a fine answer. It shows you understand what's missing.)*

**🟢 About what you can't do yet — everyone gets asked these**

63. What don't you know that this position needs?
64. How do you learn? Give me an example from the last month.
65. Why are you leaving support for DevOps?
66. You have no commercial DevOps experience. Why should we hire you?

One rule for those four: **don't make excuses and don't make things up.** "I understand Kubernetes conceptually, I haven't worked with it hands-on, I start on it in November" sounds stronger than a vague "I'm somewhat familiar". Describing your own boundary precisely reads as maturity; trying to smudge it falls apart at the first follow-up question.

---

## 6 · What to ask them

A candidate's questions get scored. Having none reads as indifference, and two good ones pull up an average conversation.

**About the work**

- What does a normal day in this role look like?
- What would my first task be in the first month?
- Who decides to ship to production, and how does that happen?
- Is there an on-call rotation? How does it work?
- What breaks most often, and how do you find out about it?

**About growing**

- Who would be onboarding me?
- How do you tell here that a junior has grown?
- Is there a budget for training and certifications?

**About the honest picture**

- What part of your infrastructure do you consider tech debt yourselves?
- Why is this role open — is the team growing, or did someone leave?

One question has to be **about something specific they told you** — it shows you were listening rather than reading off something you prepared.

---

## How to drill this

1. **Don't read the answers in advance.** You get the feeling of knowing without the knowing — exactly what fell apart last time.
2. **Answer out loud and on the clock.** 🟢 — under two minutes. Over that, the answer isn't ready.
3. **Record yourself** on questions 55–62. That is task 3.1.
4. **Mark the failures** instead of skipping past them. A failed question is a pack 02 task.
5. Know a topic at 200% and you'll deliver 100%. **Know it at 100% and you'll deliver 30%,** because nerves eat the rest. So you always need the margin.

---

## The report, 17 August

One line:

> Ran ___ of 78 out loud. Answered ___ confidently. Failed: ___ (numbers).

Failures aren't a problem, they're input data. Pack 02 gets built out of them.
