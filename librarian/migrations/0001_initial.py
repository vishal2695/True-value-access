# Generated by Django 4.0.6 on 2022-07-17 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=500, null=True, verbose_name='Email Address')),
                ('password', models.CharField(blank=True, max_length=500, null=True, verbose_name='Password')),
                ('firstname', models.CharField(blank=True, max_length=200, null=True, verbose_name='First name')),
                ('lastname', models.CharField(blank=True, max_length=200, null=True, verbose_name='Last name')),
                ('username', models.CharField(blank=True, max_length=200, null=True, unique=True, verbose_name='Username')),
                ('user_role', models.CharField(choices=[('MEMBER', 'MEMBER'), ('LIBRARIAN', 'LIBRARIAN')], max_length=100, verbose_name='User Role')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('status', models.CharField(choices=[('BORROWED', 'BORROWED'), ('AVAILABLE', 'AVAILABLE')], max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]