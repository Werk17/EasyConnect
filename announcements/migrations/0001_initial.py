# Generated by Django 3.1.13 on 2021-12-05 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('display', models.BooleanField(default=False)),
                ('level', models.CharField(choices=[('warning', 'Warning'), ('error', 'Error'), ('success', 'Success'), ('info', 'Info')], default='info', max_length=7)),
            ],
        ),
    ]