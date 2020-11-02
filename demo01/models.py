from django.db import models


# Create your models here.


class User(models.Model):
    gender_choice = (
        (0, '男'),
        (1, '女'),
        (2, '保密'),
    )
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    gender = models.SmallIntegerField(choices=gender_choice, default=0)
    pic = models.ImageField(upload_to='pic/', default='pic/pic1.jpg')

    class Meta:
        db_table = 'bz_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
