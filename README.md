# Charity project

A project allows to donate all kind of items we don't use at home to charity.
It contains register, login and account recovery feature. After creating account 
and confirm email address user can fill donate form. App validates fields(e.g. 
pickup date can't be from past) and saves donation to database.


## Installation

Install packages from requirements.txt -> pip install -r requirements.txt

Write python manage.py loaddata ./fixtures/db.json in 
terminal to populate database with necessary details(such as Categories or Foundations)