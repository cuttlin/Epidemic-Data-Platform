from django.shortcuts import render,HttpResponse
from django.db.models import Max
# Create your views here.
from .models import City, Leiji


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
    #context['quezhen_xianyou_add'] = int(leiji.dataList[0]['quezhen_xianyou'])-int(leiji.dataList[1]['quezhen_xianyou'])
    return render(request,'home.html',{'leiji':leiji,'context':context})