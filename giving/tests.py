from django.test import TestCase
import pytest
from django.test import Client
from django.shortcuts import reverse
from giving.models import User, Category, Institution, Donation
from django.contrib.messages import get_messages


@pytest.fixture
def user_created_not_logged(client, django_user_model):
    username = "username"
    password = "password"
    user = django_user_model.objects.create_user(username=username, password=password)
    return user

@pytest.fixture
def logged_user(client, django_user_model):
    username = "username"
    password = "password"
    user = django_user_model.objects.create_user(username=username, password=password)
    client.force_login(user)

@pytest.fixture
def superuser(client, django_user_model):
    username = "username"
    password = "password"
    user = django_user_model.objects.create_user(username=username, password=password, is_superuser=True)
    client.force_login(user)


@pytest.mark.django_db
def test_auth_view(client, logged_user):
    url = reverse('donate')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_donate_post_view(client, user_created_not_logged):
    url = reverse('donate')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_send_message(client):
    url = reverse('message-contact')
    response = client.get(url, {
        "name": "Adam",
        "surname": "Malysz",
        "message": "Test message"
    })
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == "Wiadomość wysłana"
    assert response.status_code == 302


@pytest.mark.django_db
def test_register(client):
    url = reverse('register')
    response = client.post(url, {
        "name": "Adam",
        'surname': "Malysz",
        'email': "adam@malysz.pl",
        'password': "Tojesthaslo!1",
        'password2': 'Tojesthaslo!1'
    })
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == "Sprawdź pocztę"
    assert response.status_code == 302
    response = client.post(url, {
        "name": "Adam",
        'surname': "Malysz",
        'email': "adam@malysz.pl",
        'password': "test",
        'password2': 'test'
    })
    assert response.status_code == 200

@pytest.mark.django_db
def test_login(client, user_created_not_logged):
    url = reverse('login')
    response = client.post(url, {
        "email": "username",
        'password': "password"
            })
    assert response['location'] == reverse('main')
    assert response.status_code == 302


@pytest.mark.django_db
def test_logout(client, logged_user):
    url = reverse('donate')
    response = client.get(url)
    assert response.status_code == 200
    url = reverse('logout')
    response = client.get(url)
    assert response['location'] == reverse('main')
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_donation(client, logged_user):
    url = reverse('donate')
    response = client.get(url)
    assert response.status_code == 200
    assert Donation.objects.count() == 0
    response = client.post(url, {
        "categories": ['test', 'meble'],
        "bags": 55,
        "organization": "organizacja testowa",
        "address": "ulica",
        "city": "miasto",
        "postcode": '80-123',
        'phone': 45789132,
        'data': '2023-05-05',
        'time': '15:33',
        'more_info': 'nie'
    })
    assert response['location'] == reverse('donate')
    assert Donation.objects.count() == 0
    cat = Category.objects.create(name="test")
    int_ = Institution.objects.create(name='test', description='test', type=1)
    int_.categories.add(cat)
    response = client.post(url, {
        "categories": ['test', 'meble'],
        "bags": 55,
        "organization": "test",
        "address": "ulica",
        "city": "miasto",
        "postcode": '80-123',
        'phone': 45789132,
        'data': '2023-05-05',
        'time': '15:33',
        'more_info': 'tak'
    })
    assert Donation.objects.count() == 1



