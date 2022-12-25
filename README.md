# A Simple CRUD API

## Introduction
This is a simple Create, Read, update and Delete API based in Django with user authentication.

## Description
* The User authentication leverages the JsonWebTokens (JWT) package to provide security in transit. 
* The Creation of a Post (POST request), Update and Delete, require authentication. View one and View all require no authentication. 
* User Authentication and Password reset implemented as well.

## Running locally 
* Create a virtual environment
* Clone the project 
* Install required dependencies with `pip install -r requirements.txt`
* To avoid having to setup PostgreSQL on your local machine, edit the `slightlytechie/settings.py` file and remove the PostgreSQL section and enable the sqlite3 section with the following 

         "ENGINE": "django.db.backends.sqlite3",

         "NAME": BASE_DIR / "db.sqlite3",
* Run migrations (Migrations should already exist) with `python manage.py migrate`
* Run the local server with `python manage.py runserver 0.0.0.0:8041`
* Visit the Swagger API documentation on `http://localhost:8041/api/docs/`
* Create a superuser with `python manage.py createsuperuser` and fill out the information in the prompt
* Login to the admin in the browser via `http://localhost:8041/admin/`
* To run tests, run `python manage.py test`


## Running in Docker Compose
* Clone the project
* Make sure docker and docker-compose are installed on your system
* From the root of the project run the following to build and start `docker-compose up --build`
* Once the container starts, access the Swagger API documentation via `http://localhost:8041/api/docs/`
* Run the following command to create a superuser `docker-compose exec -it app python manage.py createsuperuser` and follow the prompt
* Login to the admin in the browser via `http://localhost:8041/admin/`
* To run the tests, run `docker-compose exec -it app python manage.py test`
* PostgreSQL is used and the exposed on port 5435 on localhost


## Sample 
A sample is deployed on Python Anywhere. Below is the link to the Swagger Documentation of the API
[https://vixion.pythonanywhere.com/api/docs/](https://vixion.pythonanywhere.com/api/docs/)

## END