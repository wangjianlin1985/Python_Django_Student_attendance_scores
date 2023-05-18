from django.db import models
from apps.Course.models import Course
from apps.Student.models import Student
from apps.TermInfo.models import TermInfo


class ScoreInfo(models.Model):
    scoreId = models.AutoField(primary_key=True, verbose_name='成绩编号')
    studentNumber = models.ForeignKey(Student,  db_column='studentNumber', on_delete=models.PROTECT, verbose_name='学生姓名')
    courseNo = models.ForeignKey(Course,  db_column='courseNo', on_delete=models.PROTECT, verbose_name='课程名称')
    termId = models.ForeignKey(TermInfo,  db_column='termId', on_delete=models.PROTECT, verbose_name='所在学期')
    score = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='成绩得分')

    class Meta:
        db_table = 't_ScoreInfo'
        verbose_name = '成绩信息信息'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
        scoreInfo = {
            'scoreId': self.scoreId,
            'studentNumber': self.studentNumber.studentName,
            'studentNumberPri': self.studentNumber.studentNumber,
            'courseNo': self.courseNo.courseName,
            'courseNoPri': self.courseNo.courseNo,
            'termId': self.termId.termName,
            'termIdPri': self.termId.termId,
            'score': self.score,
        }
        return scoreInfo

