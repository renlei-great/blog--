from django.db import models
from user.models import User
from django.utils import timezone

# from datetime import datetime
import datetime


class Post(models.Model):
    class Meta:
        verbose_name = '博文标题'
        verbose_name_plural = verbose_name
        db_table = 'post'

    title = models.CharField(max_length=200, null=False, verbose_name='标题')
    pubdate = models.DateTimeField(default=timezone.now, null=False, verbose_name='创建时间')
    author = models.ForeignKey(User)

    def __repr__(self):
        return "<post[作者：{}] {} {}>".format(self.author.name, self.id, self.title)

    __str__ = __repr__


class Content(models.Model):
    class Meta:
        verbose_name = '博文内容'
        verbose_name_plural = verbose_name
        db_table = 'content'

    post = models.OneToOneField(Post, verbose_name='标题')
    content = models.TextField(null=False)

    def __repr__(self):
        return "<content {} {}>".format(self.id, self.content[:20])

    __str__ = __repr__










