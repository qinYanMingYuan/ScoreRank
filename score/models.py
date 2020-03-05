from django.contrib import auth
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.core.exceptions import PermissionDenied
from django.db import models

# Create your models here.


def _user_get_all_permissions(user, obj):
    permissions = set()
    for backend in auth.get_backends():
        if hasattr(backend, "get_all_permissions"):
            permissions.update(backend.get_all_permissions(user, obj))
    return permissions


def _user_has_perm(user, perm, obj):
    """
    A backend can raise `PermissionDenied` to short-circuit permission checking.
    """
    for backend in auth.get_backends():
        if not hasattr(backend, 'has_perm'):
            continue
        try:
            if backend.has_perm(user, perm, obj):
                return True
        except:
            return False
    return False


def _user_has_module_perms(user, app_label):
    """
    A backend can raise `PermissionDenied` to short-circuit permission checking.
    """
    for backend in auth.get_backends():
        if not hasattr(backend, 'has_module_perms'):
            continue
        try:
            if backend.has_module_perms(user, app_label):
                return True
        except PermissionDenied:
            return False
    return False


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """客户表"""
    username = models.EmailField(
        max_length=255,
        unique=True,
    )
    name = models.CharField(verbose_name='昵称', max_length=32)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = '账户信息'
        verbose_name_plural = "账户信息"

    def get_full_name(self):
        # The user is identified by their email address
        return self.name

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def __str__(self):  # __unicode__ on Python 2
        return self.username

    def has_perm(self, perm, obj=None):
        #     "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always

        if self.is_active and self.is_superuser:
            return True
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        #     "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    def has_module_perms(self, app_label):
        #     "Does the user have permissions to view the app `app_label`?"
        #     Simplest possible answer: Yes, always
        if self.is_active and self.is_superuser:
            return True
        return _user_has_module_perms(self, app_label)
    objects = UserManager()


class ScoreRank(models.Model):
    """客户分数表"""
    score = models.IntegerField(verbose_name='分数')
    customer = models.ForeignKey(to='UserProfile', verbose_name='客户', unique=True)






