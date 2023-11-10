from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm,CreateUserForm
from .filters import OrderFilter
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users,admin_only
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages 
from .decorators import unauthenticated_user
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout

@unauthenticated_user
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()  # Use your custom CreateUserForm

        if request.method == 'POST':
            form = CreateUserForm(request.POST)

            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                group = Group.objects.get(name='clients')
                user.groups.add(group)

                messages.success(request, 'Account created for ' + username)

                return redirect('login')

    context = {'form': form}
    return render(request, 'offres/register.html', context)
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username= request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(request, username=username,password=password)

        if user is not None:
                login(request,user)
                return redirect('home')
        else:
                messages.info(request,'Username or password is uncorrect')

    context ={}
    return render(request,'offres/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
    orders=Order.objects.all()
    customers = Customer.objects.all()
    total_customers=customers.count()
    total_orders=orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending =orders.filter(status="Pending").count()
       # Debugging print statements
    print("Total Customers:", total_customers)
    print("Total Orders:", total_orders)
    print("Delivered Orders:", delivered)
    print("Pending Orders:", pending)
    context = {'orders' :orders, 'customers':customers,' total_orders': total_orders,' delivered': delivered,' pending': pending}

    return render(request,'offres/dashboard.html',context)
def userPage(request):
    context = {}
    return render(request, 'offres/user.html', context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admins'])
def products(request):
    products = Product.objects.all()
    return render(request,'offres/products.html',{'products':products})


@login_required(login_url='login')

@allowed_users(allowed_roles=['Admins'])
def customer(request,pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    order_count =orders.count()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context ={'customer':customer,'orders':orders,'order_count':order_count,'myFilter':myFilter}
    return render(request,'offres/customer.html',context)

@login_required(login_url='login')

@allowed_users(allowed_roles=['Admins'])
def createOrder(request):
    form = OrderForm()
    if request.method == 'POST':
      #  print('Printing POST:',request.POST)
      form =OrderForm(request.POST)
      if form.is_valid():
          form.save()
          return redirect('/')

    context = {'form':form}
    return render(request,'offres/order_form.html',context)


@login_required(login_url='login')

@allowed_users(allowed_roles=['Admins'])

def updateOrder(request, pk):
    # Retrieve the order object based on the primary key (pk)
    order = get_object_or_404(Order, id=pk)
    
    if request.method == 'POST':
        # Populate the form with the POST data and the order instance
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            # Save the updated order
            form.save()
            return redirect('/')
    else:
        # If it's a GET request, initialize the form with the order data
        form = OrderForm(instance=order)
    
    context = {'form': form}
    return render(request, 'offres/order_form.html', context)
@login_required(login_url='login')

@allowed_users(allowed_roles=['Admins'])
def deleteOrder(request, pk):
    try:
        order = get_object_or_404(Order, id=pk)
        if request.method == 'POST':
            order.delete()
            return redirect('/')
    except Order.DoesNotExist:
        # Handle the case where the order doesn't exist
        # You can return an error message or redirect to a different page
        # For example, you can add a message and redirect to the home page
        messages.error(request, 'Order does not exist')
        return redirect('home')
    
    context = {'item': order}
    return render(request, 'offres/delete.html', context)