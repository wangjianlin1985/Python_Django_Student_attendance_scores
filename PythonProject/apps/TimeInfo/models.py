from django.db import models


class TimeInfo(models.Model):
    timeInfoId = models.AutoField(primary_key=True, verbose_name='记录编号')
    timeInfoName = models.CharField(max_length=20, default='', verbose_name='学时名称')

    class Meta:
        db_table = 't_TimeInfo'
        verbose_name = '学时信息信息'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
        timeInfo = {
            'timeInfoId': self.timeInfoId,
            'timeInfoName': self.timeInfoName,
        }
        return timeInfo

