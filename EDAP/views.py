from django.shortcuts import render,HttpResponse

# Create your views here.
from . models import City

def hello(request):
    context = {}
    context['hello'] = 'hello world'
    return render(request,'hello.html',context)

def index(request):
    return render(request,'index.html')
def service(request):
    City.objects.create(name='999',size='999')
    return render(request,'service.html')

def home(request):
    return render(request,'home.html')