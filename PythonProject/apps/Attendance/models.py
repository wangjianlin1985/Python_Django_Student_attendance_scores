from django.db import models
from apps.AttendanceState.models import AttendanceState
from apps.Course.models import Course
from apps.Student.models import Student
from apps.TimeInfo.models import TimeInfo


class Attendance(models.Model):
    attendanceId = models.AutoField(primary_key=True, verbose_name='记录编号')
    studentObj = models.ForeignKey(Student,  db_column='studentObj', on_delete=models.PROTECT, verbose_name='学生')
    courseObj = models.ForeignKey(Course,  db_column='courseObj', on_delete=models.PROTECT, verbose_name='课程')
    timeInfoObj = models.ForeignKey(TimeInfo,  db_column='timeInfoObj', on_delete=models.PROTECT, verbose_name='时间')
    attendanceStateObj = models.ForeignKey(AttendanceState,  db_column='attendanceStateObj', on_delete=models.PROTECT, verbose_name='状态')

    class Meta:
        db_table = 't_Attendance'
        verbose_name = '学生点名信息'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
        attendance = {
            'attendanceId': self.attendanceId,
            'studentObj': self.studentObj.studentName,
            'studentObjPri': self.studentObj.studentNumber,
            'courseObj': self.courseObj.courseName,
            'courseObjPri': self.courseObj.courseNo,
            'timeInfoObj': self.timeInfoObj.timeInfoName,
            'timeInfoObjPri': self.timeInfoObj.timeInfoId,
            'attendanceStateObj': self.attendanceStateObj.stateName,
            'attendanceStateObjPri': self.attendanceStateObj.stateId,
        }
        return attendance

