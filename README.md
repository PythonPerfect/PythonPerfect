# CITS3403-Project2
### "PythonPerfect"
Anthony Zao, Dhruv Jobanputra, Sandil Bhikha, Thobias Danudoro

## Table of Contents
1. [Introduction](#introduction)
2. [Assessment Mechanism](#Assessment-Mechanism)
3. [App Architecture](#App-Architecture)
4. [App Launching](#App-Launching)
5. [App Testing](#App-Testing)
6. [Design Process](#Design-Process)

## Introduction 
PythonPerfect is a Flask based web application designed to teach users the basics of the Python programming language. The website encourages users to learn the programming basics through the content page and assess their knowledge through the related quiz. ***Info on the quiz

Users are able to attempt multiple courses at the same time. Their progress is tracked and is viewable in the content page. Should the user be granted administrative priveleges, they will gain the ability to create new courses for others to attempt.

## Assessment Mechanism
****

## App Architecture (Flask)
This application has been constructed using the python Flask micro-framework MVC. In terms of the Model View Controller Architecture, in our application, the model is represented by the SQLite database and SQLAlchemy, the View is represented by the server-side rendering template of jinja2 which assembles the HTML static content based on the request and the Controller is represented by the Python Flask library.

## App Launching
To laucnh the application on your personal device it is recommended that you use a virtual environment. Python and virtualenv will need to be installed on your system. A detailed guide is provided below:

## Linux OS
#### Install Virtual Environment
```shell
$ pip3 install virtualenv
```
#### Activate Virtual Enviroment
```shell
$ python3 -m venv env
$ source env/bin/activate
```
#### Install required python packages
```shell
$ pip3 install -r requirements.txt
```
##### Configuring Flask
```shell
$ export FLASK_APP=PythonPerfect.py
```
#### Run Flask app
```shell
$ flask run
```

## On windows
#### Install Virtual Environment
```shell
> pip install virtualenv
```
#### Activate Virtual Enviroment
```shell
> python -m venv env
> ./env/Scripts/activate
```
#### Install required python packages
```shell
> pip install -r requirements.txt
```
##### Configuring Flask
```shell
> set FLASK_APP=PythonPerfect.py
```
#### Run Flask app
```shell
> flask run
```

## Setting Flask Environment and Debug/Testing modes
It is highly recommended to avoid setting flask environments by code
i.e. in config.py

Debug mode is by defult enabled when flask environment is set to development
#### Changing Flask Environments:
##### On windows
```shell
$ set FLASK_ENV=<environment>
```
##### On mac/linux
```shell
$ export FLASK_ENV=<environment>
```  
?! CHECK THIS ON LINUX/MAC SYSTEM

## Initialise SQLite database with flask-migrate

**If working on code post User login implementation**

```shell
$ flask db upgrade
```

to construct the existing database on your local device.

Instructions on migration repository initialisation omitted
#### Modifying databases
Create new migration script

```shell
$ flask db migrate
$ flask db upgrade 
```


**For large changes, please inspect the script first before pushing to git**

## Testing Users database
Flask shell context set in `PythonPerfect.py` add imports as required.

#### First start up flask shell

```shell
$ flask shell
```

#### To create new user instance and add it to the database

	>>> u = User(username='testName', email='testEmail@example.com')
	>>> u.set_password('testPassword')
	>>> db.session.add(u)
	>>> db.session.commit()

**IMPORTANT: remember to commit to session, otherwise changes will not be added to the database**

#### To remove test users from database

There are several ways to delete test users from database.

##### By filtering with know infomation, e.g. username

	>>> db.session.delete(User.query.filter_by(username='testName').first())
	>>> db.session.commit()

##### If only test users exist, run loop to delete all

```shell
>>> users = User.query.all()
>>> for u in users:
. . .   db.session.delete(u)
. . .
>>> db.session.commit()
```




