# Learning Machine

Backend-проект LMS (Learning Management System), реализованный на Django и Django REST Framework.

Проект представляет собой серверную часть SPA-приложения и возвращает данные в формате JSON.

---

## 📌 Описание проекта

В рамках задания реализована базовая архитектура LMS-системы, в которой:

- Пользователи могут быть зарегистрированы в системе (кастомная модель пользователя).
- Создаются курсы.
- Создаются уроки, которые могут быть привязаны к курсу.
- Реализован полный CRUD для курсов и уроков.
- В детальном представлении курса выводится количество уроков и список всех уроков курса.
- Добавлена модель платежей (оплата курса или отдельного урока).
- Реализован API эндпоинт для просмотра списка платежей с фильтрацией и сортировкой.
- В профиле пользователя выводится история платежей.

---

## 🛠 Используемые технологии

- Python
- Django
- Django REST Framework
- PostgreSQL
- Poetry
- Pillow
- python-dotenv

---

## ⚙️ Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone https://github.com/newfatto/learning_machine.git
cd learning_machine
```

### 2. Установить зависимости

```bash
poetry install --no-root
poetry env activate
```

### 3. Создать файл .env в корне проекта на основе .env.example


### 4. Применить миграции

```bash
python manage.py migrate
```
### 5. Создать суперпользователя

```bash
python manage.py createsuperuser
```

### 6. Запустить сервер

```bash
python manage.py runserver
```

---

## Приложение users

### Пользователь (User)

Реализована кастомная модель пользователя:
* Авторизация по email
* Телефон
* Город
* Аватар

### Платёж (Payment)

- user — ссылка на пользователя
- payment_date — дата оплаты (auto_now_add)
- course — оплаченный курс (nullable)
- lesson — оплаченный урок (nullable)
- payment — сумма оплаты (PositiveIntegerField, MinValueValidator(1))
- payment_way — способ оплаты: cash / transfer



## Модели приложения LMS

### Course (Курс)

* name — название
* description — описание
* preview — изображение превью

### Lesson (Урок)
* name — название
* description — описание
* preview — изображение превью
* video_link — ссылка на видео
* course — внешний ключ к Course

#### Связь:

* Один курс содержит много уроков
* При удалении курса удаляются связанные уроки (CASCADE)

### CRUD
#### Course

Реализован через ViewSet.
Поддерживает: Получение списка, Получение одного курса, 
Создание, Обновление, Удаление.

#### Lesson

Реализован через Generic-классы. Поддерживает: Получение списка, 
Получение одного урока, Создание, Обновление, Удаление.


## API эндпоинты

### Курсы
- `GET /courses/` — список курсов
- `GET /courses/<id>/` — детальная информация о курсе (включая количество уроков и список уроков)
- `POST /courses/` — создание курса
- `PUT/PATCH /courses/<id>/` — обновление курса
- `DELETE /courses/<id>/` — удаление курса

### Уроки
- `GET /lessons/` — список уроков
- `GET /lessons/<id>/` — детальная информация
- `POST /lessons/` — создание
- `PUT/PATCH /lessons/<id>/` — обновление
- `DELETE /lessons/<id>/` — удаление

### Платежи
- `GET /payments/` — список платежей с фильтрацией и сортировкой

#### Фильтрация и сортировка платежей

- Сортировка по дате оплаты:
  - `GET /payments/?ordering=payment_date`
  - `GET /payments/?ordering=-payment_date`

- Фильтрация по курсу:
  - `GET /payments/?course=<course_id>`

- Фильтрация по уроку:
  - `GET /payments/?lesson=<lesson_id>`

- Фильтрация по способу оплаты:
  - `GET /payments/?payment_way=cash`
  - `GET /payments/?payment_way=transfer`

