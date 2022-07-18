from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.



class MyUserManager(BaseUserManager):
    def create_user(self, email, firstname,lastname, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email)

        )
        user.firstname = firstname   
        user.lastname = lastname 
        user.set_password(password)  # change password to hash
        user.is_admin = False
        user.is_staff = False
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email)

        )
        user.username = username
        user.set_password(password)  # change password to hash
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


USER_ROLE = (
        ('MEMBER', 'MEMBER'),
        ('LIBRARIAN', 'LIBRARIAN'),
    )

    
class User(AbstractBaseUser):
    email = models.EmailField(max_length=500, verbose_name='Email Address', null=True, blank=True)
    password = models.CharField(max_length=500, verbose_name='Password', null=True, blank=True)
    firstname = models.CharField(max_length=200, verbose_name='First name', null=True, blank=True)
    lastname = models.CharField(max_length=200, verbose_name='Last name', null=True, blank=True)
    username = models.CharField(max_length=200, verbose_name='Username', unique=True, null=True, blank=True)
    user_role = models.CharField(max_length=100, verbose_name='User Role', choices=USER_ROLE)
    date_joined = models.DateTimeField(verbose_name="date joined",  auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    

    USERNAME_FIELD="username"

    REQUIRED_FIELDS=['email']

    objects=MyUserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):

        return True



BOOK_STATUS = (
        ('BORROWED', 'BORROWED'),
        ('AVAILABLE','AVAILABLE')
    )

class Book(models.Model):
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=200, default="AVAILABLE", choices=BOOK_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

USER_BOOK_STATUS = (
        ('BORROWED', 'BORROWED'),
        ('RETURNED','RETURNED')
    )
 
class Borrowbook(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=200, default="BORROWED", choices=USER_BOOK_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)