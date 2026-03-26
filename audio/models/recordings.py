from django.db import models
from django.utils.translation import gettext_lazy as _


class PoemSound(models.Model):
    """Audio metadata attached to a poem."""

    id = models.BigIntegerField(primary_key=True)
    poem = models.ForeignKey('content.Poem', models.DO_NOTHING, related_name='sounds')
    filepath = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    download_url = models.TextField(db_column='dnldurl', blank=True, null=True)
    is_direct = models.BigIntegerField(db_column='isdirect', blank=True, null=True)
    sync_guid = models.TextField(db_column='syncguid', blank=True, null=True)
    file_checksum = models.TextField(db_column='fchksum', blank=True, null=True)
    is_uploaded = models.BigIntegerField(db_column='isuploaded', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'poemsnd'
        verbose_name = _('poem sound')
        verbose_name_plural = _('poem sounds')


class SoundSync(models.Model):
    """Verse timing markers for an audio file."""

    id = models.BigIntegerField(primary_key=True)
    poem = models.ForeignKey('content.Poem', models.DO_NOTHING, blank=True, null=True, related_name='sound_syncs')
    sound = models.ForeignKey(PoemSound, models.DO_NOTHING, db_column='snd_id',
                              blank=True, null=True, related_name='sync_points')
    verse_order = models.BigIntegerField(blank=True, null=True)
    milisec = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sndsync'
        verbose_name = _('sound sync point')
        verbose_name_plural = _('sound sync points')
