import json

from django.core.paginator import PageNotAnInteger
from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
# Create your views here.
from django.views.generic.base import View
from django_filters.rest_framework import DjangoFilterBackend
from pure_pagination import Paginator
from rest_framework import mixins, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from apps.article.views import StandardResultsSetPagination
from apps.course.filter import CoursesFilter
from apps.course.models import Courses, CourseList
from apps.course.serializers import CourseSerializers, CreatedCourseSerializers, AddtutorialSerializers
from apps.uitls.jsonserializable import DateEncoder
from apps.uitls.permissions import IsOwnerOrReadOnly, IsOwnerOrRead


def List(request):
    return render(request,'pc/course/index.html')


def Detail(request,course_id):
    return render(request,'pc/course/detail.html')


def courseViewApi(request,courses_id):
    course = Courses.objects.get(pk=courses_id)
    course_list = course.courselist_set.all()
    try:
        page = request.GET.get('page', 1)

        if page == '':
            page = 1
    except PageNotAnInteger:
        page = 1
    p = Paginator(course_list,10,request=request)
    people = p.page(page)
    print(people.object_list)
    print(people.next_page_number)
    return HttpResponse()


class CoursesList(viewsets.ReadOnlyModelViewSet):
    queryset = Courses.objects.filter(is_delete=False)
    serializer_class = CourseSerializers
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # 未登录禁止访问
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]
    pagination_class = StandardResultsSetPagination


class CourseCreatedList(mixins.CreateModelMixin,mixins.UpdateModelMixin,viewsets.ReadOnlyModelViewSet):
    queryset = Courses.objects.filter(is_delete=False)
    serializer_class = CreatedCourseSerializers
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # 未登录禁止访问
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]
    filter_backends = (DjangoFilterBackend,)
    filter_class = CoursesFilter


class CourseListCreated(mixins.CreateModelMixin,mixins.UpdateModelMixin,viewsets.ReadOnlyModelViewSet):
    queryset = CourseList.objects.all()
    serializer_class = AddtutorialSerializers
    permission_classes = (IsAuthenticated, IsOwnerOrRead)  # 未登录禁止访问
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]

