<H1>ES Easy Shop</H1>
Description

## Project requirements

* docker >= 20.10.21
  ```docker --version```
* docker-compose >= v2.12.2
  ```docker-compose --version```
* python >= 3.10
  ```This is the case when you start the project without docker-compose```
* PostgreSQL >= 15 
```this is the case when you start the project without docker-compose```
## Development Environment Set Up
### Start project directly on your host
#### Virtual Environment Set up
```bash
  python -m venv <path_to_env>
  source <path_to_env>/bin/activate
```

#### Initialize database

```bash
  python manage.py makemigrations
  python manage.py migrate
```

#### Start API on localhost
```bash
python manage.py runserver
```

### Start project using docker-compose [This is preferred way]

#### Build and start containers

This will fetch/build images and start containers. Migration command will be run during startup.

```bash
  docker-compose up --build
```

#### Working with running container

* When container is running

```bash
docker-compose exec web_api <your_command>
```

* Without running container

```bash
docker-compose run --rm web_api <your_command>
```

You can run any command you would run on you host machine...
<your_command> examples:

* python manage.py makemigrations
* python manage.py migrate
* python manage.py startapp <app_name>
* python manage.py createsuperuser