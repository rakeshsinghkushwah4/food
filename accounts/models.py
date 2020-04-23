from django.db import models
from django.contrib.auth.models import User
from django.core import validators
from django.template.defaultfilters import slugify

from accounts.account_validation import validator

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(to=User,on_delete=models.CASCADE)
    name = models.CharField(max_length= 100, validators=[validator.name])
    phone = models.CharField(max_length= 10,validators=[validator.phone])
    profile_pic = models.ImageField(upload_to='profile_pic/',default='facebook.jpg',null=True,blank=True)
    cr_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    Category = (('Indoor','Indoor'),('Out Door','Out Door'))
    customer = models.ForeignKey(to=Customer,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.FloatField()
    Category = models.CharField(max_length=100,choices = Category)
    description = models.TextField()
    image = models.ImageField(upload_to='product/')
    cr_date = models.DateTimeField(auto_now_add=True)
    tag = models.ManyToManyField(Tag)
    slug = models.SlugField(null=True,unique=True)

    def __str__(self):
        return self.name

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args,**kwargs)

class Order(models.Model):
    Status = (('Panding','Panding'),('Out of delivary','Out of delivary'),('Delivered','Delivered'))
    customer = models.ForeignKey(to=Customer, on_delete = models.CASCADE)
    product = models.ForeignKey(to= Product, on_delete = models.CASCADE,null=True,)
    status = models.CharField(max_length=100,default='Panding', choices = Status,null=True)
    quntity = models.CharField(max_length=500,default=1)
    cr_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.customer)

class add_card(models.Model):
    product_id = models.CharField(max_length=225,unique=True)
    quntity = models.CharField(max_length=255)


class Ajax(models.Model):
    name= models.CharField(max_length=100)
    text = models.TextField()
    def __str__(self):
        return self.name
