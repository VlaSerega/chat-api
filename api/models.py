from django.db import models
from django.contrib.auth.models import PermissionsMixin, UserManager
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

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Contacts(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_contacts')
    contact_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='in_contacts')

    class Meta:
        unique_together = (('user_id', 'contact_id'),)


class Conversation(models.Model):
    title = models.CharField(verbose_name='Название', max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_groups')

    class Type(models.IntegerChoices):
        ONE_TO_ONE = 0, 'Личные сообщения'
        GROUP = 1, 'Групповой чат'


class ConversationParticipants(models.Model):
    conversation_id = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participants')
