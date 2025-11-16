# catalog/management/commands/translate_resources.py

from django.core.management.base import BaseCommand
from catalog.models import Resource

# dicionários de tradução baseados no TITLE em pt-br
PT_TO_EN = {
    "Agendar IRP (GNIB) — Dublin": {
        "title": "Book IRP (GNIB) — Dublin",
        "description": "Book your first issuance or renewal of the Irish Residence Permit.",
    },
    "Solicitar PPS — MyWelfare": {
        "title": "Apply for PPS — MyWelfare",
        "description": "Official page to apply for your PPS Number.",
    },
    "Leap Card (Adult/Student)": {
        "title": "Leap Card (Adult/Student)",
        "description": "Purchase, top up and information about the TFI Leap Card.",
    },
    "NDLS — Carteira de Motorista": {
        "title": "NDLS — Driving Licence",
        "description": "Information about learner permits and full licences.",
    },
    "Como solicitar PPS (passo a passo)": {
        "title": "How to apply for PPS (step by step)",
        "description": (
            "1) Create an account on MyWelfare.\n"
            "2) Fill in the PPS application.\n"
            "3) Attach documents (ID, proof of address and reason).\n"
            "4) Follow the response by e-mail."
        ),
    },
    "Emergência — 112 / 999": {
        "title": "Emergency — 112 / 999",
        "description": "Police, fire brigade and ambulance.",
    },
    "IRP (GNIB) — Dublin (Burgh Quay)": {
        "title": "IRP (GNIB) — Dublin (Burgh Quay)",
        # address fica igual, então não precisamos mexer na description
    },
    "PPS: tutorial prático": {
        "title": "PPS: practical tutorial",
        "description": "Video explaining how to apply for the PPS.",
    },
}

PT_TO_ES = {
    "Agendar IRP (GNIB) — Dublin": {
        "title": "Reservar IRP (GNIB) — Dublín",
        "description": "Reserva tu primera emisión o renovación del Irish Residence Permit.",
    },
    "Solicitar PPS — MyWelfare": {
        "title": "Solicitar PPS — MyWelfare",
        "description": "Página oficial para solicitar tu PPS Number.",
    },
    "Leap Card (Adult/Student)": {
        "title": "Leap Card (Adult/Student)",
        "description": "Compra, recarga e información sobre la TFI Leap Card.",
    },
    "NDLS — Carteira de Motorista": {
        "title": "NDLS — Licencia de Conducir",
        "description": (
            "Información sobre learner permit y full licence."
        ),
    },
    "Como solicitar PPS (passo a passo)": {
        "title": "Cómo solicitar el PPS (paso a paso)",
        "description": (
            "1) Crea una cuenta en MyWelfare.\n"
            "2) Rellena la solicitud de PPS.\n"
            "3) Adjunta documentos (identidad, comprobante de domicilio y motivo).\n"
            "4) Sigue la respuesta por correo electrónico."
        ),
    },
    "Emergência — 112 / 999": {
        "title": "Emergencia — 112 / 999",
        "description": "Policía, bomberos y ambulancia.",
    },
    "IRP (GNIB) — Dublin (Burgh Quay)": {
        "title": "IRP (GNIB) — Dublín (Burgh Quay)",
    },
    "PPS: tutorial prático": {
        "title": "PPS: tutorial práctico",
        "description": "Video que explica cómo solicitar el PPS.",
    },
}


class Command(BaseCommand):
    help = "Gera versões traduzidas (en, es) dos Resources em pt-br"

    def handle(self, *args, **options):
        base_qs = Resource.objects.filter(locale="pt-br").order_by("id")
        if not base_qs.exists():
            self.stdout.write(self.style.ERROR("Nenhum Resource com locale='pt-br' encontrado."))
            return

        self.stdout.write(self.style.WARNING(f"Encontrados {base_qs.count()} registros em pt-br."))

        created = 0
        skipped = 0

        for r in base_qs:
            for lang, mapping in (("en", PT_TO_EN), ("es", PT_TO_ES)):
                data = mapping.get(r.title)

                if Resource.objects.filter(locale=lang, section=r.section, sort_order=r.sort_order).exists():
                    skipped += 1
                    continue

                # se não tiver tradução explícita, copia o texto em pt-br mesmo
                new_title = data["title"] if data and "title" in data else r.title
                new_desc = data.get("description") if data and "description" in data else r.description

                Resource.objects.create(
                    section=r.section,
                    locale=lang,
                    country=r.country,  # por enquanto mantemos igual
                    title=new_title,
                    description=new_desc,
                    url=r.url,
                    phone=r.phone,
                    address=r.address,
                    is_official=r.is_official,
                    is_active=r.is_active,
                    sort_order=r.sort_order,
                )
                created += 1
                self.stdout.write(f"[{lang}] criado: {new_title}")

        self.stdout.write(self.style.SUCCESS(f"Concluído. Criados: {created}, pulados (já existiam): {skipped}."))
