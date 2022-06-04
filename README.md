# Django-DynamoDb-Lambda-function

[![Join the chat at https://gitter.im/nubar-api/django-dynamodb-lambda-function](https://badges.gitter.im/nubar-api/django-dynamodb-lambda-function.svg)](https://gitter.im/nubar-api/django-dynamodb-lambda-function?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

This will be a simple Django REST API, which uses AWS Dynamodb as its schemaless database. Next we will deploy on Zappa utilising AWS's Lambda function.
We use pynamodb, for its ORM, to write models and interface to Dynamodb database.

## Usage Instructions ##

First of all, install and create virtual environment:

` python -m venv .venv`

In Windows type:

`.venv\Scripts\activate`

In Mac/Linux type:

 `source venv/bin/activate`

Install required packages

 `(venv) > pip install -r requirements.txt`


<br/>

# Setup Django RESTapi project
## Folder structure

```
project
│   README.md
│   env.py
│   manage.py
|   .env.example
|   .env.local
│   .env.dev
│   .env.prod
│
└───django_dynamodb_lambda_function/api
│   │   __init__.py
│   │   asgi.py
│   │   settings.py
|   |   urls.py
│   |   wsgi.py
|
└───apps
|   └───productionLine/     # django-app
|   |   └───actions/      # actions on productionline items
|   |   └───migration/
|   │   │   __init__.py
|   |   |   admin.py
|   |   |   apps.py
|   |   |   dynamodb_interface.py
|   │   │   models.py
|   │   │   urls.py
|   |   |   views.py
|   |
|   └───products/   # django-app
|   |
│   └───contactUs/  # django-app
```

# Setup environments
AWS provides downlodable version of dynamodbb which can be used for development purposes on local machine.
So, used [django-environ]() to setup separate environments for local machine development(`.env.local`), cloud hosted development(`.env.dev`) and production environment(`.env.prod`).

>`pip install django-environ `



setup in a separate `env.py` file:

```java
import environ
env = environ.Env()
ENVIRONMENT = os.environ.get('ENV')
if ENVIRONMENT == 'local':
   env.read_env(str(BASE_DIR / '.env.local'))
elif ENVIRONMENT == 'dev':
   env.read_env(str(BASE_DIR / '.env.dev'))
elif ENVIRONMENT == 'prod':
   env.read_env(str(BASE_DIR / '.env.production'))

DB_HOST = env.str('DB_HOST')
DB_REGION = env.str('DB_REGION')
SECRET_KEY = env.str('SECRET_KEY')
DEBUG = env.str('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
CORS_ALLOWED_URL = env.list('CORS_ALLOWED_ORIGINS')
LOGGING_HANDLERS = env.list('LOGGING_HANDLERS')
DJANGO_LOG_LEVEL = env.str('DJANGO_LOG_LEVEL', 'INFO')
DJANGO_LOG_FILE = env.str('DJANGO_LOG_FILE')
```


next import these environment variables inside django `settings.py` file.

# Setup Dynamodb

## Setup for Local machine
>AWS provides downladable version of dynamodb, allowing a developer to experiment without any fear to mess something up. Use [this link](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html) to setup **[Dynamodb](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html)** on your local machine.

To start a **dynamodb server on your local machine**:

    put-in following command in your powershell:
    > cd path\to\aws\dynamodb_local_latest

    > java -D"java.library.path=./DynamoDBLocal_lib" -jar DynamoDBLocal.jar -dbPath path\to\write\database_file folder
By default the dynamodb-server runs at http://localhost:8000

Next setup your `.env.local` [file](F:\huha\myGit\Django-DynamoDb-Lambda-function\.env.example).

```js
SECRET_KEY='your-django-secret-code'
DEBUG=TRUE
DB_HOST=http://localhost:8000
DB_REGION='ap-south-1'
ALLOWED_HOSTS=127.0.0.1,localhost,localhost:8080
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
...
```
and provide the following environment variable from console :
> `$env:ENV = "local"`

Next, to run the **django local server**:

    From console cd to your django project directory and enter:
> `python manage.py runserver 8080`

## Setup for Dynamodb web service
 Follow the instructions provided on [AWS website](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/SettingUp.DynamoWebService.html).
 We used it in our development environment. With relevant environment variables fixed inside `.env.dev` file.
```js
...
DB_HOST=https://dynamodb.ap-south-1.amazonaws.com
DB_REGION=ap-south-1
...
```
and provide the following environment variable from console :
> `$env:ENV = "dev"`

Next, to run the **django local server**:

    From console cd to your django project directory and enter:
> `python manage.py runserver 8080`

### [Pynamodb](https://pynamodb.readthedocs.io/en/latest/index.html)
"PynamoDB is a Pythonic interface to Amazon’s DynamoDB. By using simple, yet powerful abstractions over the DynamoDB API..."

 If you are familiar with django's style of model, serialiser and class definition of views you can readily setup your RESTapi backend using [pynamodb API](https://pynamodb.readthedocs.io/en/latest/api.html).

## Deploying on Lambda-function

### Cloud hosted dynamodb setup 

setup aws account and get on with free acccess for a year

settings for aws region,..

## Zappa Deployment

setup iAM roles, policies and permissions

zappa init

zappa settings

## logging

for local development

using aws's cloudfront services

