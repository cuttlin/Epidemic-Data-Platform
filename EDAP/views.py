from django.shortcuts import render,HttpResponse
from django.db.models import Max
# Create your views here.
from .models import City, Overviewchina


def hello(request):
    context = {}
    context['hello'] = 'hello world'
    return render(request,'hello.html',context)

def index(request):
    return render(request,'index.html')

def service(request):
    #City.objects.create(name='999',size='999')
    return render(request,'service.html')

def home(request):
    overviewchina = Overviewchina.objects.aggregate(Max('timestamp'))
    print(overviewchina)
    return render(request,'home.html')