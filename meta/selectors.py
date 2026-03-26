from django.db.models import QuerySet

from meta.models import GanjoorVersion


def get_ganjoor_versions() -> QuerySet[GanjoorVersion]:
    return GanjoorVersion.objects.order_by('-current_version')
