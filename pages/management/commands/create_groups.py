"""
Create permission groups
Create permissions (read only) to models for a set of groups
"""
import logging

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

GROUPS = ['Sponsor', 'front_desk']
MODELS = ['meeting', 'guest']
# For now only view permission by default for all, others include add, delete, change
SPONSOR_PERMISSIONS = ['view', 'change', 'add']


class Command(BaseCommand):
    help = 'Creates read only default permission groups for users'

    def handle(self, *args, **options):
        new_group, created = Group.objects.get_or_create(name='Sponsor')
        for permission in SPONSOR_PERMISSIONS:
            name = 'Can {} {}'.format(permission, 'meeting')
            print("Creating {}".format(name))

            try:
                model_add_perm = Permission.objects.get(name=name)
            except Permission.DoesNotExist:
                logging.warning(
                    "Permission not found with name '{}'.".format(name))
                continue

            new_group.permissions.add(model_add_perm)

        new_group, created = Group.objects.get_or_create(name='Front Desk')
        name = 'Can {} {}'.format('view', 'guest')
        model_add_perm = Permission.objects.get(name=name)
        new_group.permissions.add(model_add_perm)
        name = 'Can {} {}'.format('change', 'guest')
        model_add_perm = Permission.objects.get(name=name)
        new_group.permissions.add(model_add_perm)
        name = 'Can {} {}'.format('view', 'meeting')
        model_add_perm = Permission.objects.get(name=name)
        new_group.permissions.add(model_add_perm)

        print("Created default group and permissions.")
