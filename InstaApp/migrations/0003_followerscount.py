# Generated by Django 4.1 on 2022-10-10 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InstaApp', '0002_likepost'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowersCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.CharField(max_length=100)),
                ('user', models.CharField(max_length=100)),
            ],
        ),
    ]
