from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from apps.forum.models import Forum_plate, Forum
from apps.forum.serializers import Forum_plateSerializers, ForumSerializers
from apps.uitls.permissions import  IsOwnerOr


def index(request):
    plate = Forum_plate.objects.all()
    forum = Forum.objects.all()
    return render(request,'pc/forum.html',locals())











class Forum_plateView(mixins.UpdateModelMixin,mixins.CreateModelMixin,viewsets.ReadOnlyModelViewSet):
    """TODO 版块分類"""
    queryset = Forum_plate.objects.all()
    serializer_class = Forum_plateSerializers
    permission_classes = (IsAuthenticated, IsOwnerOr)  # 未登录禁止访问
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]


class ForumView(viewsets.ModelViewSet):
    """TODO 版块分類"""
    queryset = Forum.objects.all()
    serializer_class = ForumSerializers
    permission_classes = (IsAuthenticated, IsOwnerOr)  # 未登录禁止访问
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]