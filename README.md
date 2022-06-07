# Django-DynamoDb-Lambda-function
This will be a simple Django REST API, which uses AWS Dynamodb as its schemaless database. Next we will deploy on Zappa utilising AWS's Lambda function.
We use pynamodb, for its ORM, to write models and interface to Dynamodb database.

![GitHub Repo stars](https://img.shields.io/github/stars/RahulPrakash11/Django-DynamoDb-Lambda-function?style=social)
![GitHub](https://img.shields.io/github/license/RahulPrakash11/Django-DynamoDb-Lambda-function)
![](https://img.shields.io/badge/Python-3.7-red)
![](https://img.shields.io/badge/Django-3.2-green)
![](https://img.shields.io/badge/Deployment-LambdaFunction-yellow)
![](https://img.shields.io/badge/Database-Dynamodb-orange)

<br>

# Index

- **[Installation Instructions](#installation-instructions)**<br>
- **[Usage Instructions](#usage-instructions)**<br>
- **[Setup Django RESTapi project](#setup-django-restapi-project)**<br>
   - **[Folder Structure](#folder-structure)**<br>
- **[Setup Multiple Environments](#setup-multiple-environments)**<br>
- **[Setup Dynamodb](#setup-dynamodb)**<br>
  - **[Setup for Local machine](#setup-for-local-machine)**<br>
  - **[Setup for Dynamodb web service](#setup-for-dynamodb-web-service)**<br>
  - **[Using Pynamodb](#using-pynamod)**<br>
- **[Deploying on Lambda-function](#deploying-on-lambda-function)**<br>
  - **[Setup AWS resources](#setup-aws-resources)**
  - **[Zappa Deployment](#zappa-deployment)**
- **[Logging](#logging)**<br>
- **[Further Help](#further-help)**<br>
- **[License](#license)**<br>

<br>

# Installation Instructions #

First of all, install and create virtual environment:

` python -m venv .venv`

In Windows type:

`.venv\Scripts\activate`

In Mac/Linux type:

 `source venv/bin/activate`

Install required packages

 `(venv) > pip install -r requirements.txt`

<br>

# Setup Django RESTapi project #

## Folder Structure

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
│       __init__.py
│       asgi.py
│       settings.py
|       urls.py
│       wsgi.py
|
└───apps
    └───productionLine/     # django-app
    |   └───actions/      # actions on productionline items
    |   └───migration/
    │       __init__.py
    |       admin.py
    |       apps.py
    |       dynamodb_interface.py
    │       models.py
    │       urls.py
    |       views.py
    |
    └───products/   # django-app
    |
    └───contactUs/  # django-app
```
<br>

# Setup Multiple Environments

We can setup multiple environments to isolate our requirement based phases in development process. For example **development environment and production environment**. `Development environment` will involve multiple iterations of trial and error, architecture changes, code flow changes etc. This will gradually evolve into a stable code base which can be deployed on cloud. The deployment happens inside a `production environment`, which has greater security concerns and stability.

In our present case as AWS provides downloadable version of dynamodb which can be used for development purposes on local machine. Which further elliminates the requirement of connecting to a cloud hosted database to test our backend bussiness logic.

So, we have setup an addditional environment called `local environment`, which uses AWS's dynamodb server, hosted and run on our local machine.

We have ussed [**django-environ**](https://pypi.org/project/django-environ/) to setup separate environments for local machine development environment(`.env.local`), cloud hosted development environment(`.env.dev`) and production environment(`.env.prod`).
```ps
pip install django-environ
```
<br>

Setup a separate `env.py` file, which fixes evironment variables:

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
Next setup your [`.env` files](.env.example), with values for respective environment variables.

1. Setup your `.env.local` file(Local Environment).

```js
SECRET_KEY='your-django-secret-code'
DEBUG=TRUE
DB_HOST=http://localhost:8000
DB_REGION='ap-south-1'
ALLOWED_HOSTS=127.0.0.1,localhost,localhost:8080
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
...
```
2. With development environment variables fixed inside `.env.dev` file.
```js
...
DB_HOST=https://dynamodb.ap-south-1.amazonaws.com 
DB_REGION=ap-south-1
...
```
3. Similarly `.env.prod` file.
   - Since, we are using Zappa to deploy our production ready code base, we wll fix many of the production environment variables inside the auto generated [zappa_settings.json](#todo)


Next import these environment variables inside django [`settings.py`](django_dynamodb_lambda_function\settings.py) file.

<br/>

# **Setup Dynamodb**
---
- First, Download [AWS CLI](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Tools.CLI.html#Tools.CLI.DownloadingAndRunning) and configure your AWS credentials for local and development environment.
                
```ps
    > aws configure 
        AWS Access Key ID : "your-access-key-id"
        AWS SECRET ACCESS KEY : "your-secret-key"
```

Make sure to use different IAM roles for deployment inside production environment and development environments, addressing security concerns.

- ## **Setup for Local machine**
>AWS provides downladable version of dynamodb, allowing a developer to experiment without any fear to mess something up. Use [this link](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html) to setup **[Dynamodb](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html)** on your local machine.

To start a **dynamodb server on your local machine**:

1. Put in following command in your powershell

```ps
    > cd path\to\aws\dynamodb_local_latest

    > java -D"java.library.path=./DynamoDBLocal_lib" -jar DynamoDBLocal.jar -dbPath path\to\write\database_file folder
```

By default the dynamodb-server runs at http://localhost:8000

Next, To run the **django local server**, from console cd to your django project directory. Provide the relevant environment variable from console and run:
```ps
> $env:ENV = "local"
> python manage.py runserver 8080
```
<br/>

- ## **Setup for Dynamodb web service**
 Follow the instructions provided on [AWS website](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/SettingUp.DynamoWebService.html).
 We used it in our development environment. 
First provide the following environment variable from console :
```ps
> $env:ENV = "dev"
> python manage.py runserver 8080
```

or you can setup the variables to be fixed dynamically inside [**Zappa settings file**](zappa_settings_example.json).

Next, run the **django local server** as done in local environment.

<br />

## Using [**Pynamodb**](https://pynamodb.readthedocs.io/en/latest/index.html)
---

"PynamoDB is a Pythonic interface to Amazon’s DynamoDB. By using simple, yet powerful abstractions over the DynamoDB API..."

 If you are familiar with django's style of **ORM(Object Relational Mapper)** model, serialiser and class definition of views you can readily setup your RESTapi backend using [pynamodb API](https://pynamodb.readthedocs.io/en/latest/api.html).

<br />

# Deploying on Lambda-function
---
## Setup AWS resources
---
Setup AWS account and confgure IAM roles, policies and permission so as to allow zappa to manage AWS resources for your API deployment.

References:
1. [How to create a serverless service in 15 minutes](https://blog.lawrencemcdaniel.com/serve-a-django-app-from-an-aws-lambda-function/)
2. [Creating a role to delegate permissions to an AWS service](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html)

you can check the AWS resources required for zappa deployment inside [zappa_settings_example.json](zappa_settings_example.json) file

<br>

## Zappa Deployment
---
Finally we deploy our RESTApi using [Zappa](https://github.com/zappa/Zappa). Why zappa?

1. Pay per usage
2. Round the clock availability, Zero charges for hosting.
3. minimal initial manual setup required
4. Built-in logging system

<br>

Setup steps:

```ps
> zappa init
> zappa deploy dev # for development server
> zappa deploy prod # for production environment
> zappa update <dev/prod> # to update changes in your code base
```
Made mistakes and want to start over. Simply undeploy and start over

```
zappa undeploy <dev/prod>
```
<br>

# Logging
---

- For local environment:
  Checkout [**env.py**](env.py)


- To log the development/production environment:

Run from your environment console:
```
zappa tail <dev/prod>
```

- Or, you can use AWS's [cloudfront services](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/AccessLogs.html) for cloud deployed logging.

<br>

# Further Help

This project is an open-source initiative by Junkie Labs team.

For any questions or suggestions send a mail to junkielabs.dev@gmail.com or chat with the core-team on gitter.

<br>

[![Gitter](https://badges.gitter.im/nubar-api/django-dynamodb-lambda-function.svg)](https://gitter.im/nubar-api/django-dynamodb-lambda-function?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

<br>

# License

[MIT License](https://github.com/RahulPrakash11/Django-DynamoDb-Lambda-function/blob/main/Licence).


<br>

## TODO

- add badge
- test zappa
