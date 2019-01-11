from django.shortcuts import render

# Create your views here.

def List(request):
    return render(request,'pc/course/index.html')