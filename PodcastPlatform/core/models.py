from django.db import models
from .managers import BaseManager
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    class Meta:
        abstract = True

    objects = BaseManager()

    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('Created at'))

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
        verbose_name=_('Deleted datetime'),
        help_text=_('This is deleted datetime')
    )

    restored_at = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
        verbose_name=_('Restored Datetime'),
        help_text=_('This is Restored Datetime')
    )

    is_deleted = models.BooleanField(
        default=False,
        editable=False,
        db_index=True,  # creates an index on the col to improve query speed
        verbose_name=_('Deleted status'),
        help_text=_('This is deleted status')
    )

    def logical_delete(self):
        self.deleted_at = timezone.now()
        self.is_deleted = True
        self.save()

    def restore(self):
        self.restored_at = timezone.now()
        self.is_deleted = False
        self.save()
