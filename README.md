# Social Network
 Publication of paintings

 ## Current features

* Using the Django authentication system
* Creating user registration handlers
* Extending the model to users 
* Adding authorization through other social networks
* Creating many-to-many relationships 
* Redefining the behavior of forms
* jQuery bookmarklet implementation
* Creating preview images using sorl-thumbnail
* Implementing handlers for Fetch requests
* implementation of a many-to-many relationship with an intermediate model
* Creation of a subscription system 
* Adding a news feed application
* Optimization of queries for related objects
* Using Django signals
* Storing data in Redis

    

## Snaps of project
Login:
![][login]

Home:
![][home]

Images:
![][Images]

Image:
![][image]

People:
![][people]


User:
![][user]

[login]: ./scrin/login.png
[home]:./scrin/home.png 
[images]: ./scrin/images.png
[image]: ./scrin/image.png
[people]: ./scrin/people.png
[user]: ./scrin/user.png

# Instructions

1. ## Installations

Make sure to have python version 3 install on you pc or laptop.
<br>
**Clone repository**
<br>
`https://github.com/OleksiiMartseniuk/Blog.git`

2. ## Installing dependencies

It will install all required dependies in the project.
<br>
`pip install -r requirements.txt`
<br>
Change your values
```python
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
```

2. ## Migrations

Create postgresql database
<br>
To run migrations.
<br>
`python manage.py migrate`

3. ## Create superuser
   
To create super user run.
<br>
`python manage.py createsuperuser`
<br>
After running this command it will ask for username, password. You can access admin panel from
<br>
`localhost:8000/admin/`

4. ## Running locally

To run at localhost. It will run on port 8000 by default.
<br>
`python manage.py runserver`