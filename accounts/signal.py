from django.db.models.signals import post_save
from django.contrib.auth.models import User
from accounts.models import Customer
from django.contrib.auth.models import Group

def customer_profile(sender,instance,created, **kwargs):
    print(' I am in side of signal ')
    if created:
        # group = Group.objects.get(name="customer")
        # instance.groups.add(group)
        Customer.objects.create(user=instance)
        print('profile created')
post_save.connect(customer_profile,sender=User)