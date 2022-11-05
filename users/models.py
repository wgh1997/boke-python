from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#         avatar = models.FileField(
#     upload_to='avatar/', default="/avatar/default_avatar.jpg")
        create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
