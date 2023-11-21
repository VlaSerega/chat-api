from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(verbose_name='Имя', max_length=60, null=False)
    last_name = models.CharField(verbose_name='Фамилия', max_length=60, null=False)

    email = models.EmailField('Email', unique=True, null=False)
    date_joined = models.DateTimeField('Дата регистрации', auto_now_add=True, null=False)
    is_active = models.BooleanField('Пользователь активирован', default=True, null=False)
    is_staff = models.BooleanField('is_staff', default=False, null=False)
    is_superuser = models.BooleanField('Суперпользователь', default=False, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
