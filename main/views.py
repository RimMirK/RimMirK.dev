from django.shortcuts import render
from django.http import FileResponse
from . import models
from django.db.models import F
from .forms import ContactForm
from django.core.mail import send_mail
import os


def index(request):
    return render(request, "index.html", {
        'index': models.Index.objects.last(),
        'projects': models.Project.objects.filter(hidden=False, pinned=True).order_by('order'),
        'articles': models.Article.objects.filter(hidden=False).order_by('-created_at')[:5]
    })


def about(request):
    return render(request, "about.html", {'content': models.About.objects.last().content})


def contacts(request):
    sent = False

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            message = form.cleaned_data["message"]
            contact = form.cleaned_data["contact"]

            full_message = f"Имя: {name}\nКонтакт: {contact}\n\nСообщение:\n{message}"

            send_mail(
                subject="Новое сообщение с контактной формы",
                message=full_message,
                from_email=None,
                recipient_list=[os.environ['MY_EMAIL']], 
            )
            
            sent = True
    else:
        form = ContactForm()

    return render(
        request, "contacts.html",
        {"form": form, "sent": sent, 'content': models.Contact.objects.last().content})


def donate(request):
    return render(request, "donate.html", {'content': models.Donate.objects.last().content})


def projects_list(request):
    return render(request, "projects_list.html", {"projects": models.Project.objects.filter(hidden=False).order_by('order')})


def project_detail(request, project_slug):
    return render(request, "project_detail.html", {"project": models.Project.objects.get(slug=project_slug)})


def articles_list(request):
    return render(request, "articles_list.html", {
        'articles': models.Article.objects.filter(hidden=False).order_by('-created_at')
    })


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for: # if proxy
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def article_detail(request, article_slug):
    article = models.Article.objects.get(slug=article_slug)
    
    # add view
    models.Article.objects.filter(pk=article.pk).update(views=F('views') + 1)
    article.refresh_from_db()
    
    # add unique view
    ip = get_client_ip(request)
    if not models.ArticleView.objects.filter(article=article, ip=ip).exists():
        models.ArticleView.objects.create(article=article, ip=ip)
        models.Article.objects.filter(pk=article.pk).update(unique_visitors=F('unique_visitors') + 1)
        article.refresh_from_db()

    return render(request, "article_detail.html", {"article": article})


def project_logo(_, filename):
    return FileResponse(open(f"projects_logos/{filename}", 'rb'))


def handler400(request, exception):
    return render(request, "error.html", {
        "code": 400,
        "message": "Bad Request"
    }, status=400)

def handler403(request, exception):
    return render(request, "error.html", {
        "code": 403,
        "message": "Forbidden"
    }, status=403)

def handler404(request, exception):
    return render(request, "error.html", {
        "code": 404,
        "message": "Page Not Found"
    }, status=404)

def handler500(request):
    return render(request, "error.html", {
        "code": 500,
        "message": "Internal Server Error"

    }, status=500)


