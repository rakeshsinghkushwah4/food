from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from accounts.models import Product,Customer,Order
from accounts.models import Ajax
from accounts.account_validation import validator
from django.core import validators

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        exclude = ['slug','customer']

class orderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']

class  UserForm(forms.ModelForm):
    type = (('customer','customer'),('seller','seller'))
    username = forms.CharField(max_length=100,validators=[validator.username],widget=forms.TextInput(attrs={'class':'input-text','placeholder': 'Enter Email'}))
    password = forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={'class':'input-text','placeholder':'password'}))
    confirm_password = forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={'class':'input-text','placeholder':'Confirm_password'}))
    register_type = forms.ChoiceField(choices=type)
    class Meta:
        model = Customer
        fields = ['name','username','password','confirm_password','register_type','phone','profile_pic']

        widgets = {
            'name' : forms.TextInput(attrs={'placeholder':'Enter name'}),
            'phone' : forms.TextInput(attrs={'type':'number','maxlength':'10','placeholder':'Enter Mobile number'}),
        }

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            if not len(password) >= 6:
                raise validators.ValidationError('Password length is less then 6')
            return self.cleaned_data
        else:

            raise validators.ValidationError('Password and confirm_password does not match')

class customerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        exclude = ['user']

class searchForm(forms.Form):
    Status = (('Status','Status'),('Panding','Panding'),('Out of delivary','Out of delivary'),('Delivered','Delivered'))
    # product = Product.objects.all()
    # pro = (('Product','Prodcut'),)
    # for p in product:
    #     pro= pro+((str(p),str(p)),)
    # status = forms.ChoiceField(choices=Status,required=False,initial='None')
    # products = forms.ChoiceField(choices = pro,required=False,initial='None')

class ajaxForm(forms.ModelForm):
    class Meta:
        model = Ajax
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'id': 'i1','placeholder': 'Say something...'}),
            'text': forms.Textarea(attrs={'id':'i2','placeholder': 'Say something...'}),}
    
    
