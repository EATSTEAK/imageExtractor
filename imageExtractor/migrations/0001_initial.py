# Generated by Django 3.1.3 on 2020-11-10 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('req_id', models.UUIDField()),
                ('url', models.TextField()),
                ('status', models.IntegerField()),
                ('created', models.DateTimeField()),
            ],
        ),
    ]
