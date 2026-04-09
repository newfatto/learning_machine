# 📚 Learning Machine — LMS Backend (Django + DRF)

Backend-приложение для платформы онлайн-обучения. Реализует управление курсами, уроками, оплатами и подписками, а также асинхронные задачи с использованием Celery.

---

# 🚀 Технологический стек

* Python 3.10+
* Django
* Django REST Framework
* PostgreSQL
* Redis
* Celery + Celery Beat
* Docker, Docker Compose
* SimpleJWT (аутентификация)
* drf-yasg / Swagger (документация API)

---

# ⚙️ Функциональность

## 📦 Основной функционал

* CRUD для курсов и уроков
* Привязка уроков к курсам
* Ограничение доступа (владелец / модератор)
* Подписка на обновления курсов
* Платежи (интеграция со Stripe)
* Публичные и приватные данные пользователей

---

## 🔐 Аутентификация

* JWT (access + refresh)
* Регистрация и авторизация пользователей
* Разграничение прав доступа:

  * пользователь
  * модератор
  * владелец объекта

---

## 💳 Платежи

* Создание платежей за курс или урок
* Генерация Stripe Checkout Session
* Хранение:

  * суммы
  * ссылки на оплату
  * session_id

---

## 🔔 Уведомления (Celery)

Реализована асинхронная система задач:

* Отправка уведомлений при обновлении курса
* Проверка условий отправки (например, не чаще чем раз в 4 часа)
* Фоновая обработка задач через Celery

---

## ⏰ Периодические задачи (Celery Beat)

* Планировщик задач на базе `django_celery_beat`
* Хранение расписаний в базе данных
* Автоматический запуск задач по расписанию

---

# 🐳 Запуск через Docker

## 📁 Структура сервисов

* `web` — Django приложение
* `db` — PostgreSQL
* `redis` — брокер сообщений
* `celery` — worker
* `celery-beat` — планировщик задач

---

## 🔧 Переменные окружения (.env)

Создайте файл `.env` в корне проекта:

```env
SECRET_KEY=your_secret_key
DEBUG=False

POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=123456
POSTGRES_HOST=db
POSTGRES_PORT=5432

CELERY_BROKER_URL=redis://redis:6379/0
CELERY_BACKEND=redis://redis:6379/0
```

---

## ▶️ Запуск проекта

```bash
docker compose up --build
```

или в фоне:

```bash
docker compose up -d --build
```

---

## 📊 Проверка статуса

```bash
docker compose ps
```

Ожидаемый результат:

```
web           Up
db            Up (healthy)
redis         Up
celery        Up
celery-beat   Up
```

---

⚠️ Возможная проблема при первом запуске

При первом запуске контейнер celery-beat может завершиться с ошибкой вида:
```
relation "django_celery_beat_..." does not exist
```
*Причина*

Контейнер celery-beat стартует быстрее, чем Django успевает применить миграции (migrate), из-за чего необходимые таблицы ещё не созданы.

✅ Решение

После того как контейнер web завершил миграции, необходимо перезапустить celery-beat:
```
docker compose restart celery-beat
```
или:
```
docker compose up -d celery-beat
```
🔍 Проверка после исправления
```
docker compose ps
```

Контейнер celery-beat должен перейти в статус:
```
celery-beat   Up
```
## 🛑 Остановка

```bash
docker compose down
```

---

# 🌐 API

## 📄 Документация

Swagger доступен по адресу:

```
http://localhost:8000/swagger/
```

или:

```
http://localhost:8000/redoc/
```

---

## 🔑 Аутентификация

Получение токена:

```
POST /login/
```

Обновление:

```
POST /token/refresh/
```

---

## 📚 Основные эндпоинты

👤 Пользователи
```
GET     /user/
POST    /user/
GET     /user/{id}/
PUT     /user/{id}/
DELETE  /user/{id}/
```

### Курсы

```
GET     /course/
POST    /course/
GET     /course/{id}/
PUT     /course/{id}/
DELETE  /course/{id}/
```

---

### Уроки

```
GET     /lessons/
POST    /lesson/create/
GET     /lesson/{id}/
PUT     /lesson/update/{id}/
DELETE  /lesson/delete/{id}/
```

---

### Платежи

```
GET     /payments/
POST    /payment/create/
GET     /payment/{id}/
PUT     /payment/update/{id}/
DELETE  /payment/delete/{id}/
```

---

# ⚡ Особенности реализации

* Разделение логики:

  * `services.py` — бизнес-логика
  * `serializers.py` — валидация и трансформация данных
  * `views.py` — API

* Гибкая система прав доступа
* Асинхронные задачи через Celery

---

# 🧠 Важные архитектурные решения

* Использование Docker для изоляции среды
* Redis как брокер для Celery
* PostgreSQL как основная база данных
* Разделение контейнеров по ролям
* Использование переменных окружения для конфигурации

---

# 📌 Примечания

* В Docker нельзя использовать `localhost` для подключения к другим сервисам
* Для связи используется имя сервиса:

  * Postgres → `db`
  * Redis → `redis`
* Все зависимости поднимаются через Docker Compose

---


---
