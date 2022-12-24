from django.db import models
from django.forms import URLField
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    is_private = models.BooleanField(default=False)
    create_date = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    modify_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    def get_absolute_url(self):
        return "/category/%s/" % self.slug

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Link(models.Model):
    category = models.ManyToManyField(Category, related_name='categorylist')
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    url = models.URLField(max_length=250, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_private = models.BooleanField(default=False)
    count_access = models.IntegerField(default=0)
    create_date = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    modify_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Link, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Links'

    def __str__(self):
        return self.name
