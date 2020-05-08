from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import Customer

def customer_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='CUSTOMER')
        instance.groups.add(group)
        Customer.objects.create(user=instance,  email=instance.email)
        print('Profile created')

post_save.connect(receiver=customer_profile, sender=User)