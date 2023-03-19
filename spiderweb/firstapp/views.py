import subprocess

from django.http import HttpResponse
from django.shortcuts import render, redirect
import os
from django.http import HttpResponse, FileResponse

def home(request):
    if request.method == "POST":
        name = request.POST.get("name")
        maxval = request.POST.get('max')
        runtime = request.POST.get('runtime')
        print(name,maxval,runtime)
        try:
            spider_name = 'my_spider'
            process = subprocess.Popen(['scrapy', 'crawl', spider_name, '-a', 'names=%s' % name, '-a', 'maxval=%s' % maxval, '-a', 'runtime=%s' % runtime])
            process.wait()

            # download the XLSX file
            file_path = os.path.join(os.getcwd(), 'outputnew.xlsx')
            response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename='outputnew.xlsx')
            return response
        except Exception as e:
                print('Error', str(e))
    return render(request, "firstapp/list.html")

def running(request):
    return render(request, "firstapp/runing.html")