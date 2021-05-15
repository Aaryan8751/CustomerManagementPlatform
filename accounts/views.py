from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.forms import inlineformset_factory

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from django.contrib import messages
# Create your views here.
from .models import *
from .form import CustomerForm, OrderForm, CreateUserForm
from .filters import OrderFilter
from .decorators import unauthenticated_user ,allowed_users, admin_only

@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()
    if(request.method == 'POST'):
        form = CreateUserForm(request.POST)
        if(form.is_valid()):
            user = form.save()
            username = form.cleaned_data.get('username')

            
            messages.success(request, "Account was created for " + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):

    if(request.method == "POST"):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if(user is not None):
            login(request, user)
            return redirect('home')

        else:
            messages.info(request, 'Username OR Password is incorrect')
    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer=request.user.customer
    form =CustomerForm(instance=customer)

    if (request.method=="POST"):
        form = CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid:
            form.save()
            
    context = {'form':form}
    return render(request, 'accounts/account_setting.html', context)


@login_required(login_url='login')
@admin_only
def home(request):
    Orders = Order.objects.all()
    Customers = Customer.objects.all()

    total_customers = Customers.count()

    total_order = Orders.count()
    delivered = Orders.filter(status="Delivered").count()
    pending = Orders.filter(status="Pending").count()

    context = {'orders': Orders, 'customers': Customers, "total_customers": total_customers,
               "total_order": total_order, "delivered": delivered, "pending": pending}
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_order = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()
    context = {'orders':orders,"pending":pending,"delivered":delivered,"total_order":total_order}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders = customer.order_set.all()
    total_customer_order = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {'customer': customer, 'orders': orders,
               "total_customer_order": total_customer_order, "myFilter": myFilter}
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):

    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    #form = OrderForm(initial={'customer':customer})
    if (request.method == 'POST'):
        #print('Printing POST: ',request.POST)
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if(formset.is_valid()):
            formset.save()
            return redirect('home')

    context = {'formset': formset}

    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):

    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if(request.method == "POST"):
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {"form": form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):

    order = Order.objects.get(id=pk)
    if (request.method == 'POST'):
        order.delete()
        return redirect('home')

    context = {"item": order}
    return render(request, 'accounts/delete.html', context)
