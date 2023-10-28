from django.shortcuts import render,redirect,get_object_or_404
from guitarguitar.data import Order,Product,Customer

# Create your views here.
def index(request):
    context_dict = {"orders":Order.load_api()}
    print(context_dict)
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