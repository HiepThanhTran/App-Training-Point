# from django.contrib import admin

from tpm.admin import my_admin_site
from users.models import Account, Officer, Student

my_admin_site.register(Account)
my_admin_site.register(Officer)
my_admin_site.register(Student)
