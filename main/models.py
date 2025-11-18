from xmlrpc.client import Boolean
from django.db import models
from ckeditor.fields import RichTextField
from autoslug import AutoSlugField
from slugify import slugify
from django.forms import BooleanField


def make_slug(instance):
    base = slugify(instance.title)
    if instance.id:
        return f"{base}-{instance.id}"
    return base



class Index(models.Model):
    
    objects = models.Manager()
    
    subtitle = models.CharField(max_length=999)
    text = RichTextField()

    class Meta:
        verbose_name = 'Index'
        

class About(models.Model):
    content = RichTextField()
    comment = models.TextField(help_text="This text is NOT shown for users", blank=True)
    
class Contact(models.Model):
    content = RichTextField()
    comment = models.TextField(help_text="This text is NOT shown for users", blank=True)
    
class Donate(models.Model):
    content = RichTextField()
    comment = models.TextField(help_text="This text is NOT shown for users", blank=True)
    

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, editable=True)
    short_description = RichTextField()
    description = RichTextField()
    pinned = models.BooleanField()
    hidden = models.BooleanField()
    icon = models.ImageField(blank=True, upload_to='projects_logos')
    created_at = models.DateTimeField(auto_now_add=True)
    lastmod = models.DateTimeField(auto_now=True)
    comment = models.TextField(help_text="This text is NOT shown for users", blank=True)

    order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )
    
    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Project: {self.title}"
    
    def get_absolute_url(self):
        return f'/project/{self.slug}'



class ProjectLink(models.Model):
    parent = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="links")
    text = models.CharField(max_length=255)
    url = models.URLField()
    target = models.CharField(
        choices=[
            ('_blank', '_blank'),
            ('_self', '_self'),
            ('_parent', '_parent'),
            ('_top', '_top'),
            (None, 'framename')
        ],
        default="_self",
        blank=False,
    )
    style = models.CharField(
        choices=[
            ('link', 'Link'),
            ('btn', 'Button'),
            ('btn-ghost', 'Ghost Button')
        ], default='link'
    )
    extra_attrs = models.CharField(blank=True)
    
    order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )
    
    def __str__(self):
        return f"{self.text}"
    
    class Meta:
        ordering = ['order']


class Article(models.Model):
    title = models.CharField()
    hide_title = models.BooleanField(default=False)
    slug = AutoSlugField(
        populate_from=make_slug,
        unique=True,
        editable=True,
        blank=True,
        always_update=False,
    )
    description = RichTextField()
    read_btn = models.CharField(default='Read')
    content = RichTextField()
    hidden = models.BooleanField(default=False)
    author = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    unique_visitors = models.IntegerField(default=0)
    comment = models.TextField(help_text="This text is NOT shown for users", blank=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f'/article/{self.slug}'
    
    
class ArticleView(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True, editable=True)

