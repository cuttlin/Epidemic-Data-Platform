from django.shortcuts import render,HttpResponse
from django.db.models import Max
# Create your views here.
from .models import City, Leiji, Yiqingv2, Leijiworld, country_name_map, Leijitwomonth


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
    leijitwomonth = Leijitwomonth.objects.order_by('-timestamp')[0]
    leiji = Leiji.objects.order_by('-timestamp')[0]
    context = {}
    yiqingv2 = Yiqingv2.objects.order_by('-timestamp')[0]
    dl = yiqingv2.dataList
    return render(request,'home.html',{'leiji':leiji,'dl':dl,'lj2':leijitwomonth})

def city(request):
    return  render(request,'city.html')

def world(request):
    leijiworld = Leijiworld.objects.order_by('-timestamp')[0]
    for item in leijiworld.countrydata['child']:
        try:
            item['name2'] = country_name_map[item['name2']]
            #print(item['name2'])
        except:
            print()

    return render(request,'world.html',{'leijiworld':leijiworld})