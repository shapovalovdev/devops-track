# Self-check rubric — pack 01

> **English edition.** The Russian version is the original — if the two disagree, Russian wins.

After each task, ask yourself these questions **out loud**, not in your head. Out loud, because a thought you can't say coherently isn't finished being thought. And it's interview practice, just free.

How to read the rubric: **an answer of "broadly yes" means "no"**. If you find yourself softening the wording, the task isn't closed — and that's a normal intermediate result, not a failure. Note it in the report.

---

## General block — after any task

Four questions, the same four every time:

1. **What here works differently from how I expected?** If the answer is "it all went as expected", I probably wasn't testing, I was confirming.
2. **What can I explain now that I couldn't two weeks ago?** In one sentence, using no terms I can't unpack myself.
3. **What would break if I'd done it the other way round?** If I don't know, I know a recipe, not a mechanism.
4. **What did I do with my hands, and what did an agent or a guide do for me?** Honestly. Nothing gets punished for this, but it decides what I can actually do.

---

## 1.1 Stand diagram

- Can I use my own diagram to answer, in under a minute, how Grafana reaches Loki — by name or by IP, on which network, through which port?
- What on the diagram turned out **not** to be what I thought before I drew it?
- Which arrows did I draw from memory, and which did I check with a command? How many of the first kind turned out to be right?
- If I take one network away, which connections break? Can I name them all?

**Red flag:** the diagram matched my expectations completely. That means I drew it from the compose file, not from the system.

---

## 1.2 Docker networking

- Can I explain **why** name resolution works on a user-defined network and doesn't on the default one? Not "that's how it's built", but what exactly is doing the resolving.
- `localhost` inside a container — what is it? Can I describe it rather than quote the rule?
- The difference between `ports:` and `expose:` — which of the two actually opens access from outside the VM?
- Take any container of mine: can I say straight off which networks it's on, and check that with one command?
- If two containers can't see each other — which three things do I check, and in what order?

**Red flag:** I know the driver names but can't point at my own stand and say which is which.

---

## 1.3 TCP and diagnostics

- In `curl -v` output — where does setting up the connection end and HTTP begin? Can I point at the exact line?
- `0.0.0.0` and `127.0.0.1` in `ss -tulpn` output — what's the practical difference? Which of them is reachable from my laptop?
- Did I **see** SYN → SYN-ACK → ACK with my own eyes, or did I read about them?
- A connection won't establish. Can I tell from tcpdump the difference between "it never reached me", "it arrived and was refused", and "it arrived but the reply never came back"?
- Are there lines of output in my cheat sheet that I **didn't understand**? Are they written out separately?

**Red flag:** the cheat sheet is nothing but commands, with no output. That's someone else's cheat sheet, even if I typed it myself.

---

## 2.1 Diagnosing the breakage

The main task of the pack — so the rubric is longer.

- Did each next hypothesis **follow** from the result of the last one, or was I checking everything at random?
- How many hypotheses were ruled out? If it's zero, I wrote the log after I'd fixed it.
- For each check: did I know **which result would disprove** the hypothesis before I ran the command?
- Which check gave me the most information? Why didn't I start with it?
- Can I retell the whole investigation in two minutes without opening the file?
- If the same thing broke somewhere else tomorrow, would my log help?

**Red flag:** the log reads like a success story. Real debugging looks like several dead ends and one guess.

---

## 2.2 The fix

- Can I state the root cause **in one sentence**, without the log open?
- Why it broke in the first place — did I understand that, or did I just reconfigure it?
- Could I break it again **on purpose**? If not, I didn't understand the cause.
- What did I change that didn't need changing?

**Red flag:** I fixed it by recreating everything from scratch. Working — yes. Learned something — no.

---

## 2.3 Pipeline: building the image

- Why tag by commit SHA and not `latest`? Can I explain it through "here's what happens if" rather than "that's the right way"?
- What exactly happens between `git push` and the image appearing in the registry? Can I list the steps in order?
- Where does the runner live, where is the image built, where does it go — in networks and hosts, not in the abstract?
- If the pipeline fails at `push` — where do I go looking for the cause first?
- Can I explain this `.gitlab-ci.yml` line by line? **Every** line?

**Red flag:** there are lines I'd describe as "that came from the example". Work them out or delete them.

---

## 2.4 [+] Auto-deploy

- What happens if the deploy fails halfway? What state does the service end up in?
- How do I roll back to the previous version? Have I tested that, or am I assuming?
- What's wrong with my SSH deploy — can I name two specific weaknesses? (This is exactly the question they'll ask in an interview.)

---

## 2.5 README

- Could someone who doesn't know me bring the system up from this README, without me?
- The "what I'd do differently" section — is there anything real in it, or just words?
- In two months, will I work out from it myself what I did and why?

---

## 3.1 Narrating aloud

After **every** recording, before listening back and after:

- Where did I stop to remember something? What was I remembering — a fact or a phrasing?
- How many times did I say "um", "sort of", "basically"?
- Was I explaining the system, or listing technologies? A list of tools isn't a story.
- Did I say **why** I built it, or only what it is?
- Between recording 1 and recording 4: what changed, specifically? Not "it got better" — what exactly.

**Red flag:** I can't listen to my own recording. That's a normal reaction, and it's exactly the discomfort the task exists for. Listen anyway.

---

## 3.3 Five lines for your CV

Each bullet separately:

- Is this **true**? Fully, with no "almost"?
- If they say "tell me more about this one" — do I have three minutes of substance?
- Did I give the scale — how many services, how much data, how long it's been running?
- Did I undersell it? "Set up a VM" and "deployed monitoring infrastructure across 4 services" are the same event.

**Red flag:** a bullet I couldn't defend against one follow-up question. Cross it out, don't deliberate.

---

## 4.1 The agent

- Did I **verify** every claim it made, or take on trust whatever sounded confident?
- Did it get anything wrong at all? If it didn't, I probably wasn't checking, I was matching it against a feeling.
- What did I do faster with it? What did it stop me from **understanding**?
- If the agent went offline today — which of the things I did could I not repeat on my own?

**Red flag:** the answer to that last question isn't "nothing". Then part of the work needs doing again by hand — not on principle, but because that's exactly what they'll ask about in the interview.

---

## Stand rubric — after any work on the system

Applies in this pack and every one after it. Five questions:

1. **What changed in the system, and is it written down anywhere?** A change that isn't in git doesn't exist — in a week I'll have forgotten it.
2. **How will I find out it broke?** If the answer is "I'll log in and look", there's no observability.
3. **How do I roll it back?** Have I tested that, or do I just think I can?
4. **What now depends on what I've just done?** Which other parts of the system might I have touched?
5. **If this were the job and a senior engineer were sitting next to me — what would they ask first?**

---

## The pack's closing question — 17 August, before the report

One sentence, out loud, no notes:

> **What can I do now that I couldn't do on 4 August?**

If the answer comes out as a list of topics, that's the wrong answer. It should come out as a description of an ability: "I can work out why two containers can't see each other, and explain it in words."
