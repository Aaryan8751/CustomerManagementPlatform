from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from .models import *
from .form import OrderForm

def home(request):
    Orders = Order.objects.all()
    Customers = Customer.objects.all()

    total_customers = Customers.count()

    total_order = Orders.count()
    delivered = Orders.filter(status="Delivered").count()
    pending = Orders.filter(status="Pending").count()

    context = {'orders':Orders,'customers':Customers,"total_customers":total_customers,"total_order":total_order,"delivered":delivered,"pending":pending}
    return render(request,'accounts/dashboard.html',context)

def products(request):
    products = Product.objects.all()
    return render(request,'accounts/products.html',{'products':products})

def customer(request,pk_test):
    customer = Customer.objects.get(id=pk_test)
    
    orders = customer.order_set.all()
    
    total_customer_order = orders.count()
    context={'customer':customer,'orders':orders,"total_customer_order":total_customer_order}
    return render(request,'accounts/customer.html',context)

def createOrder(request):

    form = OrderForm()
    if (request.method=='POST'):
        #print('Printing POST: ',request.POST)
        form = OrderForm(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('home')

    context = {'form':form}

    return render(request,'accounts/order_form.html',context)