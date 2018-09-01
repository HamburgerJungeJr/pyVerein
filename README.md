![alt=logo](https://github.com/HamburgerJungeJr/pyVerein/raw/master/pyVerein/app/static/app/images/logo.png)

[![Build Status](https://travis-ci.org/HamburgerJungeJr/pyVerein.svg?branch=master)](https://travis-ci.org/HamburgerJungeJr/pyVerein)

## What is pyVerein
PyVerein is a software to manage your club. It features the possibility to create and list the members as well as managing the finances of your club. Therefore a doubled accounting like required by the HGB is implemented.

## Features
pyVerein contain various features:
* General:
  * Fully featured permission system. For each function of the app you can set wheter the user can view, add or edit an entry. 
* Members:
  * Manage your members with all their personal attributes like 
    * name
    * address
    * birthday
    * join andd termination date
  * Manage how your member pay their fees
    * Cash
    * Remmitance
    * Direct debit
  * five more additional textfields, customizable for all your other needs.
* Finance:
  * pyVerein contains a doubled accounting finance system like required by the HGB
  * Debitors, creditors and impersonal accounts
  * Costaccounting with costcenters and costobjects
  * Automatic function to reset a transaction or to reset and create a new transaction with the same values
  * Stepped transaction input: you cannot save a transaction until debit and credit values are balanced. 

## How to install
### Step 0: Virtualenv (optional, but recommended)
Set up virtualenv / virtualenvwrapper. Refer to the official [virtualenv](https://virtualenv.pypa.io/en/stable/) / [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) documentation for instructions.

### Step 1: Preconditions
Setup your Environment with the following variables:
* `DJANGO_SETTINGS_MODULE`: Sets the settings module. 
  * `pyVerein.settings.development`: For development environment
  * `pyVerein.settings.production`: For production environment
  * `pyVerein.setting.travis`: For Travis-CI environment
* `SECRET_KEY`: Sets the Django secret key. You can generate one with the command 
```
python -c 'from django.core.management import utils; print(utils.get_random_secret_key())'
```
* `DATABASE_URL`: For production only: Sets the database connection string. It utilizes the dj-database-url package. Please refer to the official [documentation](https://github.com/kennethreitz/dj-database-url) for further instructions. In development environments a SQLite database is used by default.
* `DJANGO_PROD_HOST`: For production only: Sets the allowed hosts for Django. Please refer to the official [documentation](https://docs.djangoproject.com/en/2.1/ref/settings/#allowed-hosts) for further instructions.

### Step 2: Install packages
Install the required packages by running the following command in the project root:
* For development environment
```
pip install -r ./requirements_development.txt
```
* For production environment
```
pip install -r ./requirements_production.txt
```

### Step 3: Generate Database
Change into the `pyVerein` directory and run the following command to migrate the database models:
```
python manage.py migrate
```

### Step 4: Compile translation
Currently there is only a german translation
Stay in the `pyVerein` directory and run the command:
```
python manage.py compilemessages
```

### Step 5: Run server
Stay in the `pyVerein` directory and run the command:
```
python manage.py runserver
```

For further information on how to deploy a Django-application please refer to the [official Django documentation](https://docs.djangoproject.com/en/2.1/).