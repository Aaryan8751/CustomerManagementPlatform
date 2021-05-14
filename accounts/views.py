from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
# Create your views here.
from .models import *
from .form import OrderForm
from .filters import OrderFilter

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

    myFilter =OrderFilter(request.GET,queryset=orders)
    orders = myFilter.qs
    context={'customer':customer,'orders':orders,"total_customer_order":total_customer_order,"myFilter":myFilter}
    return render(request,'accounts/customer.html',context)

def createOrder(request,pk):

    OrderFormSet = inlineformset_factory(Customer,Order, fields=('product','status'),extra=5)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    #form = OrderForm(initial={'customer':customer})
    if (request.method=='POST'):
        #print('Printing POST: ',request.POST)
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST,instance=customer)
        if(formset.is_valid()):
            formset.save()
            return redirect('home')

    context = {'formset':formset}

    return render(request,'accounts/order_form.html',context)

def updateOrder(request,pk):

    order =Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if(request.method=="POST"):
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {"form":form}
    return render(request,'accounts/order_form.html',context)

def deleteOrder(request,pk):
    
    order = Order.objects.get(id=pk)
    if (request.method=='POST'):
        order.delete()
        return redirect('home')


    context = {"item":order}
    return render(request,'accounts/delete.html',context)