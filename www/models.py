from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class Teacher(AbstractUser):
    phone_number = PhoneNumberField(unique=True, blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Student(models.Model):
    SEX_CHOICES = (
        ('male', 'Мужчина'),
        ('female', 'Женщина'),
    )

    fio = models.CharField(max_length=255)
    email = models.EmailField()
    birth_date = models.DateField()
    klass = models.ForeignKey('Klass', on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    sex = models.CharField(max_length=255, choices=SEX_CHOICES)
    photo = models.ImageField(upload_to='upload/', blank=True)

    def __str__(self):
        return self.fio


class Klass(models.Model):
    name = models.CharField(max_length=255)
    school = models.ForeignKey('School', on_delete=models.CASCADE)
    teacher = models.OneToOneField('Teacher', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class School(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
