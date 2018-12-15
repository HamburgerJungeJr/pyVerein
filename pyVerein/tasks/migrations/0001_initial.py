# Generated by Django 2.1.1 on 2018-12-14 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TasksPermissionModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('run_tasks', 'Can run tasks'), ('run_subscription_task', 'Can run subscription task'), ('run_closure_task', 'Can run closure task')),
                'managed': False,
            },
        ),
    ]