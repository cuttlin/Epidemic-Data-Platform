from django.shortcuts import render,HttpResponse
# Create your views here.
from .models import City, Leiji, Yiqingv2, Leijiworld, country_name_map, Leijitwomonth, \
    Provincehistory, Predict, Realtimenews,Rumors
import time,json

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
    yiqingv2 = Yiqingv2.objects.order_by('-timestamp')[0]
    return  render(request,'city.html',{'city':yiqingv2})

def chinatrend(request):
    # 湖北预测
    phhubei = Provincehistory.objects.filter(place="湖北")().order_by('-timestamp')[0]
    daydata = []
    for i in range(200):
        daydata.append(phhubei.dataList[i]['confirm'])
    prehubei = Predict.logistic(daydata=daydata,prdictday=207)
    # 河北预测
    phhebei = Provincehistory.objects.filter(place="河北")().order_by('-timestamp')[0]
    daydata2 = []
    for i in range(338,378):
        daydata2.append(phhebei.dataList[i]['confirm'])
    prehebei = Predict.logistic(daydata=daydata2, prdictday=20)
    # 湖北SEIR
    seirhubei = Predict.seir(people=60000000)
    # 河北SEIR
    seirhebei = Predict.seir(people=76000000)
    return render(request,'chinatrend.html',{'phhubei':phhubei,'prehubei':prehubei,\
                                             'phhebei':phhebei,'prehebei':prehebei,'looptimes':range(0,59),\
                                             'seirhubei':seirhubei,'seirhebei':seirhebei,'looptimes1':range(0,160),
                                             })

def world(request):
    leijiworld = Leijiworld.objects.order_by('-timestamp')[0]
    for item in leijiworld.countrydata['child']:
        try:
            item['name2'] = country_name_map[item['name2']]
            #print(item['name2'])
        except:
            print()

    return render(request,'world.html',{'leijiworld':leijiworld})

def worldtrend(request):
    return render(request,'worldtrend.html')

# 实时热点
def realtime(request):
    realtimenews = Realtimenews.objects.order_by('-timestamp')[0]
    for item in realtimenews.data['list']:
        item['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item['timestamp']/1000))

    return render(request,'realtime.html',{'news':realtimenews})

def rumor(request):
    rumors = Rumors.objects.order_by('-timestamp')[0]
    return render(request,'rumor.html',{'rumors':rumors})

def api(request):
    return render(request,'api.html')

#全球实时数据
def apiworldnow(request):
    result = Leijiworld.objects.order_by('-timestamp')[0]['countrydata']['child']
    return HttpResponse(json.dumps(result), content_type="application/json")

#国内实时数据
def apinow(request):
    result = Leijitwomonth.objects.order_by('-timestamp')[0]['dataList'][0]
    return HttpResponse(json.dumps(result), content_type="application/json")

#国内新闻数据
def apinews(request):
    result = Realtimenews.objects.order_by('-timestamp')[0]['data']
    return HttpResponse(json.dumps(result), content_type="application/json")

#国内谣言数据
def apirumors(request):
    result = Rumors.objects.order_by('-timestamp')[0]['data']
    return HttpResponse(json.dumps(result), content_type="application/json")