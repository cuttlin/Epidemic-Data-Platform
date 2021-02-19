from django.shortcuts import render
# Create your views here.
def hello(request):
    context = {}
    context['hello'] = 'hello world'
    return render(request,'hello.html',context)

def index(request):
    return render(request,'index.html')