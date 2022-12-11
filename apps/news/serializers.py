from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from apps.news.models import Category, ReportImages, Report, Region


class CategoryModelSerializer(ModelSerializer):
    def validate(self, data):
        if Category.objects.filter(name=data['name']).exists():
            raise ValidationError('This category is already taken')
        return data

    class Meta:
        model = Category
        exclude = ('slug',)


class ReportImageModelSerializer(ModelSerializer):
    class Meta:
        model = ReportImages
        fields = '__all__'


class ReportModelSerializer(ModelSerializer):
    def to_representation(self, instance):
        represent = super().to_representation(instance)
        represent['images'] = ReportImageModelSerializer(instance.report_images.first()).data
        represent['category_id'] = CategoryModelSerializer(instance.category_id).data
        return represent


    class Meta:
        model = Report
        fields = '__all__'

class RegionModelSerializer(ModelSerializer):
    class Meta:
        def validate(self, data):
            if Region.objects.filter(name=data['name']).exists():
                raise ValidationError('This region is already taken')
            return data
        model = Region
        fields = ('name', )
