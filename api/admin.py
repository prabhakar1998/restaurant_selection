from django.contrib import admin

# Register your models here.
from .models import Employee, Menu, Restaurant, User, Vote

# class UserAdmin(admin.ModelAdmin):
#     fields = __all__

admin.site.register(User)
admin.site.register(Employee)
admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(Vote)
