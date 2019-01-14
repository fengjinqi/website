from django.shortcuts import render

# Create your views here.


def List(request):
    return render(request,'pc/course/index.html')


def Detail(request,course_id):
    return render(request,'pc/course/detail.html')