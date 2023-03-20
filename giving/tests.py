from django.test import TestCase
import pytest
from django.test import Client
from django.shortcuts import reverse
from giving.models import User, Category, Insitution, Donation


# Create your tests here.
# @pytest.fixture
# def client():
#     return Client()


@pytest.fixture
def user_created_not_logged(client, django_user_model):
    username = "username"
    password = "dupa"
    user = django_user_model.objects.create_user(username=username, password=password)
    return user

@pytest.fixture
def logged_user(client, django_user_model):
    username = "username"
    password = "dupa"
    user = django_user_model.objects.create_user(username=username, password=password)
    client.force_login(user)


# response = clint.post(url, {slownik z danymi przekazanymi w post}

@pytest.mark.django_db
def test_auth_view(client, logged_user):
    url = reverse('donate')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_donate_post_view(client, logged_user):
    url = reverse('donate')
    response = client.post(url, {"dupa": "kupa"})
    print(response)

@pytest.mark.django_db
def test_email(client):
    url = reverse('register')
    response = client.post(url, {"name": "imie",
                                 "surname": "nazwisko",
                                 "email": 'wojtekteam@op.pl',
                                 'password': 123,
                                 'password2': 123})
    assert response.status_code == 302