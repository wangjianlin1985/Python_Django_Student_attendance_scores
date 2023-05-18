from django.db import models


class AttendanceState(models.Model):
    stateId = models.CharField(max_length=20, default='', primary_key=True, verbose_name='状态编号')
    stateName = models.CharField(max_length=20, default='', verbose_name='状态名称')

    class Meta:
        db_table = 't_AttendanceState'
        verbose_name = '出勤状态信息'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
        attendanceState = {
            'stateId': self.stateId,
            'stateName': self.stateName,
        }
        return attendanceState

