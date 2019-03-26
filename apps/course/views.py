import json

from django.core.paginator import PageNotAnInteger
from django.shortcuts import render, get_object_or_404
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
    """TODO 教程列表  a标签根据uuid进 Detail视图渲染对应的所有文章"""
    course = Courses.objects.all()
    return render(request,'pc/course/index.html',{'course':course})


def Detail(request,course_id,list_id):
    """TODO 文章视图 根据uuid来查询对应所有文章
        页面左侧要渲染所有的title标题
        右侧对应当前标题内容
        我的文章目录就是所有的文章 ，但是我只渲染了title标题，右侧就渲染对应标题的内容
        现在问题是我懵逼了，貌似这个视图不能同时拿到uuid和id 只能二选一
    """
    course_list = CourseList.objects.filter(course=course_id)#根据文章列表uuid查询对应的文章
    #course_list.filter(id='')#根据对应文章id 来获取对应的数据
    content = get_object_or_404(course_list, pk=list_id)
    previous_blog = course_list.filter(id__gt=list_id).first()
    netx_blog = course_list.filter(id__lt=list_id).last()
    return render(request,'pc/course/detail.html',{'course':course_list,'uuid':course_id,'content':content,'previous_blog':previous_blog,'netx_blog':netx_blog})


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




class MeCoursesList(viewsets.ReadOnlyModelViewSet):
    queryset = Courses.objects.filter(is_delete=False)
    serializer_class = CourseSerializers
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # 未登录禁止访问
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Courses.objects.filter(user=self.request.user)

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

