from django.db import models

class TasksPermissionModel(models.Model):

    class Meta:

        managed = False 

        permissions = ( 
            ('view_tasks', 'Can view tasks'), 
            ('run_tasks', 'Can run tasks'), 
            ('run_subscription_task', 'Can run subscription task'),
            ('run_closure_task', 'Can run closure task')
        )