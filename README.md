# Event Web App

Yet another assignment; an entry task. This time to build a SPA web app in Django. I didn't have enough time to use React for the frontend, so it was old school html and Js + ajax with Django's templating features.

## Requirements
* Build and event web app in Django WITHOUT using the Django's Admin module, User module or Django Rest Framework
* Users should be able to search, join, like and comment on events
* Admin users should be able to manage events (CRUD), upload images


## SETUP

### Local Python environment settings: 
````
conda create --name event_app python=3.7
source activate event_app
pip install -r requirements.txt
````
* Events app src code in `./src` 

* Test related scripts in `./test`



### Nginx:
* Used `nginx:1.14` docker image as reverse proxy
### Mysql:
* Used `bitnami/mysql:5.7` docker image for MySql database


# Deployment
- see `Dockerfile` and deployment related files in `./deployment`
- `./wait-for-it.sh` is a pure bash script that will wait on the availability of a host and TCP port. (see https://github.com/vishnubob/wait-for-it)
 

### Deployment helper scripts:
* `init-deployment.sh`:
   * Builds and saves image as tar file
   * copy `./deployment` folder into server
   * runs `docker stack deploy -c docker-compose.yml ${stack_name}
   `
* `admin-setup-script.sh`:
   * creates 1 staff account to login, username and password specified in `./deployment.env`


