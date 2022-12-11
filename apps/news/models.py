import users
from django.contrib import auth
from django.contrib.postgres.fields import ArrayField
from django.db.models import CharField, SlugField, ForeignKey, CASCADE, TextField, SET_NULL, Model, IntegerField, \
    ImageField
from django.utils.text import slugify

from apps.shared import BaseModel

class Region(Model):
    name = CharField(max_length=255)

# Create your models here.
class Category(BaseModel):
    name = CharField(max_length=255)
    slug = SlugField(unique=True, blank=True)

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Category.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = self._get_unique_slug()
        if force_update is True:
            self.slug = slugify(self.name)
        super().save(self, force_update=False, using=None, update_fields=None)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categories'


class Report(BaseModel):
    category_id = ForeignKey(Category, CASCADE, 'category')
    title = CharField(max_length=255)
    slug = SlugField(unique=True, blank=True)
    author = ForeignKey('auth.User', CASCADE, 'author')
    region_id = ForeignKey(Region, CASCADE, 'region')
    views = IntegerField()
    text = TextField()
    hash_tags = ArrayField(CharField(max_length=255),default=list)

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Category.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = self._get_unique_slug()
        if force_update is True:
            self.slug = slugify(self.title)
        super().save(self, force_update=False, using=None, update_fields=None)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'reports'

    @property
    def report_images(self):
        return self.report_images.all()


class ReportImages(BaseModel):
    image = ImageField(upload_to='media/products/')
    product = ForeignKey(Report, CASCADE, 'report_images')

    class Meta:
        db_table = 'images'
