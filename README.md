# **TODO**
Description:
This is Test task done by Yaroslav Potapchuk for Disoft recruiting process.
Whole TODO app is build on djnago along with drf and usage of docker containers to manage and build db.
### Setup Project
1. Install python3.10
2. Create venv `python3 -m virtualenv venv -p python3.10` and activate `source ./venv/bin/activate`
3. Install dependency `pip install -r requirements.txt`
4. Run command migrate `python manage.py migrate && python manage.py loaddata task/fixtures/create_default_statuses.json` and run server `python manage.py runserver` http://127.0.0.1:8000


### Docker Compose 
All db (postgresql) set up is done through docker compose network.
Both db and django service configured in docker-compose.yml
1. Install docker and docker-compose https://docs.docker.com/get-docker/ https://docs.docker.com/compose/install/
2. Run this command `docker-compose -f ./docker-compose.yml up --build`
3. Let's go on url http://0.0.0.0/

Create super user: 
```
    docker exec -it web sh
    python manage.py createsuperuser
    ... input paraments
    exit
```
Before working with api or reading docs make sure to create user: http://127.0.0.1:8000/users/sign-up/
and sign-in: http://127.0.0.1:8000/users/sign-in/
Let's login in api: https://0.0.0.0/admin/