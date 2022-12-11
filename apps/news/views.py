from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, permissions
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.news.filters import ReportFilter
from apps.news.models import Category, ReportImages, Report, Region
from apps.news.serializers import CategoryModelSerializer, ReportImageModelSerializer, ReportModelSerializer, \
    RegionModelSerializer


# Create your views here.
class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.order_by('-created_at')
    serializer_class = CategoryModelSerializer
    lookup_field = 'slug'


class ProductImageAPIView(GenericAPIView):
    queryset = ReportImages.objects.all()
    serializer_class = ReportImageModelSerializer
    parser_classes = (MultiPartParser,)

    def get(self, request):
        images = self.queryset.all()
        serializer = self.serializer_class(images, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class ReportModelViewSet(ModelViewSet):
    queryset = Report.objects.order_by('-created_at')
    serializer_class = ReportModelSerializer
    lookup_url_kwarg = 'id'
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['id', 'title']
    filterset_class = ReportFilter


class RegionApiView(GenericAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionModelSerializer
    
    def get(self, request):
        regions = self.queryset.all()
        serializer = self.serializer_class(regions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

