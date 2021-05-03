#Python Perfect

##Features
...
## App Launching
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

#### Configuring flask

##### On windows

```shell
$ set FLASK_APP=PythonPerfect.py
```


##### On mac/linux
```shell
$ export FLASK_APP=PythonPerfect.py
```
####Run Flask app
```shell
$ flask run
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

##Testing Users database
Flask shell context set in `PythonPerfect.py` add imports as required.

#### First start up flask shell

```shell
$ flask shell
```

#### To create new user instance and add it to the database

	>>> u = User(username='testName', email='testEmail@example.com')
	>>> u.set_password('testPassword')
	>>> db.session.add(u)
	>>> db.session.commit( )

**IMPORTANT: remember to commit to session, otherwise changes will not be added to the database**

#### To remove test users from database

There are several ways to delete test users from database.

##### By filtering with know infomation, e.g. username

	>>> db.session.delete(User.query.filter_by(username='testName').first())
	>>> db.session.commit( )

##### If only test users exist, run loop to delete all

```shell
>>> users = User.query.all( )
>>> for u in users:
. . .   db.session.delete(u)
. . .
>>> db.session.commit( )
```




