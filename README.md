#Python Perfect
##Features
...
## App Launching

#### Install Virtual Environment
`$ pip3 install virtualenv`
#### Activate Virtual Enviroment
`$ python3 -m venv env`

`$ source env/bin/activate`


#### Install required python packages


`$ pip3 install -r requirements.txt`

#### Configuring flask

##### On windows

`$ set FLASK_APP=PythonPerfect.py`


##### On mac/linux
`
$ export FLASK_APP=PythonPerfect.py
`
####Run Flask app
`
$ flask run
`
## Setting Flask Environment and Debug/Testing modes
It is highly recommended to avoid setting flask environments by code
i.e. in config.py

Debug mode is by defult enabled when flask environment is set to development
#### Changing Flask Environments:
##### On windows
`$ set FLASK_ENV=<environment>`
##### On mac/linux
`$ export FLASK_ENV=<environment>`   ?! CHECK THIS ON LINUX/MAC SYSTEM

## Initialise SQLite database with flask-migrate
First migration script already added, run
`$ flask db upgrade`
to construct the database on your local device.

#### Modifying databases
`$ flask db migrate`
This will create a new migration script. Running above command will implement it.
!! For large changes, please inspect the script first before upgrading. !!
