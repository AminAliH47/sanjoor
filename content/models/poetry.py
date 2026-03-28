from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """Hierarchical literary category for poets, books, and sections."""

    id = models.BigIntegerField(primary_key=True)
    poet = models.ForeignKey('content.Poet', models.DO_NOTHING, blank=True, null=True, related_name='categories')
    text = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True, related_name='children')
    url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cat'
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self) -> str:
        return self.text or str(self.id)


class Poet(models.Model):
    """Poet profile with biography and root category reference."""

    id = models.BigIntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, models.DO_NOTHING, db_column='cat_id', related_name='poets')
    description = models.TextField(blank=True, null=True)

    # Custom fields
    photo = models.ImageField(
        null=True,
        blank=True,
        help_text=_('Portrait of the poet')
    )

    class Meta:
        managed = True
        db_table = 'poet'
        verbose_name = _('poet')
        verbose_name_plural = _('poets')

    def __str__(self) -> str:
        return self.name or str(self.id)


class Poem(models.Model):
    """Poem metadata and location in the category hierarchy."""

    id = models.BigIntegerField(primary_key=True)
    category = models.ForeignKey(Category, models.DO_NOTHING, db_column='cat_id',
                                 blank=True, null=True, related_name='poems')
    title = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'poem'
        verbose_name = _('poem')
        verbose_name_plural = _('poems')

    def __str__(self) -> str:
        return self.title or str(self.id)


class Verse(models.Model):
    """Ordered verse or prose line linked to a poem."""

    id = models.BigIntegerField(primary_key=True)
    poem = models.ForeignKey(Poem, models.DO_NOTHING, related_name='verses')
    order = models.BigIntegerField(db_column='vorder')
    position = models.BigIntegerField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'verse'
        unique_together = (('poem', 'order'),)
        verbose_name = _('verse')
        verbose_name_plural = _('verses')

    def __str__(self) -> str:
        return f'{self.poem_id}:{self.order}'
