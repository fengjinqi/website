from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from apps.forum.models import Forum_plate
from apps.forum.serializers import Forum_plateSerializers
from apps.uitls.permissions import  IsOwnerOr


def index(request):
    return render(request,'pc/forum.html')











class Forum_plateView(mixins.UpdateModelMixin,mixins.CreateModelMixin,viewsets.ReadOnlyModelViewSet):
    """TODO 版块分類"""
    queryset = Forum_plate.objects.all()
    serializer_class = Forum_plateSerializers
    permission_classes = (IsAuthenticated, IsOwnerOr)  # 未登录禁止访问
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]