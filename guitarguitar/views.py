from django.shortcuts import render,redirect,get_object_or_404

# Create your views here.
def index(request):
    context_dict = {}
    return render(request, 'guitarguitar/index.html', context=context_dict)