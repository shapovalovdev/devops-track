# Чеклист: 1–14 сентября 2026

## Трек 1 — Фундамент: Сети и Архитектура
- [ ] **1.1 Сетевая диагностика в Linux (Минимум)**
  - [ ] Разобраны и выполнены команды `sudo ss -tulpn`
  - [ ] Найден слушающий процесс через `lsof -i :80` и `lsof -i -P -n | grep LISTEN`
  - [ ] Проверена маршрутизация ядра через `ip route show` и `ip route get <IP>`
  - [ ] Создан файл-шпаргалка `docs/network-cheatsheet.md` с примерами
- [ ] **1.2 Построение архитектурной схемы мониторинга в Excalidraw (Минимум)**
  - [ ] Шаг 1: Отрисованы 3 ВМ (`vm1-simpleapp`, `vm2-gitlab`, `vm3-runner`) и Host Laptop с IP-адресами
  - [ ] Шаг 2: Выделены сетевые контуры (`Host-Only`, `Internal Network`, `NAT`, `Docker Bridge`)
  - [ ] Шаг 3: Размещены прикладные сервисы (`Nginx`, `Simpleapp`, `PostgreSQL`, `Redis`, `GitLab`, `Registry`, `Runner`)
  - [ ] Шаг 4: Размещены агенты сбора метрик (`node_exporter` на 3 ВМ, `cAdvisor` на vm1/vm3, `Promtail`)
  - [ ] Шаг 5: Отрисован блок Prometheus Server с Scraper, TSDB и PromQL API
  - [ ] Шаг 6: Нарисованы стрелки Pull сбора метрик (`Prometheus` $\to$ `:9100`, `:8080`, `:9090`)
  - [ ] Шаг 7: Отрисован Alertmanager (`:9093`), поток алертов из Prometheus и нотификации в Telegram
  - [ ] Шаг 8: Обозначен поток Push логов (`Promtail` $\to$ `Loki :3100`) для контраста с метриками
  - [ ] Шаг 9: Отрисован слой Grafana (`:3000`) с PromQL/LogQL источниками и доступом с ноутбука
  - [ ] Шаг 10: Оформлена легенда, проверена читаемость и экспортирован файл `assets/stand-topology-v2.png`

## Трек 2 — Практика: Prometheus & CI/CD
- [ ] **2.1 Prometheus + node_exporter на 3 ВМ (Минимум)**
  - [ ] Создан `prometheus.yml` со статическими таргетами трех ВМ
  - [ ] Prometheus поднят в Docker на `vm2-gitlab`
  - [ ] `node_exporter` установлен и запущен на всех 3 ВМ
  - [ ] Проверен веб-интерфейс `http://<prometheus-ip>:9090/targets` — все 3 таргета в статусе `UP`
- [ ] **2.2 Контейнерные метрики через cAdvisor**
  - [ ] `cAdvisor` поднят на `vm1-simpleapp`
  - [ ] Таргет `cadvisor` добавлен в `prometheus.yml`
  - [ ] Проверены метрики `container_cpu_usage_seconds_total` и `container_memory_usage_bytes`
- [ ] **2.3 Устранение долга CI/CD (Tagging by SHA)**
  - [ ] В `.gitlab-ci.yml` настроен тег `$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA`
  - [ ] Шаг `deploy` переведен на деплой конкретного хэша коммита
  - [ ] Проверен детерминированный запуск через `docker ps`

## Трек 3 — Растяжка и Артикуляция
- [ ] **3.1 [+] Базовый PromQL (Растяжка)**
  - [ ] Написаны 5 базовых запросов (CPU %, Mem %, Disk %, Network rate, Instance Down)
- [ ] **4.1 Проговаривание вслух (Артикуляция)**
  - [ ] Повтор 1 (15 мин): Архитектура и сети своего стенда
  - [ ] Повтор 2 (15 мин): Pull-модель Prometheus и назначение экспортеров
