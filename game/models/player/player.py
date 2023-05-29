from django.db import models
from django.contrib.auth.models import User


class Player(models.Model): #数据表模型都要继承自models.Model
    user = models.OneToOneField(User, on_delete=models.CASCADE) #确立一对一关系
    photo = models.URLField(max_length=256, blank=True) #URLField是Django的自定义超链接
    openid = models.CharField(default="", max_length=50, blank=True, null=True)
    score = models.IntegerField(default=1500)

    def __str__(self): #player在admin后台的表示
        return str(self.user)
