from django.db import models


class Course(models.Model):
    courseNo = models.CharField(max_length=20, default='', primary_key=True, verbose_name='课程编号')
    courseName = models.CharField(max_length=20, default='', verbose_name='课程名称')
    teacherName = models.CharField(max_length=20, default='', verbose_name='任课教师')
    courseCount = models.IntegerField(default=0,verbose_name='总课时')
    courseScore = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总学分')

    class Meta:
        db_table = 't_Course'
        verbose_name = '课程信息信息'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
        course = {
            'courseNo': self.courseNo,
            'courseName': self.courseName,
            'teacherName': self.teacherName,
            'courseCount': self.courseCount,
            'courseScore': self.courseScore,
        }
        return course

