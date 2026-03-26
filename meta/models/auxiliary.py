from django.db import models
from django.utils.translation import gettext_lazy as _


class Favorite(models.Model):
    """Saved poem or verse marker from legacy Ganjoor clients."""

    id = models.BigIntegerField(primary_key=True)
    poem_id = models.BigIntegerField(blank=True, null=True)
    verse_id = models.BigIntegerField(blank=True, null=True)
    pos = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fav'
        verbose_name = _('favorite')
        verbose_name_plural = _('favorites')


class IgnoredCategory(models.Model):
    """Category IDs excluded from update suggestion checks."""

    id = models.BigIntegerField(primary_key=True)
    category = models.ForeignKey('content.Category', models.DO_NOTHING, db_column='cat_id',
                                 blank=True, null=True, related_name='ignored_entries')

    class Meta:
        managed = False
        db_table = 'gil'
        verbose_name = _('ignored category')
        verbose_name_plural = _('ignored categories')


class GanjoorVersion(models.Model):
    """Single-row table that stores Ganjoor database version."""

    id = models.BigIntegerField(primary_key=True)
    current_version = models.BigIntegerField(db_column='curver', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gver'
        verbose_name = _('ganjoor version')
        verbose_name_plural = _('ganjoor versions')
