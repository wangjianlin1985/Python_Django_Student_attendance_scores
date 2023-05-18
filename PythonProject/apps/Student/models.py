from django.db import models
from apps.ClassInfo.models import ClassInfo


class Student(models.Model):
    studentNumber = models.CharField(max_length=20, default='', primary_key=True, verbose_name='学号')
    studentName = models.CharField(max_length=20, default='', verbose_name='姓名')
    sex = models.CharField(max_length=2, default='', verbose_name='性别')
    classInfoId = models.ForeignKey(ClassInfo,  db_column='classInfoId', on_delete=models.PROTECT, verbose_name='所在班级')
    birthday = models.CharField(max_length=20, default='', verbose_name='出生日期')
    zzmm = models.CharField(max_length=10, default='', verbose_name='政治面貌')
    telephone = models.CharField(max_length=20, default='', verbose_name='联系电话')
    address = models.CharField(max_length=50, default='', verbose_name='家庭地址')
    photoUrl = models.ImageField(upload_to='img', max_length='100', verbose_name='学生照片')

    class Meta:
        db_table = 't_Student'
        verbose_name = '学生信息信息'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
        student = {
            'studentNumber': self.studentNumber,
            'studentName': self.studentName,
            'sex': self.sex,
            'classInfoId': self.classInfoId.className,
            'classInfoIdPri': self.classInfoId.classNo,
            'birthday': self.birthday,
            'zzmm': self.zzmm,
            'telephone': self.telephone,
            'address': self.address,
            'photoUrl': self.photoUrl.url,
        }
        return student

