from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, F
from .models import Program, News, Staff, GalleryImage, Document, FAQ
from .forms import ApplicationForm, ContactForm


def home(request):
    context = {
        "programs": Program.objects.filter(is_active=True)[:8],
        "latest_news": News.objects.filter(is_published=True)[:3],
        "management": Staff.objects.filter(role="management")[:4],
        "gallery": GalleryImage.objects.all()[:8],
        "programs_count": Program.objects.filter(is_active=True).count(),
    }
    return render(request, "core/home.html", context)


def about(request):
    context = {
        "management": Staff.objects.filter(role="management"),
        "teachers": Staff.objects.filter(role="teacher"),
        "documents": Document.objects.all(),
    }
    return render(request, "core/about.html", context)


def programs(request):
    return render(request, "core/programs.html",
                  {"programs": Program.objects.filter(is_active=True)})


def program_detail(request, slug):
    program = get_object_or_404(Program, slug=slug, is_active=True)
    return render(request, "core/program_detail.html", {"program": program})


def admissions(request):
    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Arizangiz muvaffaqiyatli yuborildi! Tez orada siz bilan bog'lanamiz.")
            return redirect("admissions")
        messages.error(request, "Iltimos, maydonlarni to'g'ri to'ldiring.")
    else:
        form = ApplicationForm()
    context = {
        "form": form,
        "faqs": FAQ.objects.all(),
        "programs": Program.objects.filter(is_active=True),
    }
    return render(request, "core/admissions.html", context)


def news_list(request):
    qs = News.objects.filter(is_published=True)
    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(body__icontains=q))
    paginator = Paginator(qs, 6)
    page = paginator.get_page(request.GET.get("page"))
    return render(request, "core/news_list.html", {"page_obj": page, "q": q})


def news_detail(request, slug):
    item = get_object_or_404(News, slug=slug, is_published=True)
    News.objects.filter(pk=item.pk).update(views=F("views") + 1)
    related = News.objects.filter(is_published=True).exclude(pk=item.pk)[:3]
    return render(request, "core/news_detail.html", {"item": item, "related": related})


def gallery(request):
    return render(request, "core/gallery.html", {"images": GalleryImage.objects.all()})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Murojaatingiz yuborildi. Rahmat!")
            return redirect("contact")
        messages.error(request, "Iltimos, maydonlarni to'g'ri to'ldiring.")
    else:
        form = ContactForm()
    return render(request, "core/contact.html", {"form": form})


def search(request):
    q = request.GET.get("q", "").strip()
    news = programs_qs = []
    if q:
        news = News.objects.filter(
            Q(title__icontains=q) | Q(body__icontains=q), is_published=True)
        programs_qs = Program.objects.filter(
            Q(title__icontains=q) | Q(description__icontains=q), is_active=True)
    return render(request, "core/search.html",
                  {"q": q, "news": news, "programs": programs_qs})
