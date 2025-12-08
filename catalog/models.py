from django.db import models
from django.db import models
from django.utils import timezone
from django.db import models
from django.utils import timezone


from django.db import models
from django.utils import timezone


class Section(models.TextChoices):
    USEFUL_LINKS = "useful_links", "Links úteis"
    HOW_TO      = "how_to", "Como solicitar"
    PHONES      = "phones", "Telefones úteis"
    ADDRESSES   = "addresses", "Endereços"
    VIDEOS      = "videos", "Vídeos"

    # Novos blocos
    WHATSAPP_ACCOMMODATION = "whatsapp_accommodation", "WhatsApp (acomodação)"
    JOB_SITES    = "job_sites", "Sites de emprego"
    JOB_FACEBOOK = "fb_jobs_group", "Grupos de emprego (Facebook)"
    DAILY_APPS   = "daily_apps", "Apps úteis"



class Resource(models.Model):
    section     = models.CharField(max_length=32, choices=Section.choices)
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    url         = models.URLField(blank=True)               # links, vídeos, grupos, sites
    phone       = models.CharField(max_length=50, blank=True)   # telefones
    address     = models.CharField(max_length=255, blank=True)  # endereços
    is_official = models.BooleanField(default=False)
    country     = models.CharField(max_length=2, blank=True)    # "IE", "BR", etc. ou ""
    locale      = models.CharField(max_length=10, default="en") # "pt-br", "en", "es"...
    sort_order  = models.IntegerField(default=0)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(default=timezone.now, editable=False)
    # usamos default em vez de auto_now pra não quebrar fixtures/loaddata
    updated_at  = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(
                fields=["section", "locale", "country", "is_active", "sort_order"]
            ),
        ]
        ordering = ["section", "sort_order", "id"]

    def __str__(self):
        return f"{self.section} | {self.title}"


class ClickEvent(models.Model):
    link       = models.ForeignKey(
        Resource,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="clicks",
    )
    locale     = models.CharField(max_length=10, blank=True)
    country    = models.CharField(max_length=2, blank=True)
    referrer   = models.TextField(blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["link"]),
            models.Index(fields=["locale", "country"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"Click {self.id} -> {self.link_id or 'none'}"


class AdSlot(models.Model):
    position   = models.CharField(
        max_length=32,
        choices=[("hero", "hero"), ("sidebar", "sidebar"), ("footer", "footer")],
    )
    country    = models.CharField(max_length=2, blank=True)  # "" = global
    title      = models.CharField(max_length=120, blank=True)
    image_url  = models.URLField(blank=True)
    target_url = models.URLField(blank=True)
    html_embed = models.TextField(blank=True)                # opcional
    is_active  = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)
    starts_at  = models.DateTimeField(null=True, blank=True)
    ends_at    = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=["position", "country", "is_active"]),
        ]
        ordering = ["position", "sort_order", "id"]

    def __str__(self):
        return f"{self.position} | {self.country or 'GLOBAL'} | {self.title or self.id}"



# class Section(models.TextChoices):
#     USEFUL_LINKS = "useful_links", "Links úteis"
#     HOW_TO      = "how_to", "Como solicitar"
#     PHONES      = "phones", "Telefones úteis"
#     ADDRESSES   = "addresses", "Endereços"
#     VIDEOS      = "videos", "Vídeos"

# class Resource(models.Model):
#     section     = models.CharField(max_length=32, choices=Section.choices)
#     title       = models.CharField(max_length=200)
#     description = models.TextField(blank=True)
#     url         = models.URLField(blank=True)          # links e vídeos
#     phone       = models.CharField(max_length=50, blank=True)   # telefones
#     address     = models.CharField(max_length=255, blank=True)   # endereços
#     is_official = models.BooleanField(default=False)
#     country     = models.CharField(max_length=2, blank=True)     # “IE” agora; depois BR/MX/IN
#     locale      = models.CharField(max_length=10, default='en')  # “pt-br”, “en”, etc.
#     sort_order  = models.IntegerField(default=0)
#     is_active   = models.BooleanField(default=True)
#     created_at = models.DateTimeField(default=timezone.now, editable=False)
#     updated_at = models.DateTimeField(default=timezone.now)  # ← em vez de auto_now=True
#     # created_at  = models.DateTimeField(auto_now_add=True)
#     # updated_at  = models.DateTimeField(auto_now=True)

#     class Meta:
#         indexes = [
#             models.Index(fields=["section","locale","country","is_active","sort_order"]),
#         ]
#         ordering = ["section", "sort_order", "id"]

#     def __str__(self):
#         return f"{self.section} | {self.title}"


# class ClickEvent(models.Model):
#     link = models.ForeignKey(Resource, null=True, blank=True, on_delete=models.SET_NULL, related_name="clicks")
#     locale = models.CharField(max_length=10, blank=True)
#     country = models.CharField(max_length=2, blank=True)
#     referrer = models.TextField(blank=True)
#     user_agent = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         indexes = [
#             models.Index(fields=["created_at"]),
#             models.Index(fields=["link"]),
#             models.Index(fields=["locale","country"]),
#         ]
#         ordering = ["-created_at"]

# class AdSlot(models.Model):
#     position   = models.CharField(max_length=32, choices=[("hero","hero"),("sidebar","sidebar"),("footer","footer")])
#     country    = models.CharField(max_length=2, blank=True)  # "" = global
#     title      = models.CharField(max_length=120, blank=True)
#     image_url  = models.URLField(blank=True)
#     target_url = models.URLField(blank=True)
#     html_embed = models.TextField(blank=True)                # opcional
#     is_active  = models.BooleanField(default=True)
#     sort_order = models.IntegerField(default=0)
#     starts_at  = models.DateTimeField(null=True, blank=True)
#     ends_at    = models.DateTimeField(null=True, blank=True)
#     created_at = models.DateTimeField(default=timezone.now, editable=False)
#     updated_at = models.DateTimeField(default=timezone.now)

#     class Meta:
#         indexes = [
#             models.Index(fields=["position","country","is_active"]),
#         ]
#         ordering = ["position","sort_order","id"]

#     def __str__(self):
#         return f"{self.position} | {self.country or 'GLOBAL'} | {self.title or self.id}"
