from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets,mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from apps.article.views import StandardResultsSetPagination
from apps.support.models import Banners, Emails, link, QQ, Seo
from apps.uitls.permissions import IsOwnerOrReadOnly
from apps.support.serializers import BannersSerializer, EmailsSerializer, LinkSerializer, QQSerializer, SEOSerializer


def index(request):
    email = Emails.objects.first()
    return render(request,'pc/support.html',{'email':email})



class BannerList(viewsets.ModelViewSet):
    queryset = Banners.objects.all()
    serializer_class = BannersSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # 未登录禁止访问
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]
    pagination_class = StandardResultsSetPagination



class EmailsList(viewsets.ModelViewSet):
    queryset = Emails.objects.all()
    serializer_class = EmailsSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # 未登录禁止访问
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]
    pagination_class = StandardResultsSetPagination


class LinkList(viewsets.ModelViewSet):
    queryset = link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # 未登录禁止访问
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]
    pagination_class = StandardResultsSetPagination


class QQList(viewsets.ModelViewSet):
    queryset = QQ.objects.all()
    serializer_class = QQSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # 未登录禁止访问
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]


class SeoList(mixins.CreateModelMixin,mixins.DestroyModelMixin,mixins.ListModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    queryset = Seo.objects.all()
    serializer_class = SEOSerializer
    # permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # 未登录禁止访问
    # authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]