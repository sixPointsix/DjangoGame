from django.shortcuts import render #从服务端渲染一个js文件

def index(request):
    return render(request, "multiends/web.html")
