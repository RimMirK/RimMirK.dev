from django.contrib.sitemaps import Sitemap
from .models import Project, Article
from django.urls import reverse


class ProjectSitemap(Sitemap):
    changefreq = "monthly"

    def items(self):
        return Project.objects.filter(hidden=False)

    def lastmod(self, obj):
        return obj.lastmod

    def location(self, obj):
        return obj.get_absolute_url()

    def priority(self, obj):
        return 0.9 if obj.pinned else 0.7


class ArticleSitemap(Sitemap):
    changefreq = "weekly"

    def items(self):
        return Article.objects.filter(hidden=False)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()

    def priority(self, obj):
        return 0.8


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority_value = {
        "index": 1.0,
        "about": 0.7,
        "donate": 0.6,
        "projects": 0.65,
        "articles": 0.65,
        "contacts": 0.5,
    }

    def items(self):
        return list(self.priority_value.keys())

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return self.priority_value.get(item, 0.5)
