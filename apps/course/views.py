from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
from rest_framework import mixins, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from apps.article.views import StandardResultsSetPagination
from apps.course.models import Courses
from apps.course.serializers import CourseSerializers, CreatedCourseSerializers
from apps.uitls.permissions import IsOwnerOrReadOnly


def List(request):
    return render(request,'pc/course/index.html')


def Detail(request,course_id):
    return render(request,'pc/course/detail.html')




class CourseList(viewsets.ReadOnlyModelViewSet):
    queryset = Courses.objects.filter(is_delete=False)
    serializer_class = CourseSerializers
    pagination_class = StandardResultsSetPagination


class CourseCreatedList(mixins.CreateModelMixin,mixins.UpdateModelMixin,viewsets.ReadOnlyModelViewSet):
    queryset = Courses.objects.filter(is_delete=False)
    serializer_class = CreatedCourseSerializers
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # 未登录禁止访问
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]
