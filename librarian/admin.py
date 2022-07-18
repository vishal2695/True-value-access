from django.contrib import admin
from .models import User, Book, Borrowbook
# Register your models here.


@admin.register(User)
class Useradmin(admin.ModelAdmin):
    list_display = ['id','email', 'user_role']



@admin.register(Book)
class Useradmin(admin.ModelAdmin):
    list_display = ['id','name']


@admin.register(Borrowbook)
class Useradmin(admin.ModelAdmin):
    list_display = ['id','user_id','book_id']



