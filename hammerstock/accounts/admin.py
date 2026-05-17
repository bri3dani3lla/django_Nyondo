from django.contrib import admin 
from django.contrib.auth.models import User 
from .models import Profile 

# Register your models here.
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class UserAdmin(admin.ModelAdmin):
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile)
 
# store_manager - manager1234
# sales_attendant - attendant1234
# accounts_admin - accounts1234
