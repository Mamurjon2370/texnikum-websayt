import os

from django.core.files.storage import default_storage
from django.db import models
from django.utils import timezone


def document_storage():
    # Callable storage: Django migratsiyalarda buni import yo'li sifatida saqlaydi,
    # shu bois muhitdan (Cloudinary bor/yo'q) mustaqil, barqaror migratsiya bo'ladi.
    if os.environ.get("CLOUDINARY_URL"):
        from cloudinary_storage.storage import RawMediaCloudinaryStorage
        return RawMediaCloudinaryStorage()
    return default_storage


class SiteSettings(models.Model):
    """Sayt umumiy sozlamalari (bitta yozuv)."""
    name = models.CharField("Texnikum nomi", max_length=255,
                            default="O'zbekiston tuman 2-son texnikumi")
    short_name = models.CharField("Qisqa nom", max_length=100, default="2-son texnikum")
    slogan = models.CharField("Shior", max_length=255, blank=True,
                              default="O'rta bo'g'in kadrlarni yetishtirish")
    about_short = models.TextField("Qisqacha tavsif", blank=True)
    founded_year = models.CharField("Tashkil topgan yil", max_length=20, default="1973")
    address = models.CharField("Manzil", max_length=255,
                               default="O'zbekiston tuman, Tuyul MFY, Do'stlarobod qo'rg'oni 102-uy")
    phone = models.CharField("Telefon", max_length=100, default="+998 91-154-56-97")
    email = models.EmailField("E-mail", default="uzbekistandistrict2ps@gmail.com")
    work_hours = models.CharField("Ish vaqti", max_length=255, default="Dushanba-Shanba, 08:00-17:00")
    ministry = models.CharField("Vazirlik", max_length=255,
                                default="Oliy ta'lim, fan va innovatsiyalar vazirligi huzuridagi Kasbiy ta'lim agentligi")
    logo = models.ImageField("Logotip", upload_to="site/", blank=True, null=True)
    map_embed = models.TextField("Xarita (Google Maps embed URL)", blank=True,
                                 default="https://www.google.com/maps?q=Uzbekistan&output=embed")
    telegram = models.URLField("Telegram", blank=True)
    instagram = models.URLField("Instagram", blank=True)
    facebook = models.URLField("Facebook", blank=True)
    youtube = models.URLField("YouTube", blank=True)

    class Meta:
        verbose_name = "Sayt sozlamalari"
        verbose_name_plural = "Sayt sozlamalari"

    def __str__(self):
        return self.name

    @classmethod
    def get(cls):
        obj = cls.objects.first()
        if obj is None:
            obj = cls.objects.create()
        return obj


class Program(models.Model):
    """Ta'lim yo'nalishi / mutaxassislik."""
    title = models.CharField("Yo'nalish nomi", max_length=255)
    slug = models.SlugField("Slug", unique=True)
    description = models.TextField("Tavsif", blank=True)
    duration = models.CharField("O'qish muddati", max_length=100, default="2 yil")
    diploma = models.CharField("Diplom turi", max_length=255,
                               default="Boshlang'ich professional ta'lim")
    icon = models.CharField("Ikonka (bootstrap-icons nomi)", max_length=100,
                            default="mortarboard", blank=True)
    image = models.ImageField("Rasm", upload_to="programs/", blank=True, null=True)
    grant_places = models.PositiveIntegerField("Grant o'rinlari", default=0)
    contract_places = models.PositiveIntegerField("Kontrakt o'rinlari", default=0)
    contract_price = models.CharField("Kontrakt summasi", max_length=100, blank=True)
    language = models.CharField("O'qish tili", max_length=100, default="O'zbek tili")
    order = models.PositiveIntegerField("Tartib", default=0)
    is_active = models.BooleanField("Faol", default=True)

    class Meta:
        verbose_name = "Yo'nalish"
        verbose_name_plural = "Yo'nalishlar"
        ordering = ["order", "title"]

    def __str__(self):
        return self.title


class NewsCategory(models.Model):
    name = models.CharField("Nomi", max_length=100)
    slug = models.SlugField("Slug", unique=True)

    class Meta:
        verbose_name = "Yangilik toifasi"
        verbose_name_plural = "Yangilik toifalari"

    def __str__(self):
        return self.name


class News(models.Model):
    """Yangiliklar / e'lonlar."""
    title = models.CharField("Sarlavha", max_length=255)
    slug = models.SlugField("Slug", unique=True, max_length=255)
    category = models.ForeignKey(NewsCategory, verbose_name="Toifa", on_delete=models.SET_NULL,
                                 null=True, blank=True, related_name="news")
    summary = models.CharField("Qisqa mazmun", max_length=300, blank=True)
    body = models.TextField("Matn")
    image = models.ImageField("Rasm", upload_to="news/", blank=True, null=True)
    published_at = models.DateTimeField("Chop etilgan sana", default=timezone.now)
    is_published = models.BooleanField("Chop etilgan", default=True)
    views = models.PositiveIntegerField("Ko'rishlar", default=0)

    class Meta:
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangiliklar"
        ordering = ["-published_at"]

    def __str__(self):
        return self.title


class Staff(models.Model):
    """Rahbariyat va o'qituvchilar."""
    ROLE_CHOICES = [
        ("management", "Rahbariyat"),
        ("teacher", "O'qituvchi"),
        ("staff", "Xodim"),
    ]
    full_name = models.CharField("F.I.O.", max_length=255)
    position = models.CharField("Lavozimi", max_length=255)
    role = models.CharField("Turi", max_length=20, choices=ROLE_CHOICES, default="teacher")
    photo = models.ImageField("Rasm", upload_to="staff/", blank=True, null=True)
    bio = models.TextField("Ma'lumot", blank=True)
    phone = models.CharField("Telefon", max_length=100, blank=True)
    email = models.EmailField("E-mail", blank=True)
    order = models.PositiveIntegerField("Tartib", default=0)

    class Meta:
        verbose_name = "Xodim"
        verbose_name_plural = "Rahbariyat va o'qituvchilar"
        ordering = ["role", "order", "full_name"]

    def __str__(self):
        return f"{self.full_name} - {self.position}"


class Application(models.Model):
    """Abituriyent onlayn arizasi."""
    STATUS_CHOICES = [
        ("new", "Yangi"),
        ("review", "Ko'rib chiqilmoqda"),
        ("accepted", "Qabul qilindi"),
        ("rejected", "Rad etildi"),
    ]
    full_name = models.CharField("F.I.O.", max_length=255)
    birth_date = models.DateField("Tug'ilgan sana", null=True, blank=True)
    phone = models.CharField("Telefon", max_length=100)
    email = models.EmailField("E-mail", blank=True)
    program = models.ForeignKey(Program, verbose_name="Yo'nalish", on_delete=models.SET_NULL,
                                null=True, related_name="applications")
    prev_school = models.CharField("Oldingi o'quv muassasasi", max_length=255, blank=True)
    message = models.TextField("Qo'shimcha ma'lumot", blank=True)
    status = models.CharField("Holati", max_length=20, choices=STATUS_CHOICES, default="new")
    created_at = models.DateTimeField("Yuborilgan sana", auto_now_add=True)

    class Meta:
        verbose_name = "Ariza"
        verbose_name_plural = "Onlayn arizalar"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} ({self.get_status_display()})"


class ContactMessage(models.Model):
    """Aloqa / murojaat shakli xabarlari."""
    name = models.CharField("Ism", max_length=255)
    email = models.EmailField("E-mail", blank=True)
    phone = models.CharField("Telefon", max_length=100, blank=True)
    subject = models.CharField("Mavzu", max_length=255, blank=True)
    message = models.TextField("Xabar")
    is_read = models.BooleanField("O'qilgan", default=False)
    created_at = models.DateTimeField("Sana", auto_now_add=True)

    class Meta:
        verbose_name = "Murojaat"
        verbose_name_plural = "Murojaatlar"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name}: {self.subject or 'murojaat'}"


class GalleryImage(models.Model):
    title = models.CharField("Sarlavha", max_length=255, blank=True)
    image = models.ImageField("Rasm", upload_to="gallery/")
    order = models.PositiveIntegerField("Tartib", default=0)

    class Meta:
        verbose_name = "Galereya rasmi"
        verbose_name_plural = "Fotogalereya"
        ordering = ["order"]

    def __str__(self):
        return self.title or f"Rasm #{self.pk}"


class Document(models.Model):
    """Meyoriy hujjatlar, litsenziyalar (PDF)."""
    title = models.CharField("Nomi", max_length=255)
    file = models.FileField("Fayl", upload_to="documents/", storage=document_storage)
    uploaded_at = models.DateTimeField("Yuklangan sana", auto_now_add=True)

    class Meta:
        verbose_name = "Hujjat"
        verbose_name_plural = "Hujjatlar"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.title


class FAQ(models.Model):
    """Tez-tez so'raladigan savollar."""
    question = models.CharField("Savol", max_length=300)
    answer = models.TextField("Javob")
    order = models.PositiveIntegerField("Tartib", default=0)

    class Meta:
        verbose_name = "Savol-javob"
        verbose_name_plural = "FAQ (tez-tez so'raladigan savollar)"
        ordering = ["order"]

    def __str__(self):
        return self.question
