from django.db.models import QuerySet

from audio.models import PoemSound, SoundSync


def get_poem_sounds(poem_id: int) -> QuerySet[PoemSound]:
    return PoemSound.objects.filter(poem_id=poem_id).order_by('id')


def get_sound_sync_points(sound_id: int) -> QuerySet[SoundSync]:
    return SoundSync.objects.filter(sound_id=sound_id).order_by('verse_order')
