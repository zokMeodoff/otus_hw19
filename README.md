## **Курс Web-разработчик на Python от OTUS**

### **Домашнее задание №19**
Переписать тесты проекта на pytest и factory_boy.

Проект представляет собой базовый бекенд для сайта с курсами.
Реализовать базовый бекенд для сайта с курсами.
Есть курс, у которого есть занятия, у курсов есть преподаватели. Есть пользователи, которые могут зарегистрироваться, залогиниться и записаться на курс.
Бекенд представляет собой REST-API на Django, который позволяет: 
- зарегистрироваться (можно без капчи и подтверждения email); 
- залогиниться; 
- посмотреть список курсов; 
- зайти внутрь одного курса, где посмотреть его описание и список уроков, прикриплённых к дате; 
- дополнительно можно задать возможность записаться на курс. 

### Установка

```консоль
Получение исходного кода приложения:
$ git clone https://github.com/zokMeodoff/otus_hw19.git

Установка зависимостей:
$ cd otus_hw19
$ pip install -r requirements.txt

Миграции:
$ python manage.py migrate

Загрузка данных в БД:
$ python manage.py loaddata courses

```

### Запуск

```консоль
$ python manage.py runserver
```

### API-запросы

#### Регистрация пользователя

    POST http://127.0.0.1:8000/users/ 

В теле запроса передаётся JSON-объект с данными регистрируемого пользователя.  
В теле ответа при успешной регистрации возвращается JSON-объект с данными зарегестрированного пользователя.

#### Аутентификация пользователя

	POST http://127.0.0.1:8000/users/login/

В теле запроса передаётся JSON-объект с учётными данными пользователя.  
В теле ответа в случае успешной аутентификации возвращается JSON-объект с токеном пользователя.

#### Просмотр списка курсов

    GET http://127.0.0.1:8000/courses/

Доступно только для зарегистрированных пользователей - в заголовке "Authorization" запроса необходимо передать значение токена, полученное при аутентификации.  
В теле ответа возвращается массив JSON-объектов, содержащих информацию о курсах.

#### Просмотр конкретного курса

    GET http://127.0.0.1:8000/courses/<id>/

Доступно только для зарегистрированных пользователей - в заголовке "Authorization" запроса необходимо передать значение токена, полученное при аутентификации.  
В теле ответа в случае, если курс с заданным идентификатором сущесвтует, возвращается JSON-объект, содержащий информацию о выбранном курсе.

#### Запись на курс

    PUT http://127.0.0.1:8000/courses/signup/<id>/
    или
    PATCH http://127.0.0.1:8000/courses/signup/<id>/

Доступно только для зарегистрированных пользователей - в заголовке "Authorization" запроса необходимо передать значение токена, полученное при аутентификации.  
В теле ответа в случае успешной записи на курс возвращается JSON-объект, содержащий
информацию о выбранном курсе.

### Запуск тестов

Тестирование регистрации и аутентификации пользователя:

    $ pytest --ds otus_courses_site.settings tests/test_users.py

Тестирование просмотра списка курсов, просмотра конкретного курса, записи на курс:

    $ pytest --ds otus_courses_site.settings tests/test_courses.py