from django.db import models


class BaseManager(models.Manager):
    def get_deleted_list(self):
        return super().get_queryset().filter(is_deleted=True)

    def get_active_list(self):
        return self.get_queryset().filter(is_deleted=False)
