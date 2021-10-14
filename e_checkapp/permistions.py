from django.db import models
from rest_framework import permissions
from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User


class AccessPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.type == 'Accountant':
            if request.user.is_views==True:
                return True
            else:
                return False
        elif request.user.type =='CA':
            if request.user.is_views==True:
                return True
            else:
                return False
        else:
            return False


class DeletePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.type == 'Accountant':
            if request.user.is_delete == True:
                return True
            else:
                return False


