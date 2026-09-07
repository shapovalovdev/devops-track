# Материалы к паку 01

Дополнение к задачам, а не замена. Правило на этот пак: **сначала попробовать на стенде, читать — когда упёрся.** Материал, прочитанный до того, как возникла проблема, забывается за неделю; тот же материал после двух часов тупика остаётся навсегда.

Каждый пункт помечен: 🅟 первоисточник (официальная документация — читать в первую очередь) · 🅢 объяснение (быстрее заходит, но проверяй по первоисточнику) · ⏱ примерное время.

> **Начинать не отсюда.** Сначала — [«Почему всё устроено именно так»](fundamentals.md): основания под сети и CI/CD, ⏱ 40 мин, слот C или D. Материалы ниже отвечают на вопрос «как», и без «почему» они превращаются в набор рецептов.

---

## 0 · Основания

- **[Continuous Integration — Martin Fowler](https://martinfowler.com/articles/continuousIntegration.html)** — 🅟 ⏱ 60 мин. Первоисточник практики: команда интегрируется в общую ветку минимум раз в день, каждый коммит проверяется полной сборкой в эталонном окружении. Всё, что делают CI-системы, выросло отсюда. Длинно — можно в два захода.
- **[Deployment Pipeline — Martin Fowler](https://www.martinfowler.com/bliki/DeploymentPipeline.html)** — 🅟 ⏱ 15 мин. Короткая заметка про то, зачем пайплайн разбит на стадии.
- **[MinimumCD — Immutable Artifact](https://beyond.minimumcd.org/docs/reference/practices/immutable-artifacts/)** — 🅟 ⏱ 10 мин. Минимум, без которого нельзя говорить о непрерывной доставке. Отсюда правило «собрать один раз, продвигать дальше без пересборки» и, как следствие, отказ от `latest`.
- **[Immutable artefacts — UK Home Office](https://engineering.homeoffice.gov.uk/patterns/immutable-artefacts/)** — 🅢 ⏱ 10 мин. То же самое языком инженерного стандарта организации.
- **[Beej's Guide to Network Concepts — layered model](https://beej.us/guide/bgnet0/html/split/the-layered-network-model.html)** — 🅟 ⏱ 25 мин. Почему сеть слоёная и что такое инкапсуляция. Без предварительных знаний, читается легко — годится в слот **D**.
- **[Google Cloud — Four Keys](https://cloud.google.com/blog/products/devops-sre/using-the-four-keys-to-measure-your-devops-performance)** — 🅢 ⏱ 15 мин. Четыре метрики DORA и главный контринтуитивный вывод: частые выкатки коррелируют с **меньшим** числом аварий, а не с бо́льшим. Готовый ответ на «как понять, что доставка настроена хорошо».

---

## 1 · Docker networking

### 🅟 Первоисточники

- **[Networking overview](https://docs.docker.com/engine/network/)** — ⏱ 20 мин. Общая картина: драйверы, что делает Docker с сетью хоста. Начинать отсюда.
- **[Bridge network driver](https://docs.docker.com/engine/network/drivers/bridge/)** — ⏱ 30 мин. **Главный текст блока.** Здесь прямым текстом сказано то, из-за чего, скорее всего, стоит твоя поломка: в дефолтной bridge-сети контейнеры видят друг друга **только по IP**, резолв по имени работает лишь в пользовательской сети.
- **[Networking in Compose](https://docs.docker.com/compose/how-tos/networking/)** — ⏱ 15 мин. Как Compose создаёт сеть проекта и почему обращаться надо к `имя_сервиса:внутренний_порт`, а не к опубликованному порту.
- **[Compose: секция `networks`](https://docs.docker.com/reference/compose-file/networks/)** — справочник. Смотреть точечно, когда понадобится `external: true` — а он понадобится, если GitLab и стенд подняты разными compose-файлами.
- **[`docker network create`](https://docs.docker.com/reference/cli/docker/network/create/)** — справочник по флагам.

### 🅢 Если официальная документация идёт тяжело

- **[Сети Docker изнутри: iptables и интерфейсы Linux](https://habr.com/ru/articles/333874/)** (Хабр, ru) — ⏱ 40 мин. Что именно Docker делает с сетевым стеком хоста. Статья 2017 года — конкретика по версиям устарела, механика нет. Читать как «что под капотом», не как инструкцию.
- **[Мастер-контейнер для Docker сети](https://habr.com/ru/articles/710126/)** (Хабр, ru) — по желанию, про сетевые namespace на практике.

**Не читать в этом паке:** overlay, macvlan, Swarm, сети Kubernetes. Не пригодится и займёт вечер.

---

## 2 · TCP, tcpdump, диагностика

### 🅢 Начать отсюда — это редкий случай, когда объяснение лучше первоисточника

- **[Let's learn tcpdump! — Julia Evans](https://wizardzines.com/zines/tcpdump/)** — ⏱ 30 мин. Комикс-зин на 12 страниц: как читать вывод, какие флаги важны, как писать BPF-фильтры. Лучшее введение в tcpdump, которое существует. Бесплатно читается [в архиве](https://archive.org/details/tcpdump-zine), анонс с содержанием — [в блоге автора](https://jvns.ca/blog/2017/04/29/new-zine--let-s-learn-tcpdump/).
- **[Linux debugging tools you'll love](https://jvns.ca/debugging-zine.pdf)** (PDF) — ⏱ 40 мин. `strace`, `netstat`, `tcpdump`, `ngrep` и остальное. Отлично идёт в **слот D** — картинки, короткие страницы, ничего не надо запускать. Тоже [в архиве](https://archive.org/details/debugging-zine).
- **[jvns.ca](https://jvns.ca/)** — блог целиком. На будущее: она пишет ровно о том, что нужно SRE, и объясняет так, как объясняют коллеге.

### Практика — по задаче 1.3

Команды из чеклиста, плюс полезные варианты:

```
tcpdump -i any port 3000 -nn            # то, что в задаче
tcpdump -i any -nn 'tcp[tcpflags] & (tcp-syn|tcp-ack) != 0'   # только рукопожатия
tcpdump -i any -nn -v 'tcp[tcpflags] & tcp-syn != 0'          # с опциями соединения
```

Способ запуска: в одном терминале `tcpdump`, в другом `curl -v` по тому же адресу. Смотришь `[S]`, `[S.]`, `[.]` в реальном времени. Один раз увидеть живьём — и вопрос про handshake на собеседовании закрыт навсегда.

- **[Making a Connection with tcpdump](https://www.linuxjournal.com/article/6447)** (Linux Journal) — 🅢 разбор вывода построчно. Старая статья, формат вывода с тех пор не менялся.
- **[TCP Internals: 3-way Handshake and Sequence Numbers](https://community.f5.com/kb/technicalarticles/tcp-internals-3-way-handshake-and-sequence-numbers-explained/281062)** (F5) — 🅢 если захочется разобраться с sequence numbers. Не обязательно в этом паке.

---

## 3 · GitLab Runner и CI/CD

### 🅟 Под задачи 2.1 и 2.2 — починка

- **[Troubleshooting GitLab Runner](https://docs.gitlab.com/runner/faq/)** — ⏱ 30 мин. **Читать до того, как начнёшь чинить.** Половина гипотез для `debug-gitlab-runner.md` берётся отсюда, включая случай, когда runner-демон до GitLab достучаться может, а контейнер джобы — нет (DNS хоста не передаётся в контейнер).
- **[Docker executor](https://docs.gitlab.com/runner/executors/docker/)** — ⏱ 30 мин. Ключевое: `network_mode` с именем существующей сети подключает контейнер сборки к ней. Скорее всего, это твоя недостающая строчка.
- **[Troubleshooting GitLab in Docker](https://docs.gitlab.com/install/docker/troubleshooting/)** и **[Configure GitLab in Docker](https://docs.gitlab.com/install/docker/configuration/)** — про `external_url`. Смотреть, если гипотеза «адрес работает снаружи, но не изнутри сети» подтвердится.
- **[Advanced configuration](https://docs.gitlab.com/runner/configuration/advanced-configuration/)** — справочник по `config.toml`. Точечно.

### 🅟 Под задачу 2.3 — сборка и push

- **[Build and push container images](https://docs.gitlab.com/user/packages/container_registry/build_and_push_images/)** — ⏱ 40 мин. Основной текст: аутентификация в registry, `docker build`, `docker push` из джобы.
- **[Use Docker to build Docker images](https://docs.gitlab.com/ci/docker/using_docker_build/)** — ⏱ 30 мин. Варианты (dind, socket binding) и их последствия. Выбери один и умей объяснить почему — это отдельный вопрос на собеседовании.
- **[Run CI/CD jobs in Docker containers](https://docs.gitlab.com/ci/docker/using_docker_images/)** — как работает `image:` в джобе.

**Про теги.** В документации GitLab прямо сказано: если использовать Git SHA в теге, каждая джоба уникальна и устаревшего образа не будет. Переменная — `$CI_COMMIT_SHORT_SHA`, полный адрес собирается как `$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA`. Отдельно: `$CI_COMMIT_REF_NAME` может содержать слеши, а тег образа — нет, поэтому для тегов по ветке существует `$CI_COMMIT_REF_SLUG`. Это ровно тот уровень детали, который отличает «делал» от «читал».

---

## 4 · Агентный харнесс

### 🅟 Под задачу 4.1

- **[Claude Code — overview](https://code.claude.com/docs/en/overview)** — ⏱ 15 мин. Что это и чем отличается от чата.
- **[Best practices](https://code.claude.com/docs/en/best-practices)** — ⏱ 20 мин. Читать после первого запуска, не до.
- **[Как Claude помнит проект (CLAUDE.md)](https://code.claude.com/docs/en/memory)** — ⏱ 20 мин. Под задачу 4.2. Главное правило оттуда: если `CLAUDE.md` слишком длинный, половина инструкций игнорируется — пиши только то, что иначе пришлось бы объяснять каждый раз. Есть команда `/init`, которая делает заготовку по твоему проекту.

**Важнее любого материала:** правило пака — каждое утверждение агента проверяешь руками. Он объясняет и показывает, где смотреть; делаешь ты.

---

## 5 · Собеседования

- **[Отобранные вопросы под трек 1](bank.md)** — 🅟 семь вопросов из моего банка, разобранных по задачам 1.1–1.3s: какой к какой задаче, открывать до или после, и почему именно этот. Четыре помечены как обязательные. Начинать отсюда, а не со следующей ссылки.
- **[devops-interview-questions](https://github.com/devops-interviews/devops-interview-questions)** (GitHub) — сторонний банк вопросов с решениями: Kubernetes, Docker, Linux, CI/CD, сети, Git, безопасность, облако.

**Как пользоваться и как не надо.** Не читать подряд — большая часть про уровень, до которого ещё полгода. Открывать точечно: закрыл тему на стенде → нашёл соответствующие вопросы → ответил вслух → сверился. Читать ответы до попытки ответить самому бесполезно: возникает ощущение знания без самого знания, и на собеседовании оно рассыпается.

Свой список вопросов под этот пак — в [`interview-questions-pack-01.md`](questions.md). Начинай с него; отобранные — вторым; сторонний банк — на потом.

---

## Как распределить по слотам

| Слот | Что сюда годится |
|---|---|
| **A** (4–5 ч) | Официальная документация Docker и GitLab **параллельно с работой на стенде**. Читаешь абзац → проверяешь командой |
| **C** (2 ч) | Зин про tcpdump, документация Claude Code, конспектирование |
| **D** (1–1.5 ч) | Зины Julia Evans, обзорные страницы, банк вопросов. Ничего, что требует запускать команды |
| **B** | — |

---

## Чего сознательно нет в списке

**Видеокурсов.** По четыре часа на модуль — при 20 часах за пак это половина бюджета в обмен на ощущение прогресса. Вернёмся к ним, если по отчёту окажется, что текст не заходит.

**Книг.** Хорошие есть, но за две недели ни одна не закроется, а брошенная на трети книга демотивирует сильнее, чем не начатая.

**Материалов по Kubernetes, Terraform, облакам.** Не в этом паке. Начнёшь параллельно — не закроешь ни одного.
