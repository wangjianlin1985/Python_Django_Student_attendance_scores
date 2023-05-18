from django.db import models


class TermInfo(models.Model):
    termId = models.AutoField(primary_key=True, verbose_name='学期编号')
    termName = models.CharField(max_length=20, default='', verbose_name='学期名称')

    class Meta:
        db_table = 't_TermInfo'
        verbose_name = '学期信息信息'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
        termInfo = {
            'termId': self.termId,
            'termName': self.termName,
        }
        return termInfo

