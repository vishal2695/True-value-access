# Generated by Django 4.0.6 on 2022-07-18 06:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('librarian', '0002_book_return_avail_status_alter_book_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='return_avail_status',
        ),
    ]