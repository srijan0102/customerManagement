from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib import messages
from django.urls import reverse
from .filters import OrderFilter
from .decorators import permission_grated, admin_extended_permission
from .models import *
from .forms import *

#Authentication
def login_user(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('accounts:home')) #dyamic url 
        else:
            if not User.objects.get(username=username).is_active:
                messages.info(request, 'Please contact to the administrator.')
            else:
                messages.info(request, 'Username or password is incorrect')    
                  
    return render(request, 'login.html')


def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            # ADD user in the group # Implement this using signals
            # group = Group.objects.get(name='CUSTOMER')
            # user.groups.add(group)
            # Create Customer
            # Customer.objects.create(user=user, email=form.cleaned_data.get('email')) # Implement this using signals
            messages.success(request, 'Accounts was created for ' + username)
            return redirect(reverse('accounts:login'))
    context={
        'form' : form,
    }
    return render(request, 'register.html', context=context)

def logout_user(request):
    logout(request)
    return redirect(reverse('accounts:login'))

@permission_grated(allowed_roles=['CUSTOMER'])
def account_profile(request):
    form = CustomerForm(instance=request.user.customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=request.user.customer)
        if form.is_valid():
            form.save()
    context = {
        'form': form
    }
    return render(request, 'edit_profile.html', context=context)
    

#Home
@admin_extended_permission
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customer = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='DELIVERED').count()
    pending = orders.filter(status='PENDING').count()
    context = {'orders': orders,
                'customers': customers,
                'total_customer': total_customer,
                 'total_orders': total_orders,
                 'delivered': delivered,
                 'pending': pending}
    return render(request, 'dashboard.html', context=context)

#Product
@permission_grated(allowed_roles=['ADMIN'])
def products(request):
    products = Product.objects.all()
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    return render(request, 'products.html', context={'products':products})

#Customers
@permission_grated(allowed_roles=['CUSTOMER'])
def customer_profile(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='DELIVERED').count()
    pending = orders.filter(status='PENDING').count()
    context = {
        'orders':orders,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending
    }
    return render(request, 'customer_profile.html', context=context)

@permission_grated(allowed_roles=['ADMIN'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = Order.objects.filter(customer=customer)
    total_orders = orders.count()
    order_filter = OrderFilter(request.GET, queryset=orders)
    orders = order_filter.qs
    context = {
        'customer': customer,
        'orders': orders,
        'total_orders': total_orders,
        'order_filter': order_filter
    }
    return render(request, 'customer.html', context=context)

#ORDER
@permission_grated(allowed_roles=['ADMIN'])
def create_order(request, customer_pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10) # fields are selected columns of child model Order
    customer = Customer.objects.get(id=customer_pk)
    formset = OrderFormSet(queryset =Order.objects.none(), instance=customer) # queryset =Order.objects.none() hide filled form data    
    # forms = OrderForm(initial={'customer': customer})
    if request.method == 'POST':
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect(reverse('accounts:home'))
            
    context={
        'form': formset
    }
    return render(request, 'order_form.html', context=context)

@permission_grated(allowed_roles=['ADMIN'])
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    forms = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:home'))
    context={
        'form': forms
    }
    return render(request, 'order_form.html', context=context)

@permission_grated(allowed_roles=['ADMIN'])
def delete_order(request, pk):
    order =Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect(reverse('accounts:home'))
    context={
        'item': order
    }
    return render(request, 'delete.html', context=context)