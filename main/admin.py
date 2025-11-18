
from pyexpat import model
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin, SortableAdminBase, SortableStackedInline
from django.contrib import admin
from . import models
from . import forms


def get_singleton_class(cls):
    class SingletonModelAdmin(admin.ModelAdmin):
        def has_add_permission(self, request):
            return not cls.objects.exists()
    return SingletonModelAdmin



admin.site.register(models.Index,  get_singleton_class(models.Index))
admin.site.register(models.About,  get_singleton_class(models.About))
admin.site.register(models.Contact,get_singleton_class(models.Contact))
admin.site.register(models.Donate, get_singleton_class(models.Donate))


class LinkInline(SortableStackedInline, admin.StackedInline):
    model = models.ProjectLink
    extra = 3
    form = forms.ProjectLinkAdminForm

@admin.register(models.Project)
class ProjectAdmin(SortableAdminMixin, admin.ModelAdmin):
    inlines = [LinkInline]
    list_display = ['pinned', 'title', 'order']
    list_editable = ['pinned']
    list_display_links = ['title']


admin.site.register(models.Article)