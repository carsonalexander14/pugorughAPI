from django.test import TestCase
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
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
    
    def test_fields(self):
        data = self.serializer.data

        self.assertEqual(data['name'], self.dog_data['name'])
        self.assertEqual(data['image_filename'],
                         self.dog_data['image_filename'])
        self.assertEqual(data['age'], self.dog_data['age'])
        self.assertEqual(data['breed'], self.dog_data['breed'])
        self.assertEqual(data['gender'], self.dog_data['gender'])
        self.assertEqual(data['size'], self.dog_data['size'])

