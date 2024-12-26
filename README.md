# FastAPI_OAuth2

## Реализация на *FastAPI* авторизации на основе *JSON Web Token*

## Оглавление
- 1 [Описание проекта.](#1-описание-проекта)
- 2 [Проект OAuth2.](#2-проект-oauth2)
- 2.1 [Запуск вручную.](#21-запуск-вручную)
- 2.2 [Запуск с помощью docker.](#22-запуск-с-помощью-docker)
- 2.3 [Запуск с помощью docker-compose.](#23-запуск-с-помощью-docker-compose)
- 2.4 [Переменные окружения сервиса авторизации.](#24-переменные-окружения-сервиса-авторизации)
- 2.5 [Проверка запуска сервиса авторизации.](#25-проверка-запуска-сервиса-авторизации)
- 2.6 [Принцип работы.](#26-принцип-работы)
- 2.7 [Получение токенов.](#27-получение-токенов)
- 2.8 [Проверка токена доступа.](#28-проверка-токена-доступа)
- 2.9 [Обновление токена доступа.](#29-обновление-токена-доступа)
- 3 [Проект OAuth2_test.](#3-проект-oauth2_test)
- 3.1 [Запуск вручную.](#31-запуск-вручную)
- 3.2 [Запуск с помощью docker.](#32-запуск-с-помощью-docker)
- 3.3 [Запуск с помощью docker-compose.](#33-запуск-с-помощью-docker-compose)
- 3.4 [Переменные окружения сайта проверки сервиса авторизации.](#34-переменные-окружения-сайта-проверки-сервиса-авторизации)
- 3.5 [Проверка запуска сервиса авторизации.](#35-проверка-запуска-сервиса-авторизации)
- 3.6 [Принцип работы.](#36-принцип-работы)
- 4 [Проверка работы сервиса с помощью визуального интерфейса.](#4-проверка-работы-сервиса-с-помощью-визуального-интерфейса)

## 1. Описание проекта

Данный проект демонстрирует пример реализации микросервиса авторизации на основе ***JWT токена***, а также пример 
использования этого микросервиса на сайте созданном на FastAPI, в виде реализации интерфейса ***Starlette*** для 
управления аутентификацией и разрешениями ***AuthenticationBackend***, который добавляется в обработку запроса к серверу 
в виде ***AuthenticationMiddleware***.

Проект реализован и проверен на Python 3.12, FastAPI 0.115, SQLAlchemy 2.0.

Основной проект состоит из двух проектов: [OAuth2*](https://github.com/Paradox81ru/FastAPI_OAuth2/tree/main/OAuth2) - 
собственно сам микросервис авторизации реализованный на фреймворке [FastAPI](https://fastapi.tiangolo.com/). А так же 
[OAuth2_test](https://github.com/Paradox81ru/FastAPI_OAuth2/tree/main/OAuth2_test) - небольшой сайт, так же 
реализованный на FastAPI, который в своей реализации использует микросервис OAuth2 для проверки авторизации пользователя. 
Оба проекта можно запустить как по отдельности, в системе контейнеризации [***docker***](https://www.docker.com/), так 
и совместно, с помощью системы запуска многоконтейнерных Docker-приложений [***docker-compose***](https://docs.docker.com/compose/). 
Если у Вас установлен [***Python***]((https://www.python.org/)), то конечно же любой из проектов можно запустить и вручную.

Из особенностей хотел бы обратить внимание на применение в качестве работы с криптошифрованием паролей, библиотеки 
[*pwdlib*](https://pypi.org/project/pwdlib/) версии 0.2.1, вместо библиотеки [*passlib*](https://pypi.org/project/passlib/), 
которая при реализации проектов на FastAPI используется гораздо чаще. Но, тем не менее, в моём проекте при запуске его 
в контейнере [*python:3.12-slim*](https://hub.docker.com/_/python), библиотека *passlib* версии 1.7.4 вызвала ошибку. Возможную причину в интернете
описывают как плохую поддержку данной библиотеки. В качестве решения проблемы и было предложено использование более 
современной аналогичной библиотеки *pwdlib*. Впрочем, управление криптошифрованием паролей в моём проекте осуществляется 
в виде реализации интерфейса [AbstractPwdContext](https://github.com/Paradox81ru/FastAPI_OAuth2/blob/main/OAuth2/Auth/base.py),
и библиотеку можно легко заменить в конфигурационном файле [config.py](https://github.com/Paradox81ru/FastAPI_OAuth2/blob/main/OAuth2/config.py),
в функции возвращающей класс работы с паролем ***get_pwd_context()***. В частности, для возвращения к библиотеке *passlib*,
достаточно в функции ***get_pwd_context()*** раскомментировать первую строку и закомментировать третью строку.


## 2. Проект OAuth2

Проект [OAuth2](https://github.com/Paradox81ru/FastAPI_OAuth2/tree/main/OAuth2) является реализацией микросервиса 
авторизации по протоколу ***OAuth*** версии **2**, посредством ключа аутентификации пользователя ***JWT*** (***JSON Web Token***). 
Реализован данный микросервис с использованием фреймворка ***FastAPI***.

### 2.1 Запуск вручную

Если у Вас установлен интерпретатор [*Python*](https://www.python.org/) версии <ins>3.12</ins>, то данный сервис можно запустить 
вручную. Для этого надо создать виртуальное окружение и установить в него пакеты из файла 
[requirements.txt](https://github.com/Paradox81ru/FastAPI_OAuth2/blob/main/OAuth2/requirements.txt) данного проекта.
Далее все действия должны производиться в этом активированном виртуальном окружении.

Для работы сервиса, требуется сгенерировать базу данных. Так как это исключительно демонстрационный проект, то в качестве базы данных используется 
обычный [*SQLite3*](https://docs.python.org/3/library/sqlite3.html). Для работы с базой данных используется библиотека [*SQLAlchemy*](https://www.sqlalchemy.org/), 
а для управления миграциями базы данных *SQLAlchemy*, применяется пакет [*Alembic*](https://alembic.sqlalchemy.org/en/latest/index.html).
Конечно ревизия базы данных мной уже подготовлена, и осталось её только инициализировать. Для этого надо запустить команду
`alembic upgrade head`. 

Очень важно, так как для управления миграциями, *Alembic* использует файл конфигурации 
[alembic.ini](https://github.com/Paradox81ru/FastAPI_OAuth2/blob/main/OAuth2/alembic.ini),
а он находиться в корневой директории проекта [OAuth2](https://github.com/Paradox81ru/FastAPI_OAuth2/tree/main/OAuth2),
то команду инициализации базы данных надо запускать именно из директории **OAuth2**. 

И ещё одно достаточно важное примечание. При инициализации базы данных, в неё добавляется четыре пользователя с различными ролями. 
Настройка параметров этих пользователей, вроде того, какие они получат адреса электронной почты и пароли, зависят от конфигурации 
приложения, где, кроме прочих параметров, также устанавливаются настройки начальной инициализации пользователей. Значения 
этих настроек берутся из файла **.env**, который, чтобы с него считались данные, должен находиться в поддиректории 
[Auth](https://github.com/Paradox81ru/FastAPI_OAuth2/tree/main/OAuth2/Auth). Так как этот файл содержит личные данные, 
то мной он был отмечен в [.gitignore](https://github.com/Paradox81ru/FastAPI_OAuth2/blob/main/.gitignore), поэтому, после 
клонирования проекта, Вы его там не найдёте. Если этот файл не добавить в проект, то настройки будут взяты из значений 
по умолчанию файла конфигурации [config.py](https://github.com/Paradox81ru/FastAPI_OAuth2/blob/main/OAuth2/config.py).
Но я всё же рекомендовал бы этот файл установить, и изменять настройки приложения именно с помощью него. Проще всего это 
сделать с помощью точно такого же файла настроек [.env](https://github.com/Paradox81ru/FastAPI_OAuth2/blob/main/OAuth2/tests/.env), 
но используемого для тестирования проекта. Находиться он в директории [tests](https://github.com/Paradox81ru/FastAPI_OAuth2/tree/main/OAuth2/tests),
и имеет он именно тот формат, который и нужен. Поэтому надо просто скопировать файл **.env** из директории **tests** в директорию **Auth**,
и изменить в нём значения переменных. Это будет особенно полезно при тестировании сервиса авторизации на другом сайте, 
когда для формирования токена доступа, нужно будет вводить логин и пароль, и они будут именно те, что Вы указали в файле настроек.

И так, после инициализации базы данных в корне проекта появится файл **db.sqlite3** (или такой, как Вы указали в настройках,
если Вы вдруг решили их изменить). Далее можно запускать сам сервис. Для этого воспользуемся ***ASGI*** сервером 
[*Uvicorn*](https://www.uvicorn.org/), с помощью которого OAuth2 микросервис можно запустить с помощью команды 
`uvicorn main:app --host localhost --port 8001`. Значение хоста *localhost* и значение порта *8001* указаны именно эти 
потому, что в настройках сайта проверки сервиса авторизации, в соответствующих переменных указаны именно эти настройки. 
Если сервис будет запущен с другими параметрами, то далее сайт проверки не сможет произвести проверку авторизации пользователя,
пока на сайте проверки не будут произведены соответствующие изменения в настройках конфигурации.

Так же сервис можно запустить, просто запустив файл main.py: `python main.py`, главное перед этим не забыть активировать 
виртуальное окружение и инициализировать базу данных. Запуск сервера ***Uvicorn*** будет осуществлён с параметрами значение хоста *localhost* 
и значение порта *8001*.

В директории [tests](https://github.com/Paradox81ru/FastAPI_OAuth2/tree/main/OAuth2/tests) расположены тесты, реализованные с помощью библиотеки [*pytest*](https://docs.pytest.org/en/stable/index.html). Хочу заметить, что каждый раз перед началом
тестирования сервиса, ***pytest*** создаёт свою тестовую базу, инициируя её пользователями в соответствии с конфигурацией файла 
**.env**, расположенного в директории **test**. После запуска теста в корне проекта появится тестовая база **db-test.sqlite3**.
Для инициализации базы данных используется всё та же библиотека управления миграциями ***Alembic***, и так как файл конфигурации 
***Alembic*** - **alembic.ini**, расположен в корне проекта, то и запуск тестов должен производиться не из директории *tests*, 
а из коневой директории **OAuth2**. И ещё хочу заметить, что если при запуске ***pytest*** теста Вы получите ошибку 
`ModuleNotFoundError: No module named 'main'`, то попробуйте запустить ***pytest*** как выполняемый модуль, с ключом -m, 
чтобы текущий каталог оказывался в списке рабочих каталогов: `python -m pytest -vv`.

### 2.2 Запуск с помощью docker

В настоящий момент проект оптимизирован для запуска его целиком с помощью ***docker-compose***, поэтому, для того чтобы запустить 
проекты по отдельности в [***docker***](https://www.docker.com/), надо внести небольшие изменения. Во-первых, при запуске сервиса авторизации, как мы 
помним, должна быть инициализирована база данных. Так как в случае с ***docker-compose*** эту функцию берёт на себя он, то
в случае с ***docker*** в конфигурационном файле [Dockerfile](https://github.com/Paradox81ru/FastAPI_OAuth2/blob/main/OAuth2/Dockerfile)
в данный момент инициализация базы данных закомментирована. Поэтому надо раскомментировать строку `RUN alembic upgrade head`.
Далее, для инициализации базы данных требуются настройки конфигурации, чтобы инициированные пользователя получили известные
логины и пароли. В целях безопасности основной *.env* файл настройки переменных окружения, в контейнер не передаётся вообще,
а все значения всех переменных указываются прямо в конфигурационном файле ***Dockerfile***, которые в настоящий момент так же
закомментированы. Поэтому все *ENV* значения нужно раскомментировать. И тут я должен предостеречь, что хранить пароли и секретные ключи
в открытом виде не безопасно. В *production* для этого следует использовать секреты. Но так как этот проект исключительно
демонстрационный, то в данном случае пароли пользователей удобнее хранить прямо в конфигурационном файле. И наконец сам 
запуск сервиса, после запуска контейнера, для этого следует раскомментировать последнюю строку в *Dockerfile*] 
`CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]`. Про значения параметров хоста и порта 
ранее уже упоминалось. Собственно всё, контейнер можно создавать и запускать. Разумеется, для того чтобы сайт проверки
авторизации смог получить доступ к этому контейнеру, контейнеру сервиса авторизации при создании следует назначить наименование
*oauth2*, и запускать оба контейнера надо в одной сети докера.

### 2.3 Запуск с помощью docker-compose

И наконец, самое простое, это запуск проекта целиком с помощью [***docker-compose***](https://docs.docker.com/compose/). 
В этом случае изменения можно внести только в конфигурационный файл [docker-compose.yml](https://github.com/Paradox81ru/FastAPI_OAuth2/blob/main/docker-compose.yml),
значение переменных окружения которых теперь меняются именно здесь. Конфигурационные же файлы *Dockerfile* менять не следует,
все закомментированные строки, должны остаться закомментированы. Инициализацию базы данных, запуск сервисов и объединение
их в одну сеть, берёт на себя docker-compose. 

### 2.4 Переменные окружения сервиса авторизации

Как бы не запускался сервис, во всех случаях работа его будет зависеть от установленных параметров переменных, набор 
которых во всех случаях одинаковый:
- SECRET_KEY - секретный ключ для шифрования и дешифрования токена;
- ACCESS_TOKEN_EXPIRE_MINUTES - время жизни токена доступа. Через какое время, в минутах, токен доступа станет просроченным и не валидным;
- ACCESS_TOKEN_EXPIRE_MINUTES - время жизни токена обновления. Через какое время, в минутах, токен обновления станет просроченным и не валидным;
- DB_CONNECT_STR - строка соединения с базой данных;
- INIT_ADMIN_EMAIL - электронная почта администратора при инициализации базы данных;
- INIT_SYSTEM_EMAIL - электронная почта специального системного пользователя при инициализации базы данных;
- INIT_DIRECTOR_LOGIN - логин пользователя с ролью директора при инициализации базы данных;
- INIT_DIRECTOR_NAME - имя пользователя с ролью директора при инициализации базы данных;
- INIT_DIRECTOR_LASTNAME - фамилия пользователя с ролью директора при инициализации базы данных;
- INIT_DIRECTOR_EMAIL - электронная почта пользователя с ролью директора при инициализации базы данных;
- INIT_USER_LOGIN - логин обычного пользователя с ролью посетителя при инициализации базы данных;
- INIT_USER_NAME - имя обычного пользователя с ролью посетителя при инициализации базы данных;
- INIT_USER_LASTNAME - фамилия обычного пользователя с ролью посетителя при инициализации базы данных;
- INIT_USER_EMAIL - электронная почта обычного пользователя с ролью посетителя при инициализации базы данных;
- INIT_ADMIN_PASSWORD - пароль администратора при инициализации базы данных;
- INIT_SYSTEM_PASSWORD - пароль специального системного пользователя при инициализации базы данных;
- INIT_DIRECTOR_PASSWORD - пароль пользователя с ролью директора при инициализации базы данных;
- INIT_USER_PASSWORD - пароль обычного пользователя с ролью посетителя при инициализации базы данных;
- DEBUG_MODE - должен ли сервис быть запущен в режиме отладки, влияет на создание логов.

### 2.5 Проверка запуска сервиса авторизации
Для проверки запущенного сервиса, можно открыть автоматическую интерактивную документацию API, предоставленную [Swagger UI](https://swagger.io/), 
для этого в адресной строке браузера следует ввести http://localhost:8001/docs. 

Либо можно открыть страницу авторизации, для этого следует ввести http://localhost:8001/index.

### 2.6 Принцип работы

Принцип работы сервиса авторизации состоит в выдаче специального токена, в ответ на верно указанные логин и пароль. Далее,
уже, при обращении к ресурсам, вместо логина и пароля предоставляется этот токен, который в зашифрованном виде содержит 
в себе информацию и о пользователе, и о дополнительных правах. Для дальнейшей верификации токена вновь происходит обращение к 
сервису авторизации, но на этот раз для получения информации об истинности токена и выданных на этот токен правах доступа.
Такая схема позволят минимизировать шансы компрометации пароля, а также, за счёт настраиваемого срока жизни этого токена,
как правило, довольно короткого срока, минимизировать шансы перехвата этого токена и использования его в несанкционированных действиях.
Так как токен доступа имеет, как правило, довольно короткий срок службы, то вместе с токеном доступа выдаётся и токен обновления,
который используется только для получения нового токена доступа, когда срок службы токена доступа истечёт. Обычно эта
процедура происходит в автоматическом режиме, и не требует дополнительных действий от пользователя. Токен обновления тоже 
имеет свой срок жизни, он несколько больше чем у токена доступа, поэтому тоже периодически обновляется. Так как токен 
обновления используется только для обновления токена доступа, то есть относительно редко, то шансы перехватить его небольшие.
Но даже если возникнет подозрение компрометации какого либо из токенов, любой из них, или даже их всех, можно отозвать.

### 2.7 Получение токенов
Теперь конкретная логика работы данного сервиса. 

Пользователь открывает страницу авторизации, где в форме авторизации указывает логин, пароль, и scope - сфера планируемого 
доступа к ресурсам. Scope позволяет в дальнейшим ограничить или наоборот расширить возможности авторизированного пользователя. 
Разумеется при авторизации можно проверить, могут ли для данного пользователя быть выданы такие разрешения. Сервис после 
получения логина и пароля находит в своей базе данных указанного пользователя, проверяет, что он не заблокирован и не удалён, 
проверяет верность ввёдённого пароля, и если всё нормально, то формирует [*JWT (JSON Web Token)*](https://jwt.io/introduction) 
токен доступа и ***JWT*** токен обновления. 

JWT токен доступа, как можно понять из его названия, имеет в своей основе JSON, а значит содержит информацию. В частности, 
в качестве информации он принимает: владельца токена, то есть на кого он выдан; кто выдал токен; время когда этот токен 
был выдан; время когда этот токен станет валидным; время жизни, то есть когда этот токен перестанет быть валидным (время протухания); 
тип токена, в данном случае является ли он токеном доступа или токеном обновления; строка, определяющая уникальный идентификатор 
данного токена, в данном случае реализована в виде [*UUID*](https://docs.python.org/3/library/uuid.html), который также 
является первичным ключом в таблице базы данных, хранящих информацию о выданных токенах; ну и кроме этого он может хранить 
и другую полезную информацию, и в качестве другой информации я сохраняю в токене информацию о scope, указанный во время авторизации.
Далее с помощью библиотеки [PyJWT](https://pyjwt.readthedocs.io/en/latest/) эта и другие части данных токена кодируются 
с применением алгоритма шифрования [Base64](https://ru.wikipedia.org/wiki/Base64), формируется подпись, в моём случае 
с помощью алгоритма *HS256* и с использованием секретного ключа, компонуются и формируется токен. В моём случае, для удобства, 
секретный ключ просто расположен в конфигурационном файле, в реальном же проекте его лучше разместить где-нибудь в более 
укромном месте, так как именно этот ключ далее поможет проверить валидность подписи токена.

Сразу же формируется и токен обновления, с очень похожим содержимым, за исключением: типа токена, это всё-таки уже токен доступа;
времени жизни токена, он несколько больше чем у токена доступа; уникального идентификатора, он у каждого токена свой. После 
того как токены будут сформированы они сохраняются в базу данных, где их там будет легко найти по уникальному идентификатору
или, при желании, по владельцу. И далее эти токены (доступа и обновления), а так же тип авторизационного токена - bearer, 
возвращаются в ответ на введённый логин и пароль.

### 2.8 Проверка токена доступа

У сервиса авторизации имеется API-функция [get_user](https://github.com/Paradox81ru/FastAPI_OAuth2/blob/main/OAuth2/Auth/routers/auth.py),
которая ожидает получение запроса с наличием в заголовке параметра *Authorization*, содержащим токен, предварённый типом 
авторизационного токена - *Bearer*. Проверив тип авторизационного токена, из значения выбирается только сам токен. Далее,
с помощью библиотеки [*PyJWT*](https://pyjwt.readthedocs.io/en/latest/), вновь используя секретный ключ и тот же алгоритм, 
что использовался для формирования подписи (*HS256*), токен расшифровывается, проверяя его валидность - подпись, и проверяя не истёк ли срок 
жизни токена. Если при расшифровке токена библиотека ***PyJWT*** не вернула исключение, значит предоставленный токен доступа 
валидный и действующий. В этом случае из содержимого расшифрованного токена в начале проверяется тип токена, предоставленный
токен должен быть именно токеном доступа. Далее проверяется наличие данного токена в хранилище выданных токенов, по его 
уникальному идентификатору. Это важная, дополнительная проверка на валидность. Если такой токен в хранилище обнаружен не будет, 
значит, возможно, он по какой-то причине был отозван и из хранилища удалён. В этом случае токен опять же будет считаться 
не валидным. Кроме этого токен проверятся на наличие владельца в своём содержимом. Если токен проверку на валидность не прошёл,
то будет вызвано исключение [AuthenticateException](https://github.com/Paradox81ru/FastAPI_OAuth2/blob/main/OAuth2/Auth/exceptions.py), 
которое наследуется от исключения [*HTTPException*](https://fastapi.tiangolo.com/ru/reference/exceptions/) и приведёт к 
возврату в ответе ошибки с кодом **401**, и сообщением, описывающем причину возникновения ошибки.

Если токен успешно прошёл проверку на валидность, то из содержимого токена берётся информация о владельце токена, и о scope,
используемый при авторизации пользователя. По владельцу токена в базе данных находиться информация о пользователе, и проверяется,
что пользователь в данный момент не удалён и не заблокирован. Если всё нормально, то информация о пользователе и scope возвращается
в ответ на запрос *get_user*.

### 2.9 Обновление токена доступа

У сервиса авторизации также имеется APi-функция [token-refresh](https://github.com/Paradox81ru/FastAPI_OAuth2/blob/main/OAuth2/Auth/routers/auth.py),
которая позволяет обновить просроченный токен доступа. Для этого он ожидает получение запроса с наличием в заголовке параметра 
*Authorization*, содержащим токен, предварённый типом авторизационного токена - *Bearer*, аналогично проверке токена в API-функции
*get_user*. Но на этот раз ожидается, что тип переданного токена будет именно типом токена обновления. Валидация и расшифровка
содержимого токена обновления, происходит так же, как и валидация и расшифровка содержимого токена доступа. Если валидация
токена обновления пройдёт успешно, то из содержимого токена обновления берётся информация о его уникальном идентификаторе,
владельце токена и scope. Владелец и scope нужны, чтобы вернуть эту информацию в новые создаваемые токены доступа и обновления.
А уникальный идентификатор нужен, чтобы сразу удалить информацию об уже заменённом токене обновления из базы данных, сделав
предыдущий токен обновления не валидным. Информация о просроченном токене доступа пока остаётся в базе данных, но это ничего
страшного, ведь этот токен всё равно уже просрочен и воспользоваться им уже нельзя. Просто потом надо создать задачу, которая бы
удаляла всё просроченный токены из базы данных, функция для этого уже есть: [remove_expire_token](https://github.com/Paradox81ru/FastAPI_OAuth2/blob/main/OAuth2/Auth/db/models/jwt_token_manager.py).
Обновлённые токены готовы, и они возвращаются аналогично новым токенам при первичном получении.

## 3. Проект OAuth2_test

Проект [OAuth2_test](https://github.com/Paradox81ru/FastAPI_OAuth2/tree/main/OAuth2_test) - это небольшой сайт, созданный
на фреймворке ***FastAPI*** и демонстрирующий возможности использования удалённого сервиса авторизации, для управления ограничениями
при доступе к своим ресурсам.

### 3.1 Запуск вручную

Если у Вас установлен интерпретатор [*Python*](https://www.python.org/) версии <ins>3.12</ins>, то, так же как и сервис авторизации ***OAuth2***,
можно вручную запустить сайт проверки сервиса авторизации - ***OAuth2_test***. Для этого надо просто создать виртуальное
окружение, установить в него пакеты из файла *requirements.txt* данного проекта, активировать виртуальное окружение и 
запустить файл main.py: `python main.py`. Так же можно запустить сайт через ***uvicorn*** с помощью команды 
`uvicorn main:app --host localhost --port 8000`. Предыдущий вариант запуска сайта открывает сайт с такими же параметрами,
хотя здесь значения порта уже особого значения не играет, это повлияет только на открытие сайта в браузере.

### 3.2 Запуск с помощью docker

Сайт ***OAuth2_test*** так же можно запустить в [***docker***](https://www.docker.com/), но, так как уже упоминалось ранее, проект оптимизирован для 
запуска его целиком с помощью ***docker-compose***, поэтому, для того чтобы запустить данный проект в ***docker***, 
надо внести небольшие изменения в файл [Dockerfile](https://github.com/Paradox81ru/FastAPI_OAuth2/blob/main/OAuth2_test/Dockerfile).
Изменений немного, надо раскомментировать три переменные - *ENV* значения, и раскомментировать, собственно, сам запуск
сайта, последнюю строку - `CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]`. Всё, контейнер можно 
создавать и запускать. Ещё раз напоминаю, что в случае запуска проектов через ***docker***, запускать оба контейнера надо 
в одной сети докера.

### 3.3 Запуск с помощью docker-compose

И, конечно, самое простое, это запуск проекта целиком с помощью [***docker-compose***](https://docs.docker.com/compose/). Всё аналогично пункту
**2.3** данной документации.

### 3.4 Переменные окружения сайта проверки сервиса авторизации
Сайт проверки сервиса авторизации имеет в своём распоряжении всего три переменные:
- AUTH_SERVER_HOST - хост микросервиса авторизации, url адрес, по которому сайт будет пытаться связываться для проверки токена доступа;
- AUTH_SERVER_PORT - порт микросервиса авторизации, по которому сайт будет пытаться связываться для проверки токена доступа;
- DEBUG_MODE - должен ли сайт быть запущен в режиме отладки, влияет на создание логов.

Самые важные здесь первые две переменные окружения, если они будут неправильно определены, то при попытке проверки доступа 
к ресурсам будет возвращаться ошибка *"The OAuth2 authorization server is unavailable"*. По умолчанию все параметры настроены 
так, чтобы сайт мог успешно проверять доступ к ресурсам.

### 3.5 Проверка запуска сервиса авторизации

Для проверки запущенного сайта, можно открыть автоматическую интерактивную документацию API, предоставленную [Swagger UI](https://swagger.io/), 
для этого в адресной строке браузера следует ввести http://localhost:8000/docs. 

Либо можно сразу открыть главную страницу проверки авторизации, для этого следует ввести http://localhost:8000/index.

### 3.6 Принцип работы

Принцип работы с удалённым сервисом авторизации, состоит в передаче токена доступа на проверку OAuth2 сервису на специальную
API-функцию. В ответ на запрос ***OAuth2*** сервис либо возвращает код **200**, с данными пользователя, на которого выписан 
токен, и scope, либо код ***401*** с информацией о причине отказа в авторизации.

В распоряжении сайта для проверки авторизации находятся 9 ресурсов - это обычные API-функции, при успешной авторизации которые
возвращают информацию об авторизованном пользователе и его роли. К основному эапускаемому экземпляру класса FastAPI подключен
[AuthenticationMiddleware](https://github.com/Paradox81ru/FastAPI_OAuth2/blob/main/OAuth2_test/main.py),
который для проверки авторизации использует класс [JWTTokenAuthBackend](https://github.com/Paradox81ru/FastAPI_OAuth2/blob/main/OAuth2_test/fastapi_site/middlewares/authentication.py),
реализующий специальный интерфейс абстрактного класса [*AuthenticationBackend*](https://fastapi-contrib.readthedocs.io/en/latest/fastapi_contrib.auth.html).
При обращении к какому-либо ресурсу сайта этот класс, прежде чем будет предоставлен ресурс, проверяет в заголовке наличие
параметра *Authorization*, содержащий токен, предварённый типом авторизационного токена - *Bearer*. Если параметра *Authorization*
в заголовке нет вообще, то считается, что к ресурсам обращается не авторизованный пользователь, и возвращается анонимный 
пользователь с ролью "Гость". Иначе из поля выбирается токен, который передаётся для проверки на API функцию сайта 
авторизации *get_user*. Там этот токен проверяется на валидность, и если всё нормально, то сервис авторизации в ответ вернет
информацию о пользователе, на которого этот токен был ранее создан, и scope, который находиться внутри содержимого токена.
Получив эту информацию, реализованный интерфейс ***AuthenticationBackend*** добавляет её в запрос Request, и доступ к 
авторизованному пользователю становиться доступным для всёх ресурсов сайта. Далее, используя полученную информацию,
сайт проверяет доступ к ресурсу, к которому было обращение. Для этого используются четыре [функции - зависимости](https://github.com/Paradox81ru/FastAPI_OAuth2/blob/main/OAuth2_test/fastapi_site/dependencies.py):
*check_scope*, *check_role*, *is_auth* и *is_anonym_user*.
- check_scope - предоставляет доступ к ресурсу только при наличии указанного при авторизации параметра scope, или 
комбинации нескольких scope;
- check_role - предоставляет доступ только пользователям с указанной ролью, или ролью, входящей в список разрешённых
к доступу к ресурсу ролей;
- is_auth - предоставляет доступ к ресурсу только любому авторизованному пользователю;
- is_anonym_user - предоставляет доступ к ресурсу только не авторизованному пользователю.
Все эти ***функции - зависимости*** добавляются к функциям реализующие доступ к какому-либо ресурсу, с требуемыми для
ограничения параметрами.

## 4. Проверка работы сервиса с помощью визуального интерфейса

Для визуальной проверки сервиса авторизации, надо любым из удобных, вышеописанных способов, запустить в веб-сервере сервис 
авторизации и сайт для проверки авторизации. После этого в браузере надо открыть оба сервиса на странице *index*. 
Например, для сервиса OAuth2 http://127.0.0.1:8001/index, после чего в браузере откроется страница **Главная страница 
микросервиса авторизации OAuth2**. А для сайта проверки http://127.0.0.1:8000/index, после чего в браузере откроется 
страница **Главная страница проверки авторизации OAuth2**.

На странице сервиса авторизации находиться форма для авторизации, представляющая собой два поля **Имя** и **Пароль**, и, ниже,
несколько чекбоксов, представляющие собой **Область действия**, или по другому **scope**. Для получения токена авторизации надо
указать верные **логин** и **пароль**, а также необходимую **Область действия**, **scope**. Какие в базе данных есть логины и пароли, 
можно проверить в переменных окружения. После ввода логина и пароля нужно нажать кнопку **Запрос токенов**, или просто
нажать **Enter**. Кроме формы авторизации на странице так же присутствуют два больших поля - **Токен доступа** и 
**Токен обновления**. Если логин и пароль были указаны верно, то именно в них появятся выданные на указанного пользователя
токен доступа и токен обновления. Для начала нас интересует токен доступа, который нужно скопировать в буфер.

После того как токен доступа получен, надо перейти на страницу проверки авторизации. Там есть поле **Токен доступа**, именно
в него надо вставить скопированный в буфер полученный ранее токен доступа. Ниже расположено большое поле **Информация о пользователе**.
После того как будет нажата кнопка **Получить информацию пользователя**, в этом поле отобразиться информация о пользователе,
токен которого был указан. Так же в этом поле будет указана информация об указанном при авторизации Области действия,
если, конечно, она была указана.

Справа расположены восемь кнопок, имитирующие доступ к ресурсам с ограничением доступа. При нажатии на каждую из них можно 
увидеть результат: **Ok**, если доступ к данному ресурсу по введённому токену разрешён, или **Invalid**, если доступ запрещён.

Иногда при попытке получить информацию пользователя, может появиться сообщение об ошибке: **Error: Unauthorized. The JWT token is expired**.
Это значит, что срок жизни токена доступа истёк. В этом случае надо вернуться на **Главную страницу микросервиса авторизации
OAuth2**, и нажать кнопку **Обновление токенов**. При этом не забудьте убедиться, что токен обновления всё ещё указан в поле
**Токен обновления**. После нажатия кнопки **Обновление токенов**, в соответствующих полях появятся новые токен доступа 
и токен обновления. Всё, можно снова скопировать токен доступа, вернуться к сайту проверки сервиса авторизации, заменить
в поле **Токен доступа** старый токен на новый и дальше проверять доступ к ресурсам.
