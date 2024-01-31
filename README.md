# Задание:
-------
Для корректной работы всего проекта, необходимо создать .env файл и заполнить его своими данными по образцу:
```
MODE=DEV
# Указать режим работы DEV, TEST, PROD

DB_HOST=db_name
DB_PORT=db_port
DB_USER=db_username
DB_NAME=db_name
DB_PASS=db_user_password

TEST_DB_HOST=test_db
TEST_DB_PORT=5432
TEST_DB_USER=restaurant_user
TEST_DB_NAME=test_restaurant_db
TEST_DB_PASS=pass
```
# Задание 1
<details>
Написать проект на FastAPI с использованием PostgreSQL в качестве БД. В проекте следует реализовать REST API по работе с меню ресторана, все CRUD операции.
Даны 3 сущности: Меню, Подменю, Блюдо.

Зависимости:
* У меню есть подменю, которые к ней привязаны.
* У подменю есть блюда.

Условия:
* Блюдо не может быть привязано напрямую к меню, минуя подменю.
* Блюдо не может находиться в 2-х подменю одновременно.
* Подменю не может находиться в 2-х меню одновременно.
* Если удалить меню, должны удалиться все подменю и блюда этого меню.
* Если удалить подменю, должны удалиться все блюда этого подменю.
* Цены блюд выводить с округлением до 2 знаков после запятой.
* Во время выдачи списка меню, для каждого меню добавлять кол-во подменю и блюд в этом меню.
* Во время выдачи списка подменю, для каждого подменю добавлять кол-во блюд в этом подменю.

# Запуск
------
Вам необходимо прописать следующие команды в вашей консоли:
```
git clone https://github.com/AKunshin/restaurant_menu
cd restaurant_menu
python3 -m venv env
```
Далее, активируйте виртуальную среду python

Для Linux:
```
. ./env/bin/activate
```

Для Windows:
```
. .\env\Scripts\activate
```
Необходимо создать файл .env и заполнить его своими данными, по образцу .env_example:

```
DB_HOST=db_host_name
DB_PORT=db_port
DB_USER=db_username
DB_NAME=db_name
DB_PASS=db_user_password
```

Установите требуемые зависимости,для этого пропишите в консоли:
```
pip install -r requirements.txt

```
Для запуска проекта в консоли пропишите команду:
```
uvicorn app.main:app --reload

```
Перейти на страницу автоматической документации Swagger:
```
http://localhost:8000/api/v1/docs
```


# Запуск Docker
------
Если у вас установлен Docker, вам потребуется всего лишь прописать 2 следующие команды:
```
docker compose build
docker compose up -d
```
##### Остановка docker:
-------
```
docker compose stop
```
Перейти на страницу автоматической документации Swagger:
```
http://localhost:8000/api/v1/docs
```
</details>

# Задание 2
<details>
Обернуть программные компоненты в контейнеры. 

Образы для Docker:
(API) python:3.10-slim
(DB) postgres:15.1-alpine

* Написать CRUD тесты для ранее разработанного API с помощью библиотеки pytest
* Подготовить отдельный контейнер для запуска тестов. Команду для запуска указать в README.md
* Реализовать вывод количества подменю и блюд для Меню через один (сложный) ORM запрос.
* Реализовать тестовый сценарий «Проверка кол-ва блюд и подменю в меню» из Postman с помощью pytest

# Запуск Docker
------
Для запуска контейнеров для тестирования выполните следующие команды:
```
docker compose -f docker-compose.test.yml build
docker compose -f docker-compose.test.yml up
```
##### Остановка docker:
-------
```
docker compose stop
```
Вывод количества подменю и блюд для Меню в одном сложном запросе реализован в эндпоинте:
```
app/menu/routers.py
@router.get("/test/{target_menu_id}")
```
Сам запрос SqlAlchemyORM находится app/menu/MenuDAO.py в следующем методе:
```
async def get_all_menu_fields_by_id(cls, id=id):
```
</details>

