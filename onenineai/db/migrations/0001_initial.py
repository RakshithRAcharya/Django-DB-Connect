# Generated by Django 3.2.3 on 2021-05-31 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('db_server', models.CharField(blank=True, max_length=100)),
                ('db_host', models.CharField(max_length=100)),
                ('db_name', models.CharField(max_length=100)),
                ('db_port', models.IntegerField()),
                ('db_login_username', models.CharField(max_length=255)),
                ('db_login_password', models.CharField(blank=True, max_length=100)),
            ],
        ),
    ]
