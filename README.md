# FastAPI_OAuth2

## Реализация на *FastAPI* авторизации на основе *JSON Web Token*

## 1. Описание проекта

Данный проект демонстрирует пример реализации микросервиса авторизации на основе ***JWT токена***, а также пример 
использования этого микросервиса на сайте созданном на FastAPI, в виде реализации интерфейса ***Starlette*** для 
управления аутентификацией и разрешениями ***AuthenticationBackend***, который добавляется в обработку запроса к серверу 
в виде ***AuthenticationMiddleware***.

Проект реализован и проверен на Python 3.12, FastAPI 0.115, SQLAlchemy 2.0.

Основной проект состоит из двух проектов: ***OAuth2*** - собственно сам микросервис авторизации реализованный на фреймворке 
[FastAPI](https://fastapi.tiangolo.com/). А так же ***OAuth2_test*** - небольшой сайт, так же реализованный на FastAPI, 
который в своей реализации использует микросервис OAuth2 для проверки авторизации пользователя. Оба проекта можно запустить 
как по отдельности, в системе контейнеризации ***docker***, так и совместно, с помощью системы запуска многоконтейнерных 
Docker-приложений ***docker-compose***. Если у Вас установлен ***Python***, то конечно же любой из проектов можно запустить 
и вручную.

Из особенностей хотел бы обратить внимание на применение в качестве работы с криптошифрованием паролей, 
библиотеки [*pwdlib*](https://pypi.org/project/pwdlib/) версии 0.2.1, вместо библиотеки [*passlib*](https://pypi.org/project/passlib/), 
которая при реализации проектов на FastAPI используется гораздо чаще. Но, тем не менее, в моём проекте при запуске его 
в контейнере [*python:3.12-slim*](https://hub.docker.com/_/python), библиотека passlib версии 1.7.4 вызвала ошибку. 
Возможную причину описывают как плохую поддержку данной библиотеки. В качестве решения проблемы и было предложено использование 
более современной аналогичной библиотеки pwdlib.

## 2. Проект OAuth2

Проект ***OAuth2*** является реализацией микросервиса авторизации по протоколу ***OAuth*** версии **2**, посредством ключа 
аутентификации пользователя ***JWT*** (***JSON Web Token***). Реализован данный микросервис с использованием фреймворка
FastAPI.

### 2.1 Запуск вручную

Если у Вас установлен интерпретатор [*Python*](https://www.python.org/) версии <ins>3.12</ins>, то данный сервис можно запустить 
вручную. Для этого надо создать виртуальное окружение и установить в него пакеты из файла *requirements.txt* данного проекта.
Далее все действия должны производиться в этом активированном виртуальном окружении.

Для работы сервиса, надо сгенерировать базу данных. Так как это исключительно демонстрационный проект, то в качестве базы данных используется 
обычный ***SQLite3***. Для работы с базой данных используется библиотека [*SQLAlchemy*](https://www.sqlalchemy.org/), 
а для управления миграциями базы данных SQLAlchemy, применяется пакет [*Alembic*](https://alembic.sqlalchemy.org/en/latest/index.html).
Конечно ревизия базы данных мной уже подготовлена, и осталось её только инициализировать. Для этого надо запустить команду
`alembic upgrade head`. 

Очень важно, так как для управления миграциями, Alembic использует файл конфигурации 
[alembic.ini](https://github.com/Paradox81ru/FastAPI_OAuth2/blob/main/OAuth2/alembic.ini),
а он находиться в корневой директории проекта [OAuth2](https://github.com/Paradox81ru/FastAPI_OAuth2/tree/main/OAuth2),
то команду инициализации базы данных надо запускать именно из директории **OAuth2**. 

И ещё одно достаточно важное примечание. При инициализации базы данных, в неё сразу добавляются четыре пользователя с различными ролями. 
Настройка параметров этих пользователей, вроде того, какие они получат адреса электронной почты и пароли, зависят от конфигурации 
приложения, где, кроме прочих параметров, также устанавливаются настройки начальной инициализации пользователей. Значения 
этих настроек берутся из файла **.env**, который, чтобы с него считались данные, должен находиться в поддиректории 
[Auth](https://github.com/Paradox81ru/FastAPI_OAuth2/tree/main/OAuth2/Auth). Так как этот файл содержит личные данные, 
то мной он был отмечен в [.gitignore](https://github.com/Paradox81ru/FastAPI_OAuth2/blob/main/.gitignore), поэтому, после 
клонирования проекта, Вы его та мне найдёте. Если этот файл не добавить в проект, то настройки будут взяты из значений 
по умолчанию файла конфигурации [config.py](https://github.com/Paradox81ru/FastAPI_OAuth2/blob/main/OAuth2/config.py).
Но я всё же рекомендовал бы этот файл установить, и изменять настройки приложения именно с помощью него. Проще всего это 
сделать с помощью точно такого же файла настроек [.env](https://github.com/Paradox81ru/FastAPI_OAuth2/blob/main/OAuth2/tests/.env), 
но используемого для тестирования проекта. Находиться он в директории [tests](https://github.com/Paradox81ru/FastAPI_OAuth2/tree/main/OAuth2/tests),
и именно тот формат, который и нужен. Поэтому надо просто скопировать файл **.env** из директории **tests** в директорию **Auth**,
и изменить в нём значения переменных. Это будет особенно полезно при тестировании сервиса авторизации на другом сайте, 
когда для формирования токена доступа, нужно будет вводить логин и пароль, и они будут именно те, что Вы указали в файле настроек.

И так, после инициализации базы данных в корне проекта появится файл **db.sqlite3** (или такой, как Вы указали в настройках,
если Вы вдруг решили их изменить). Далее можно запускать сам сервис. Для этого воспользуемся ***ASGI*** сервером 
[*Uvicorn*](https://www.uvicorn.org/), с помощью которого OAuth2 микросервис можно запустить с помощью команды 
`uvicorn main:app --host localhost --port 8001`. Значение хоста *localhost* и значение порта *8001* указаны именно эти 
потому, что в настройках сайта проверки сервиса авторизации в соответствующих переменных указаны именно эти настройки. 
Если сервис будет запущен с другими параметрами, то далее сайт проверки не сможет произвести проверку авторизации пользователя,
пока на сайте проверки не будут произведены соответствующие изменения в настройках конфигурации.

Так же сервис можно запустить, просто запустив файл main.py: `python main.py`, главное перед этим не забыть активировать 
виртуальное окружение и инициализировать базу данных.

В директории [tests](https://github.com/Paradox81ru/FastAPI_OAuth2/tree/main/OAuth2/tests) расположены тесты, реализованные
с помощью библиотеки [*pytest*](https://docs.pytest.org/en/stable/index.html). Хочу заметить, что каждый раз перед началом
тестирования сервиса, ***pytest*** создаёт свою тестовую базу, инициируя её пользователями в соответствии с конфигурацией файла 
**.env**, расположенного в директории **test**. После запуска теста в корне проекта появится тестовая база **db-test.sqlite3**.
Для инициализации базы данных используется всё та же библиотека управления миграциями ***Alembic***, и так как файл конфигурации 
***Alembic*** - **alembic.ini**, расположен в корне проекта, то и запуск тестов должен производиться не из директории *tests*, 
а из коневой директории **OAuth2**. И ещё хочу заметить, что если при запуске ***pytest*** теста Вы получите ошибку 
`ModuleNotFoundError: No module named 'main'`, то попробуйте запустить ***pytest*** как выполняемый модуль, с ключом -m, 
чтобы текущий каталог оказывался в списке рабочих каталогов: `python -m pytest -vv`.

### 2.2 Запуск с помощью docker