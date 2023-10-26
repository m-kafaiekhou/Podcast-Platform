from django.db import models
from django.db.models.aggregates import Count
from random import randint


class BaseManager(models.Manager):
    def get_deleted_list(self):
        return super().get_queryset().filter(is_deleted=True)

    def get_active_list(self):
        return self.get_queryset().filter(is_deleted=False)
    
    def random(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return self.all()[random_index]
    
