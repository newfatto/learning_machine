# 📚 Learning Machine — LMS Backend (Django + DRF)

Backend-приложение для платформы онлайн-обучения. Проект реализует управление курсами, уроками, пользователями, оплатами и подписками, а также фоновые и периодические задачи через Celery и Celery Beat.

Проект подготовлен к запуску локально, в Docker и к production-деплою на удалённый сервер через GitHub Actions.

---

## 🚀 Технологический стек

- Python 3.10
- Django
- Django REST Framework
- PostgreSQL
- Redis
- Celery + Celery Beat
- django-celery-beat
- SimpleJWT
- drf-yasg / Swagger
- Stripe API
- Poetry
- Docker, Docker Compose
- Gunicorn
- Nginx
- GitHub Actions

---

## ⚙️ Функциональность

### Основной функционал

- CRUD для курсов и уроков
- Привязка уроков к курсам
- Регистрация и авторизация пользователей
- JWT-аутентификация
- Разграничение прав доступа: владелец, модератор, обычный пользователь
- Подписка на обновления курсов
- Создание платежей за курс или урок
- Интеграция со Stripe Checkout Session
- Асинхронная отправка уведомлений через Celery
- Периодические задачи через Celery Beat

### Права доступа

В проекте используется разграничение прав:

- пользователь может работать со своими объектами;
- модератор может просматривать и изменять разрешённые сущности;
- владелец объекта имеет доступ к управлению своим контентом.

### Платежи

Платёжная логика включает:

- создание платежа за курс или урок;
- создание Stripe Checkout Session;
- сохранение ссылки на оплату;
- сохранение `session_id`;
- хранение суммы и способа оплаты.

### Уведомления

Celery используется для фоновых задач:

- отправка уведомлений при обновлении курса;
- проверка условий отправки уведомлений;
- выполнение периодических задач через Celery Beat.

---

## 📁 Основные сервисы Docker

В production-конфигурации используются сервисы:

- `nginx` — внешний веб-сервер, принимает HTTP-запросы на порту `80`;
- `web` — Django-приложение, запущенное через Gunicorn;
- `db` — PostgreSQL;
- `redis` — брокер сообщений для Celery;
- `celery` — worker для фоновых задач;
- `celery-beat` — планировщик периодических задач.

---

## 🔧 Переменные окружения

В проекте используется файл `.env`. 

Для настройки окружения используйте шаблон:

```bash
cp .env.template .env
```

Пример структуры переменных:

```env
SECRET_KEY=
DEBUG=False
ALLOWED_HOSTS=
CSRF_TRUSTED_ORIGINS=

DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_HOST=
DATABASE_PORT=5432

POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=

STRIPE_API_KEY=

CELERY_BROKER_URL=
CELERY_RESULT_BACKEND=
CELERY_TASK_ALWAYS_EAGER=False
CELERY_TASK_EAGER_PROPAGATES=False

EMAIL_HOST=
EMAIL_PORT=465
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_TLS=False
EMAIL_USE_SSL=True
DEFAULT_FROM_EMAIL=
```

### Важное различие хостов

При локальном запуске без Docker:

```env
DATABASE_HOST=localhost
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

При запуске через Docker Compose:

```env
DATABASE_HOST=db
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

---

## ▶️ Локальный запуск без Docker

### 1. Клонировать репозиторий

```bash
git clone https://github.com/newfatto/learning_machine.git
cd learning_machine
```

### 2. Установить зависимости

```bash
poetry install
```

### 3. Создать и заполнить `.env`

```bash
cp .env.template .env
```

Для локального запуска укажите:

```env
DATABASE_HOST=localhost
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
DEBUG=True
```

### 4. Применить миграции

```bash
poetry run python manage.py migrate
```

### 5. Запустить сервер разработки

```bash
poetry run python manage.py runserver
```

Приложение будет доступно по адресу:

```text
http://127.0.0.1:8000/
```

---

## 🐳 Локальный запуск через Docker Compose

Для локального Docker-запуска используется файл:

```text
docker-compose.yaml
```

### 1. Создать `.env`

```bash
cp .env.template .env
```

Для Docker-запуска укажите:

```env
DATABASE_HOST=db
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

### 2. Собрать и запустить контейнеры

```bash
docker compose up --build
```

или в фоновом режиме:

```bash
docker compose up -d --build
```

### 3. Проверить состояние контейнеров

```bash
docker compose ps
```

Ожидаемые сервисы:

```text
web
nginx / если используется production-compose
db
redis
celery
celery-beat
```

### 4. Остановить контейнеры

```bash
docker compose down
```

---

## 🚢 Production-запуск через Docker

Для production-запуска используется файл:

```text
docker-compose.prod.yml
```

Production-схема:

```text
Пользователь
    ↓
Nginx :80
    ↓
Gunicorn / Django web :8000 внутри Docker-сети
    ↓
PostgreSQL / Redis / Celery
```

### 1. Создать `.env` на сервере

На сервере в директории проекта должен быть файл `.env`.

Для текущего деплоя пример значений:

```env
DEBUG=False
ALLOWED_HOSTS=89.169.177.47,localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://89.169.177.47

DATABASE_HOST=db
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

### 2. Запустить production-контейнеры

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

### 3. Применить миграции

```bash
docker compose -f docker-compose.prod.yml run --rm web python manage.py migrate
```

### 4. Собрать статические файлы

```bash
docker compose -f docker-compose.prod.yml run --rm web python manage.py collectstatic --noinput
```

### 5. Проверить состояние контейнеров

```bash
docker compose -f docker-compose.prod.yml ps
```

Ожидаемые сервисы:

```text
web
nginx
db
redis
celery
celery-beat
```

### 6. Посмотреть логи

```bash
docker compose -f docker-compose.prod.yml logs --tail=100 web
docker compose -f docker-compose.prod.yml logs --tail=100 nginx
docker compose -f docker-compose.prod.yml logs --tail=100 celery
```

---

## 🌐 Доступ к приложению

Текущий сервер:

```text
http://89.169.177.47/
```

При открытии корневого адреса отображается DRF API Root. Ответ `401 Unauthorized` для защищённых API-эндпоинтов является ожидаемым поведением, так как в проекте используется JWT-аутентификация и глобальное ограничение доступа для неавторизованных пользователей.

---

## 📄 Документация API

Swagger:

```text
http://89.169.177.47/swagger/
```

Redoc:

```text
http://89.169.177.47/redoc/
```

Для локального запуска:

```text
http://127.0.0.1:8000/swagger/
http://127.0.0.1:8000/redoc/
```

---

## 🔑 Аутентификация

В проекте используется JWT-аутентификация.

Получение токена:

```http
POST /login/
```

Обновление токена:

```http
POST /token/refresh/
```

Для доступа к защищённым эндпоинтам необходимо передавать access token в заголовке:

```http
Authorization: Bearer <access_token>
```

---

## 📚 Основные эндпоинты

### Пользователи

```http
GET     /user/
POST    /user/
GET     /user/{id}/
PUT     /user/{id}/
DELETE  /user/{id}/
```

### Курсы

```http
GET     /course/
POST    /course/
GET     /course/{id}/
PUT     /course/{id}/
DELETE  /course/{id}/
```

### Уроки

```http
GET     /lessons/
POST    /lesson/create/
GET     /lesson/{id}/
PUT     /lesson/update/{id}/
DELETE  /lesson/delete/{id}/
```

### Платежи

```http
GET     /payments/
POST    /payment/create/
GET     /payment/{id}/
PUT     /payment/update/{id}/
DELETE  /payment/delete/{id}/
```

---

## 🧪 Тестирование

Запуск тестов локально:

```bash
poetry run python manage.py test
```

В CI тесты запускаются автоматически при Pull Request и при push в ветку `develop`.

GitHub Actions поднимает временные сервисы PostgreSQL и Redis, применяет миграции и запускает Django-тесты.

---

## ✅ Линтинг

Для проверки качества кода используется `flake8`.

Команда локального запуска:

```bash
poetry run flake8 . --exclude=.venv,venv,migrations,htmlcov --max-line-length=119
```

---

## ⚙️ CI/CD

В проекте настроен GitHub Actions workflow:

```text
.github/workflows/ci-cd.yml
```

Pipeline выполняет этапы:

```text
test → lint → build → deploy
```

### Этап `test`

На этапе тестирования GitHub Actions:

1. создаёт временную Ubuntu-машину;
2. поднимает PostgreSQL и Redis как сервисы;
3. устанавливает Poetry;
4. устанавливает зависимости проекта;
5. применяет миграции;
6. запускает тесты Django.

Если тесты завершаются с ошибкой, pipeline останавливается и деплой не выполняется.

### Этап `lint`

На этапе линтинга выполняется проверка кода через `flake8`.

Если линтер находит ошибки, pipeline останавливается.

### Этап `build`

На этапе сборки GitHub Actions проверяет, что Docker-образ проекта успешно собирается.

Команда:

```bash
docker build -t learning-machine:test .
```

### Этап `deploy`

Деплой выполняется только после успешного прохождения этапов `test`, `lint` и `build`.

Деплой запускается при push/merge в ветку `develop`.

GitHub Actions:

1. подключается к серверу по SSH;
2. копирует файлы проекта на сервер через `rsync`;
3. создаёт `.env` на сервере из GitHub Secret `ENV_FILE`;
4. запускает Docker Compose;
5. применяет миграции;
6. собирает статические файлы;
7. поднимает production-контейнеры.

---

## 🔐 GitHub Secrets

Для CI/CD используются GitHub Secrets.

Минимальный набор секретов:

```text
SSH_KEY
SSH_USER
SERVER_IP
DEPLOY_DIR
ENV_FILE
```

### Назначение секретов

| Secret | Назначение |
|---|---|
| `SSH_KEY` | приватный SSH-ключ для подключения GitHub Actions к серверу |
| `SSH_USER` | пользователь на сервере |
| `SERVER_IP` | публичный IP-адрес сервера |
| `DEPLOY_DIR` | директория проекта на сервере |
| `ENV_FILE` | содержимое production `.env` файла |

Пример серверных значений:

```text
SSH_USER=user
SERVER_IP=89.129.164.45
DEPLOY_DIR=/home/user/apps/learning_machine
```

В `ENV_FILE` хранится содержимое серверного `.env` файла. Реальные значения переменных окружения не хранятся в репозитории.

---

## 🔒 Безопасность и порты

На сервере наружу открыты только необходимые порты:

```text
22  SSH
80  HTTP
```

PostgreSQL, Redis и Gunicorn не опубликованы наружу и доступны только внутри Docker-сети:

```text
5432 PostgreSQL
6379 Redis
8000 Gunicorn/Django
```

Nginx принимает внешние HTTP-запросы на порту `80` и проксирует их во внутренний сервис `web`.

Проверить открытые порты на сервере:

```bash
sudo ss -tulpn
```

Проверить состояние production-контейнеров:

```bash
docker compose -f docker-compose.prod.yml ps
```

---

## 🧠 Важные архитектурные решения

- Docker используется для изоляции окружения.
- PostgreSQL используется как основная база данных.
- Redis используется как брокер сообщений для Celery.
- Celery и Celery Beat вынесены в отдельные контейнеры.
- Gunicorn используется как WSGI-сервер для Django.
- Nginx используется как reverse proxy и внешний веб-сервер.
- Переменные окружения вынесены в `.env` и GitHub Secrets.
- Production-контейнеры настроены с `restart: unless-stopped` для автоматического перезапуска.

---

## 📌 Примечания

- В Docker нельзя использовать `localhost` для подключения к другим контейнерам.
- Для связи между контейнерами используются имена сервисов: `db`, `redis`, `web`.
- Реальный `.env` не должен попадать в репозиторий.
- `.env.template` должен быть полным, но без чувствительных данных.
- После изменения production-настроек деплой выполняется автоматически через GitHub Actions после merge/push в `develop`.
