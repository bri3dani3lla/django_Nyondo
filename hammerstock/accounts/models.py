from django.db import models
from django.contrib.auth.models import User 


# We extend Django's built-in User model using a Profile
# Django already gives us username, password, email
# We just add the role on top of that

# Create your models here.
class Profile(models.Model):

    ROLE_CHOICES = [
        ('manager',   'Store Manager'),
        ('attendant', 'Sales Attendant'),
        ('accounts',  'Accounts / Admin'), 
    ]

# OneToOneField means one user has exactly one profile
# if the user is deleted, their profile is deleted too (CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}" 