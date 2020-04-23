from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from accounts.models import Customer, Product, Order,Ajax
from accounts.form import AddProductForm, UserForm, customerForm, orderForm,searchForm,ajaxForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login as authenticated, logout as deauthenticated
from django.contrib.auth.decorators import login_required
from accounts.decorator import unauthanticated_user,allowed_user,admin_only
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.core import serializers
import json
from django.core.serializers.json import DjangoJSONEncoder
from accounts.models import add_card

# from myproject.settings import EMAIL_HOST_USER
# from django.core.mail import send_mail

# Create your views here.
@unauthanticated_user
def register(req):
    if req.method=='POST':
        form = UserForm(req.POST,req.FILES)
        if form.is_valid():
            user = User.objects.create_user(username=req.POST['username'],password=req.POST['password'])
            print(req.POST['name'])
            customer = Customer.objects.get(user=user)
            customer.name = req.POST['name']
            customer.phone = req.POST['phone']
            customer.profile_pic = req.FILES.get('profile_pic')
            group = Group.objects.get(name=req.POST['register_type'])
            user.groups.add(group)
            customer.save()
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = UserForm()
    context = {'form':form}
    return render(req,'accounts/register.html',context)

@unauthanticated_user
def login(req):
    if req.method=="POST":
        username = req.POST.get('username')
        password = req.POST.get('password')
        user = authenticate(req,username=username,password=password)
        if user is not None:
            authenticated(req,user)
            return redirect('home')
        else:
            messages.info(req,'Username or Password is incorrect ')
            return redirect('login')
    return render(req,'accounts/login.html')

@login_required(login_url='login')
def logout(req):
    deauthenticated(req)
    return redirect('login')

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin','seller'])
@admin_only(url='user_page')
def home(req):
    # ########################################################################
    # we should want that order which seller logged in 
    orders_display = Order.objects.filter(product__customer=req.user.customer)[:5]
    orders = Order.objects.filter(product__customer = req.user.customer)
    # customer = Customer.objects.all()
    # Here we get all customer which is order product in set because we get only one time name of customer
    customer_set = set()
    for i in orders:
        customer_set.add(i.customer)
    #########################################################################################################
    total_customers = len(customer_set)
    total_order  = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Panding').count()
    print('Cheaking the group s',req.user.groups.filter(name ='admin'))
    context = {'order':orders,'order_display':orders_display,'customer':customer_set,'delivered':delivered,'totalorder':total_order,'pending':pending}
    return render(req,'accounts/dashboard.html',context)

@login_required(login_url='login')
@allowed_user(['seller'])
def product(req):
    product = Product.objects.filter(customer = req.user.customer)
    context = {'product':product}
    return render(req,'accounts/product.html',context)

@login_required(login_url='login')
def productDetail(req,slug):
    product = Product.objects.get(slug=slug)
    return render(req,'accounts/product_detail.html',{'product':product,'slug':slug})

@login_required(login_url='login')
@allowed_user(['seller'])
def productEdit(req,slug):
    edit = 'edit'
    product = Product.objects.get(slug= slug)
    form = AddProductForm(instance=product)
    if req.method=="POST":
        form = AddProductForm(req.POST,instance=product)
        if form.is_valid():
            form.save()
            return redirect('product')
    context={'form':form,"edit":edit,'id':slug}
    return render (req,'accounts/add_product.html',context)

@login_required(login_url='login')
@allowed_user(['seller'])
def customer(req,pk):
    search_form = searchForm()
    customer = Customer.objects.get(id=pk)
    # Thus order is show which current seller is logged in or seller add the product
    order = customer.order_set.filter(product__customer = req.user.customer)
    print('order',order)
    total_order = order.count()
    print(req.method)
    context = {'customer':customer,'search_form':search_form,'order':order,'total_order':total_order}
    return render(req,'accounts/customer.html',context)

@login_required(login_url='login')
def createOrder(req,pk):
    # here extra is tall how many form you get 5 or 10 or so many
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('product','status'),extra=5 )
    customer = Customer.objects.get(id=pk)
    # form = orderForm(initial = {"customer":customer})
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    if req.method=="POST":
        # form = orderForm(req.POST)
        formset = OrderFormSet(req.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
        else:
            pass
            # print('form',form)
    return render(req,'accounts/order_form.html',{'form':formset})

@login_required(login_url='login')
@allowed_user(['seller'])
def updateOrder(req,pk):    
    order = Order.objects.get(pk=pk)
    print(order)
    form = orderForm(instance=order)
    print('form',form)
    if req.method=="POST":
        form = orderForm(req.POST, instance=order)
        if form.is_valid():    
            form.save()
            return redirect('/')
    context = {'form':form,'order':order}
    return render(req,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_user(['customer'])
def deleteOrder(req,pk):    
    order = Order.objects.get(pk=pk)    
    if req.method=="POST":
        order.delete()
        return redirect('user_page')
    context = {'item':order}
    return render(req,'accounts/delete.html',context)

@login_required(login_url='login')
@allowed_user(['seller'])
def addProduct(req):
    form = AddProductForm()
     # here extra is tall how many form you get 5 or 10 or so many
    # form = orderForm(initial = {"customer":customer})
    # formset = AddProductForm(queryset=Order.objects.none()
    if req.method=="POST":
        # form = orderForm(req.POST)
        form = AddProductForm(req.POST,req.FILES)
        if form.is_valid():
            # Here we are not saving this form but form is take all field 
            pro = form.save(commit=False)
            pro.customer = req.user.customer
            pro.save()    
            return redirect('/')
        else:
            print(form.errors)
            # print('form',form)
    context = {'form':form}
    return render(req,'accounts/add_product.html',context)

@login_required(login_url='login')
def search(req,pk):
    order1 = None
    customer = Customer.objects.get(id=pk)
    order = customer.order_set.filter(product__customer = req.user.customer)
    if req.method=='POST' and req.is_ajax():
        form = searchForm(req.POST)
        if form.is_valid():
            # If form is valid then form.cleaned_data is work in the form condition
            status = form.cleaned_data['status']
            product = form.cleaned_data['products'] 
            if status or product:
                if status !='Status' and product !='Product':
                    order1 = order.filter(Q(status__icontains=status)&
                                 Q(product__name__icontains=product)).values('id','product__name','product__Category','cr_date','status')
                    print(type(order1))
                elif status == "Status" and product == "Product":
                    order1 = order.all().values('id','product__name','product__Category','cr_date','status')
                else:
                    order1 = order.filter(Q(status__icontains=status) |
                                          Q(product__name__icontains=product)).values('id','product__name','product__Category','cr_date','status')
                # values is always return queryValues not a query datatype
                # But when we are not apply value in the query the it return query datatype
                # in query datatype we use following serializer use

                #serdata = serializers.serialize("json", order1)

                #But datatype is queryValue then we use below serializer
                serdata = json.dumps(list(order1),cls=DjangoJSONEncoder)
                print(serdata)
                print(type(serdata))
                return JsonResponse(serdata,safe=False)
    context = {'order1':order1,'customer':customer}
    return render(req,'accounts/customer.html',context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def user(req):
    orders = req.user.customer.order_set.all()
    p_order = orders.filter(status='Panding')
    d_order = orders.filter(status='Delivered')
    total_order  = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Panding').count()
    context = {'order':p_order,'d_order':d_order,'delivered':delivered,'totalorder':total_order,'pending':pending}
    print(context)
    return render(req,'accounts/user.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def accountsSettings(req):
    user = req.user.customer 
    print('user',user)
    form  = customerForm(instance=user)
    if req.method=='POST':
        form = customerForm(req.POST,req.FILES,instance=user)
        if form.is_valid:
            print('form is valid')
            form.save()
    context={'form':form}
    return render(req,'accounts/accounts_settings.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def Productshow(req):
    orders = Product.objects.all()
    count = add_card.objects.all().count()
    print('Product',orders)
    context = {'order':orders ,'count':count}
    return render(req,'accounts/order_product.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def Cancel_order(req,id):
    product = Product.objects.get(id=id)
    product.image.delete()
    product.delete()
        
    return redirect('product')

@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def order_customer(req,slug,quntity):
    product = Product.objects.get(slug=slug)
    customer = req.user.customer
    print(customer)
    order = Order.objects.create(customer = customer,
    product= product,quntity=quntity)
    return redirect('product_show')

def ajax_test(req):
    form = ajaxForm()
    ajax_data = Ajax.objects.all()
    if req.method=='POST' and req.is_ajax:
        form = ajaxForm(req.POST)
        if form.is_valid:

            if(form.save()):
                serdata = serializers.serialize("json", ajax_data)                
                return JsonResponse(serdata,safe=False)
            else:
                return HttpResponse('fail')
        else:
            return HttpResponse('fail')
    context = {'form':form,'ajax_data':ajax_data}
    return render(req,'accounts/ajax_test.html',context)

# /////////////////////////////////////////////// Add Cart //////////////////////////////////////////////////////////#
@login_required(login_url='login')
@allowed_user(['customer'])
def add_to_card(req):
    id = int(req.GET['product_id'])
    quntity = int(req.GET['quntity'])

    try:
        print('rakesh')
        product_quntity = add_card.objects.create(product_id = id,quntity= quntity)
        count = add_card.objects.all().count()
        print(count)
        print(product_quntity)
        return JsonResponse({'count':count}, safe=False)
    # print(card)
    # if session does not have any key then it create empty create card and store dictionary in set_default() method
    # r=req.session.setdefault('cart',{})[str(id)] =product_document
    # r[str(id)] =product_document
    # print(r)
    # req.session.set_default('cart', {})[str(id)] = product_document
    # req.session.set_default('cart',)
    except:
        return JsonResponse({'count': count}, safe=False)

    return HttpResponse('<h2>Please Add Some Thing in card 2</h2>')


@login_required(login_url='login')
@allowed_user(['customer'])
def access_card(req):
    item = add_card.objects.all()
    if len(item)==0:
        return HttpResponse('<h2>Please Add Some Thing in card </h2>')
    dic = {}
    total = 0
    print('item',len(item))
    for i in item:
        print(i)
        print('id',i.product_id)
        product = Product.objects.get(id=i.product_id)
        dic[product] =i
        total = total+(product.price*int(i.quntity))
    print(dic)
    if req.method=="POST":
        if req.user.is_authenticated:
            for i in item:
                product = Product.objects.get(id=i.product_id)
                customer = req.user.customer
                order = Order.objects.create(customer = customer,product=product,quntity=i.quntity )
                order.save()
                add = add_card.objects.get(id=i.id)
                add.delete()
            return redirect('/accounts/product_show/')
        else:
            return redirect('login')
    #    order = Order.objects.filter(id=int(id)).values('id','product__name','product__Category','cr_date','status','quntity')
    #    orders.append(order)
    # serdata = json.dumps(list(order),cls=DjangoJSONEncoder)
    # print(serdata)
    # print(type(serdata))
    # return JsonResponse(serdata,safe=False)
    # serdata = serializers.serialize("json", orders)
    # print(serdata)
    # print(type(serdata))
    # return JsonResponse(serdata,safe=False)
    return render(req,'accounts/add_card.html',{'product':dic,'total':total})

@allowed_user(['customer'])
def cancel_add_card(req,id):
    cancel_product = add_card.objects.get(id=id)
    cancel_product.delete()
    return redirect('access_card')

# def delete_card(req):
#     try:
#         del req.session['card']
#     except KeyError:
#         return HttpResponse('Please create card')
#     return render(req,'accounts/order_product.html')


# Test cookie accept or not brawoser
# def cookie_session(request):
#     request.session.set_test_cookie()
#     return HttpResponse("<h1>dataflair</h1>")
    
# def cookie_delete(request):
#     if request.session.test_cookie_worked():
#         request.session.delete_test_cookie()
#         response = HttpResponse("dataflair<br> cookie createed")
#     else:
#         response = HttpResponse("Dataflair <br> Your browser doesnot accept cookies")
#     return response

# This is a Session created

# def create_session(request):
#     request.session['name'] = 'username'
#     request.session['password'] = 'password123'
#     return HttpResponse("<h1>dataflair<br> the session is set</h1>")

# def access_session(request):
#     response = "<h1>Welcome to Sessions of dataflair</h1><br>"
#     if request.session.get('name'):
#         response += "Name : {0} <br>".format(request.session.get('name'))
#     if request.session.get('password'):
#         response += "Password : {0} <br>".format(request.session.get('password'))
#         return HttpResponse(response)
#     else:
#         return redirect('create_session/')

