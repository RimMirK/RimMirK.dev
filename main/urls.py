from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import ProjectSitemap, ArticleSitemap, StaticViewSitemap
from django.templatetags.static import static
from django.views.generic import RedirectView

sitemaps = {
    "static": StaticViewSitemap,
    "projects": ProjectSitemap,
    "articles": ArticleSitemap,
}

def robots_txt(request):
    content = (
        "User-agent: *\n"
        "Disallow: /admin/\n"
    )
    return HttpResponse(content, content_type="text/plain")

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("projects/", views.projects_list, name="projects"),
    path("project/<str:project_slug>/", views.project_detail, name="project"),
    path("articles/", views.articles_list, name="articles"),
    path("article/<str:article_slug>/", views.article_detail, name="article"),
    path("projects_logos/<str:filename>", views.project_logo, name="project_logo"),
    path("donate/", views.donate, name='donate'),
    path("contacts/", views.contacts, name="contacts"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("favicon.ico", RedirectView.as_view(url=static('images/cat-rounded.png'))),
    path("robors.txt", robots_txt)
]

handler400 = "app.views.handler400"
handler403 = "app.views.handler403"
handler404 = "app.views.handler404"
handler500 = "app.views.handler500"
