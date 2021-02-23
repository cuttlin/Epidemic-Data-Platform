from django.shortcuts import render,HttpResponse
from django.db.models import Max
# Create your views here.
from .models import City, Leiji, Yiqingv2


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
    leiji = Leiji.objects.order_by('-timestamp')[0]
    context = {}
    yiqingv2 = Yiqingv2.objects.order_by('-timestamp')[0]
    dl = yiqingv2.dataList
    print(type(dl))
    return render(request,'home.html',{'leiji':leiji,'dl':dl})