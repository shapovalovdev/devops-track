# Interview Questions — Pack 02

Questions asked during Junior+/Middle DevOps/SRE technical screenings.

---

## Docker and Containerization
1. How do multi-stage builds work in Docker, and what security and operational problems do they resolve?
2. What is the difference between `COPY` and `ADD` instructions in a Dockerfile?
3. What is the role of PID 1 in a Linux container namespace? Why must PID 1 handle `SIGTERM` signals properly, and what is a zombie process?
4. How do `CMD` and `ENTRYPOINT` interact in Docker?
5. How does the `HEALTHCHECK` directive operate, and what states (`starting`, `healthy`, `unhealthy`) does Docker report?

---

## CI/CD and Production Operations
6. Why is using the `:latest` Docker tag in deployment pipelines considered an antipattern?
7. How do you securely handle SSH private keys and database credentials in GitLab CI? What do Protected and Masked flags do?
8. How do you architect a deterministic, sub-minute rollback procedure for containerized microservices?
9. What are the four core DORA metrics (Deployment Frequency, Lead Time, Change Failure Rate, MTTR), and how do you improve them?
10. What is immutable infrastructure, and why are direct manual edits on production servers strictly prohibited?

---

## Networking and Reverse Proxies
11. What is a Reverse Proxy (such as Nginx), and why is it deployed in front of application containers?
12. Why are the `Host`, `X-Real-IP`, `X-Forwarded-For`, and `X-Forwarded-Proto` headers necessary in Nginx configurations?
13. Describe the TCP three-way handshake (SYN -> SYN-ACK -> ACK). What happens when a port is closed and returns a packet with the `RST` flag?
14. Which command in Linux allows instant inspection of listening sockets and their corresponding process PIDs (`ss -tulpn`)?
15. What is the difference between `SIGKILL` and `SIGTERM` signals when stopping a container?
