# Technical

The project is based on Django. 

# Setup

> pip install -r requirements

> python manage.py makemigrations

> python manage.py migrate

> python manage.py runserver

# Django

- webapp: base project which includes main settings 
- main: is the main app of the project, includes the basic structure for evnets
- kitchenrun: includes the kitchenrun logics and models 

Further event types should be developed as app which uses a similar structure to kitchenrun to ensure configurability and extandability.
