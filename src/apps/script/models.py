# encoding:utf-8
from __future__ import unicode_literals

from django.db import models

import uuid
# Create your models here.
from django.utils.timezone import now


class Script(models.Model):
    """
    脚本对象
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20)
    content = models.TextField(null=True)
    creat_time = models.DateTimeField(null=True, auto_now=now())

    def __unicode__(self):
        return self.name
