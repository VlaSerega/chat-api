# Generated by Django 4.2.7 on 2023-11-30 14:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_conversation_alter_user_managers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='conversation_type',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Личные сообщения'), (1, 'Групповой чат')], default=0, verbose_name='Тип переписки'),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='contact_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_contacts', to=settings.AUTH_USER_MODEL),
        ),
    ]