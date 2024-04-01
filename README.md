# FITS (personal FInancial Tracking Software)

FITS is a simple python-based application that allows users to track their finances. You can use it to track your incomes/expenses (recurring and non-recurring) and generate a report on a monthly basis. 

## Frameworks

- django 

## Useful commands

### 1. django

- Create a new project

```
python3 -m django startproject <projectname>
```

- Create a new app 

```
cd <projectname>
python3 manage.py startapp <appname>
```

- Run the webserver

```
python3 manage.py runserver
```

- Run migration after database changes

```
python3 manage.py makemigrations
python3 manage.py migrate
```

- Create users

```
python3 manage.py createsuperuser
```
With this, the super user can login to the admin view ({ip}/admin) and update the database. 