# Scraping Estimation Tool
> A tool to estimate the website and scraping parameters of a domain/ website.

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Instructions of Use](#instructions)
* [Status](#status)
* [Contact](#contact)

## General info
The purpose of this project is to estimate a few website parameters to understand the complexity and feasibility of scraping a website. Thsi helps the development team to analyse the scraping feasibility.


## Technologies
* Django
* Scrapy
* Scrapyd
* Python
* SQL

## Setup

* Create a new folder
* Clone to the project

`git clone https://gitlab.com/sdt-bizdev/scraping-estimation-tool.git`

* Create a virtual Environment

(Make sure you have python3, pip, and venv)

```
$ sudo apt-get install python3
$ sudo apt-get install python3-pip
$ sudo apt-get install python3-venv
$ python3 -m venv env
$ source env/bin/activate
```

* Install requirements ( check version of pip before that)

If pip version is installed with respect to python3, proceed.

`pip3 install -r requirements.txt`

* Changes to be made :

Go to settings file and change the DATABASES setting according to your local settings.

``` 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'set_database',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'Sandy@123',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

Change the USER , PASSWORD etc.

Go to the views and change the db settings according to your local settings where ever its necessary.

```
db = mysql.connector.connect(
			host="localhost",
			user="root",
			passwd="Sandy@123",
			database="set_database",
			use_unicode=True, 
			charset="utf8"
		)
```

Change user, passwd etc.

Go to the pipelines in tool folder and then change the db settings according to your local settings where ever necessary.

```
self.db = mysql.connector.connect(
			host="localhost",
			user="root",
			passwd="Sandy@123",
			database="set_database",
			use_unicode=True, 
			charset="utf8"
		)
```

Change the user, passwd etc.





* Running the Project
Activate Virtual Environment
`source env/bin/activate`
Go to the project directory and locate to manage.py 


Run the Code
```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```

## Instructions of Use

Go to tool and locate to scrapy.cfg file
Start scrapyd as a service in that location
`scrapyd`
The service should be running continuously.

Now open a new terminal and activate the environment and reach the same location as above and deploy scraping project.

`scrapyd-deploy local_set`

'local_set' is a random name, you can name it as per your convenience in scrapy.cfg file.

Go to the website and make a website entry and then xpath entry and see if eveything works fine.

## Status
Project is:  _finished_

Next version will be accommodating new features.



## Contact
Created by [@Sandeep Singamsetty](https://gitlab.com/sandeep.si) - feel free to contact me!