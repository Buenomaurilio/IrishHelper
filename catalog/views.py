from django.utils import timezone
from .models import *
from django.shortcuts import redirect
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Resource, ClickEvent
from django.shortcuts import render
from .models import Resource, Section
from django.shortcuts import render
from django.utils import timezone, translation
from django.db import models
from .models import Resource, Section, AdSlot
from django.shortcuts import render
from django.utils import timezone, translation
from django.db import models
from .models import Resource, Section, AdSlot
from django.shortcuts import render
from django.utils import timezone
from django.db import models
from .models import Resource, AdSlot, Section
from django.shortcuts import render
from django.db import models
from django.utils import timezone
from .models import Resource, AdSlot, Section


def irish_helper(request, locale="pt-br", country="IE"):
    # Normaliza valores
    locale = (locale or "pt-br").lower()
    country = (country or "IE").upper()

    now = timezone.now()

    # Base para a maior parte das listas (filtra por idioma)
    base_qs = Resource.objects.filter(
        is_active=True,
        locale=locale,
    ).order_by("sort_order", "id")

    # Anúncios
    ads_qs = AdSlot.objects.filter(
        is_active=True,
    ).filter(
        models.Q(country="") | models.Q(country=country)
    ).filter(
        models.Q(starts_at__isnull=True) | models.Q(starts_at__lte=now),
        models.Q(ends_at__isnull=True)   | models.Q(ends_at__gte=now),
    ).order_by("position", "sort_order", "id")

    ads = {
        "hero":    [a for a in ads_qs if a.position == "hero"],
        "sidebar": [a for a in ads_qs if a.position == "sidebar"],
        "footer":  [a for a in ads_qs if a.position == "footer"],
    }

    # WhatsApp: **NÃO** usa base_qs – só seção + país, porque os links
    # são os mesmos para qualquer idioma.
    whatsapp_groups = Resource.objects.filter(section=Section.WHATSAPP_ACCOMMODATION, is_active=True, country__in=["", country], ).order_by("sort_order", "id")

    # Empregos / Facebook / Apps – podem continuar usando base_qs
    job_sites = base_qs.filter(section=Section.JOB_SITES,country__in=["", country],)

    job_facebook = base_qs.filter(section=Section.JOB_FACEBOOK,country__in=["", country],)

    utility_apps = base_qs.filter(section=Section.UTILITY_APPS,country__in=["", country],)

    ctx = {
        "locale": locale,
        "country": country,

        "useful_links": base_qs.filter(section=Section.USEFUL_LINKS),
        "how_to":       base_qs.filter(section=Section.HOW_TO),
        "phones":       base_qs.filter(section=Section.PHONES,    country__in=["", country]),
        "addresses":    base_qs.filter(section=Section.ADDRESSES, country__in=["", country]),
        "videos":       base_qs.filter(section=Section.VIDEOS),

        # novos blocos
        "whatsapp_groups":      whatsapp_groups,
        "job_sites":            job_sites,
        "job_facebook":         job_facebook,
        "utility_apps":         utility_apps,

        "ads": ads,
    }

    return render(request, "catalog/irish_helper.html", ctx)


# def irish_helper(request, locale="pt-br", country="IE"):
#     # todos os recursos ativos para o idioma atual
#     qs = Resource.objects.filter(
#         is_active=True,
#         locale=locale,
#     ).order_by("sort_order", "id")

#     now = timezone.now()

#     ads = AdSlot.objects.filter(
#         is_active=True
#     ).filter(
#         models.Q(country="") | models.Q(country=country)
#     ).filter(
#         models.Q(starts_at__isnull=True) | models.Q(starts_at__lte=now),
#         models.Q(ends_at__isnull=True)   | models.Q(ends_at__gte=now),
#     ).order_by("position", "sort_order", "id")

#     ctx = {
#         "locale": locale,
#         "country": country,

#         # blocos antigos
#         "useful_links": qs.filter(section=Section.USEFUL_LINKS),
#         "how_to":       qs.filter(section=Section.HOW_TO),
#         "phones":       qs.filter(section=Section.PHONES,    country__in=["", country]),
#         "addresses":    qs.filter(section=Section.ADDRESSES, country__in=["", country]),
#         "videos":       qs.filter(section=Section.VIDEOS),

#         # NOVOS BLOCOS
#         # *** repara que o nome aqui bate com o do template ***
#         "whatsapp_groups": qs.filter(
#             section=Section.WHATSAPP_ACCOMMODATION,
#             country__in=["", country],
#         ),
#         "job_sites": qs.filter(
#             section=Section.JOB_SITES,
#             country__in=["", country],
#         ),
#         "job_facebook": qs.filter(
#             section=Section.JOB_FACEBOOK,
#             country__in=["", country],
#         ),
#         "utility_apps": qs.filter(
#             section=Section.UTILITY_APPS,
#             country__in=["", country],
#         ),

#         "ads": {
#             "hero":    [a for a in ads if a.position == "hero"],
#             "sidebar": [a for a in ads if a.position == "sidebar"],
#             "footer":  [a for a in ads if a.position == "footer"],
#         },
#     }

#     return render(request, "catalog/irish_helper.html", ctx)


@csrf_exempt
@require_POST
def track_click(request, link_id: int):
    try:
        link = Resource.objects.get(pk=link_id, is_active=True)
    except Resource.DoesNotExist:
        raise Http404("Link não encontrado")

    locale = request.POST.get("locale", "")
    country = request.POST.get("country", "")
    ref = request.META.get("HTTP_REFERER", "")
    ua = request.META.get("HTTP_USER_AGENT", "")

    ClickEvent.objects.create(
        link=link,
        locale=locale[:10],
        country=country[:2],
        referrer=ref[:1000],
        user_agent=ua[:1000],
    )
    return JsonResponse({"ok": True})



def home_redirect(request):
    return redirect("irishhelper", locale="pt-br", country="IE")
