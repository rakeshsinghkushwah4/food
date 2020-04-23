from django.contrib import admin
from accounts.models import Customer, Tag, Product, Order,add_card

# Register your models here.
admin.site.register(Customer)
admin.site.register(Tag)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(add_card)
