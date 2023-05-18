from django.db import models


class ClassInfo(models.Model):
    classNo = models.CharField(max_length=20, default='', primary_key=True, verbose_name='班级编号')
    className = models.CharField(max_length=20, default='', verbose_name='班级名称')
    banzhuren = models.CharField(max_length=20, default='', verbose_name='班主任姓名')
    beginDate = models.CharField(max_length=20, default='', verbose_name='成立日期')

    class Meta:
        db_table = 't_ClassInfo'
        verbose_name = '班级信息信息'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
        classInfo = {
            'classNo': self.classNo,
            'className': self.className,
            'banzhuren': self.banzhuren,
            'beginDate': self.beginDate,
        }
        return classInfo

