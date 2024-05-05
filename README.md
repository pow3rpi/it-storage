# IT-storage 🗄️

## Description
Online service for storing and managing favorite content such as links, tutorials etc., 
which has convenient search and tagging systems.


## Features
- REST API service with SOLID and clean architecture principles applied
- Asynchronous working principle
- Quick database migrations
- JWT tokens for authorization
- Email service as a micro-service with background tasks
- Content search with different filters
- Tagging system
- Frontend as a single page application (SPA)
- Router with protected pages (which require authorization)
- Logging system


## Quick Start
Here, on GitHub you can see a development version of the application which can be easily 
deployed locally on your machine.

To run the application you should do the following:
1. Clone repository:
    ```
    git clone git@github.com:iurii-umnov/it-storage.git
    ```
2. Configure your Gmail account to use [Gmail API] with SMTP protocol.
3. In **root**, **API**, **Background** and **Frontend** directories create **.env** files 
and fill them according to corresponding **.env.template** files in the same directories.
    * example for **root .env**:
       ```
       POSTGRES_DB=db_name
       POSTGRES_USER=user
       POSTGRES_PASSWORD=password
       ```
    * example for **API/.env**:
       ```
       ACCOUNT_ACTIVATION_URL=http://127.0.0.1:5000/api/v1/activate_account
       ACCESS_TOKEN_EXPIRE_MINUTES=1440
       REFRESH_TOKEN_EXPIRE_MINUTES=10080
       ALGORITHM=HS256
       JWT_SECRET_KEY=kkbhaksdbyvcefdakbsvdvuywvwy27364tgi
       JWT_REFRESH_SECRET_KEY=akfnasnubaflsjcs234alfbmands81299h
       SIGN_UP_VERIFICATION_LINK_EXPIRE_MINUTES=120
       SQL_USER=user
       SQL_PWD=password
       SQL_PORT=5432
       SQL_HOST=postgres
       SQL_DATABASE=db
       CELERY_NAME=tasks
       CELERY_BROKER_URL=redis://redis:6379/0
       CELERY_RESULT_BACKEND=redis://redis:6379/0
       ```
    * example for **Background/.env**:
       ```
       CELERY_NAME=tasks
       CELERY_BROKER_URL=redis://redis:6379/0
       CELERY_RESULT_BACKEND=redis://redis:6379/0
       EMAIL_HOST=smtp.gmail.com
       EMAIL_PORT=465
       EMAIL_FROM=example@gmail.com
       EMAIL_PASSWORD=dimwpaqqzshjgzca
       ```
    * example for **Frontend/.env**:
       ```
       GENERATE_SOURCEMAP=false
       BROWSER=none
       ```
4. Run the command:
    ```
    docker-compose up -d
    ```
5. Open your application on http://127.0.0.1:3000.


## Tech
This project uses a number of open source projects to work properly:

### Frontend
- [HTML] - language for web layout
- [CSS] - language for applying custom styles to HTML pages
- [Bootstrap] - CSS framework for quick page layout
- [JavaScript] - language for developing frontend functionality
- [React.js] - JavaScript framework for developing web UI

### API
- [Python] - the main language of the project
- [FastAPI] - python asynchronous framework for web development
- [PostgreSQL] - main database
- [SQLAlchemy] - database interaction (queries)
- [Alembic] - database migrations
- [Dependency Injector] - python framework for implementing dependency injection principle
- [JWT] - authorization tokens
- [Pydantic] - input/output data (scheme) validation
- [Docker] - quick deployment

### Background tasks (Email Service)
- [Celery] - background tasks
- [Redis] - database for proper work of [Celery]


## Services

### Authorization 
This is an internal service which uses [JWT] tokens for users authorization. It is configured in such a way 
that tokens are stored in secured http only cookies which means that they cannot be accessed from frontend
(through JavaScript).

### Email
Email service is realised as a background micro-service, using [Celery] and [Redis].\
\
It is implemented with the help of [Gmail API] which allows you to send emails directly from the code, using such 
programming languages as Python, Java, JavaScript, Go or Node.js. The only thing you need is google account and slight 
configuration.

### Search
Search service allows users to apply convenient content search using different filters and tag system. 
This functionality is not yet organised as a separate service but in the future with the development of 
search system it will.


## Deployment
[Docker] and [Docker Compose] are used to run the application and dependent services in containers. 
See **docker-compose.yml** in the root directory for more details.\
\
The docker-compose file contains the following services/containers:
- **frontend**: React application
- **redis**: Redis service
- **celery-worker**: Background tasks (Email service)
- **postgres**: PostgreSQL service (main database)
- **api**: main FastAPI application


## License
This project is open source and MIT Licensed.


[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job.)

  [Python]: <https://www.python.org/>
  [FastAPI]: <https://fastapi.tiangolo.com/>
  [HTML]: <https://html.com/>
  [CSS]: <https://www.css3.com/>
  [Bootstrap]: <https://getbootstrap.com/>
  [JavaScript]: <https://www.javascript.com/>
  [React.js]: <https://react.dev/>
  [PostgreSQL]: <https://www.postgresql.org/>
  [SQLAlchemy]: <https://www.sqlalchemy.org/>
  [Alembic]: <https://alembic.sqlalchemy.org/en/latest/>
  [Dependency Injector]: <https://python-dependency-injector.ets-labs.org/>
  [JWT]: <https://jwt.io/>
  [Pydantic]: <https://docs.pydantic.dev/latest/>
  [Celery]: <https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html>
  [Redis]: <https://redis.io/>
  [Docker]: <https://docs.docker.com/>
  [Docker Compose]: <https://docs.docker.com/compose/>
  [Gmail API]: <https://developers.google.com/gmail/api/guides?hl=en>