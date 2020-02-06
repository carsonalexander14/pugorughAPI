from django.test import TestCase
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import (
    APIRequestFactory, force_authenticate, APIClient)

from . import models
from . import serializers


class ModelsTests(TestCase):
    def setUp(self):
        form = UserCreationForm(data={
            'id': 1,
            'username': 'carson',
            'password1': 'carson1',
            'password2': 'carson1'
        })
        form.save()
        self.user = User.objects.get(id=1)

    def test_UserPref(self):
        models.UserPref.objects.get(user=self.user)

    def test_DogModel(self):
        data = {
            'name': 'goodboy',
            'image_filename': '1.jpg',
            'age': 1,
            'breed': 'Boxer',
            'gender': 'm',
            'size': 'm',

        }
        dog = models.Dog.objects.create(**data)
        dog.full_clean()
        self.assertEqual(dog.name, data['name'])



class DogSerializerTests(TestCase):
    def setUp(self):
        self.dog_data = {
            'name': 'goodboy',
            'image_filename': '1.jpg',
            'age': 1,
            'breed': 'Boxer',
            'gender': 'm',
            'size': 'm',
        }
        self.serializer_data = {
            'name': 'goodboy',
            'image_filename': '1.jpg',
            'age': 1,
            'breed': 'Boxer',
            'gender': 'm',
            'size': 'm',
        }
        self.dog = models.Dog.objects.create(**self.dog_data)
        self.serializer = serializers.DogSerializer(instance=self.dog)

    def test_dog_open_fields(self):
        data = self.serializer.data

        self.assertCountEqual(
            data.keys(), ['name', 'image_filename', 'age', 'breed',
                          'gender', 'size', 'id'])
    

class ViewsTests(TestCase):
    def setUp(self):
        form = UserCreationForm(data={
            'id': 1,
            'username': 'carson',
            'password1': 'carson1',
            'password2': 'carson1'
        })
        form.save()
        data = {
            'name': 'goodboy',
            'image_filename': '1.jpg',
            'age': 1,
            'breed': 'Boxer',
            'gender': 'm',
            'size': 'm',

        }
        self.data = models.Dog.objects.create(**data)
        self.user = User.objects.get(id=1)
        token = Token.objects.create(user=self.user).key
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)


    def test_DetailDog_liked(self):
        self.client.put('/api/dog/1/liked/', format='json')
        response = self.client.get(
            '/api/dog/-1/liked/next/', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'goodboy')


    def test_DetailDog_disliked(self):
        self.client.put('/api/dog/1/disliked/', format='json')
        response = self.client.get(
            '/api/dog/-1/disliked/next/', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'goodboy')

