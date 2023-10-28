from django.shortcuts import render,redirect,get_object_or_404
from guitarguitar.data import Order

# Create your views here.
def index(request):
    context_dict = {"orders":Order.load_api()}
    print(context_dict)
    return render(request, 'guitarguitar/index.html', context=context_dict)