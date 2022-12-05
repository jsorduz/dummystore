# django-basic-template
This is a django basic template for future projects

## Branches
This repository has the following branches:
- **main**: basic django template with:
    - basic mixin models with UUIDv4, created_at and updated_at
    - Custom user
    - Custom command to initialize superuser
    - Additional logger
    - Linters (flake8, mypy, pylint)
    - Pytest and Coverage
    - Docker compose deploy scripts
- **restapi**: django REST framework template with:
    - basic django template features
    - django REST framework
    - jwt auth
- **celery**: django celery template with:
    - django REST framework template features
    - celery

## Local deployment
To deploy the repository locally use the following commands:
```sh
python -m venv .venv
pip install -r requirements_dev.txt
python manage.py migrate
python manage.py runserver
```

To create a superuser use:
```sh
python manage.py createsuperuser
```

To use the linters export the **.env.template** environment variables appropiate for your local environment and run:
```sh
apps="config common app_*"
black $(echo $apps)
isort $(echo $apps)
flake8
mypy $(echo $apps)
pylint $(echo $apps)
```
To run the tests:
```sh
coverage run --source='.' manage.py test $(echo $apps)
coverage report
```

### Pseudo productive deployment
Use docker-compose to deploy a pseudo productive environment that inclues
- gunicorn django deployment
- postgresql db
- nginx reverse proxy

```sh
docker-compose build
docker-compose up
