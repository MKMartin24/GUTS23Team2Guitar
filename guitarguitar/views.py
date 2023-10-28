from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from guitarguitar.data import Order,Product,Customer

# Create your views here.

def index(request):
    context_dict = {"orders":Order.load_api()}
    #print(context_dict)
    return render(request, 'guitarguitar/index.html', context=context_dict)


def view_orders(request):
    context_dict = {"orders":Order.load_api()}
    print(context_dict)
    return render(request, 'guitarguitar/orders.html', context=context_dict)

def view_customers(request):
    context_dict = {"customers":Customer.load_api()}
    print(context_dict)
    return render(request, 'guitarguitar/customers.html', context=context_dict)

def view_products(request):
    context_dict = {"products":Product.load_api()}
    print(context_dict)
    return render(request, 'guitarguitar/products.html', context=context_dict)

def login(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        customers = Customer.load_api()
        email = request.POST.get('email')
        if email is not None and any([customer.email == email for customer in customers]):
            response = redirect(reverse('guitarguitar:index'))
            response.set_cookie('login', email)
            return response
        else:
            return render(request, 'guitarguitar/login.html')
    else:
        return render(request, 'guitarguitar/login.html')

def logout(request: HttpRequest) -> HttpResponse:
    response = redirect(reverse('guitarguitar:index'))
    response.delete_cookie('login')
    return response
