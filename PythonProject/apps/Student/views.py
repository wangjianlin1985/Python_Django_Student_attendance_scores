from django.views.generic import View
from apps.BaseView import BaseView
from django.shortcuts import render
from django.core.paginator import Paginator
from apps.Student.models import Student
from apps.ClassInfo.models import ClassInfo
from django.http import JsonResponse
from django.http import FileResponse
from apps.BaseView import ImageFormatException
from django.conf import settings
import pandas as pd
import os


class FrontAddView(BaseView):  # 前台学生信息添加
    def primaryKeyExist(self, studentNumber):  # 判断主键是否存在
        try:
            Student.objects.get(studentNumber=studentNumber)
            return True
        except Student.DoesNotExist:
            return False

    def get(self,request):
        classInfos = ClassInfo.objects.all()  # 获取所有班级信息
        context = {
            'classInfos': classInfos,
        }

        # 使用模板
        return render(request, 'Student/student_frontAdd.html', context)

    def post(self, request):
        studentNumber = request.POST.get('student.studentNumber') # 判断学号是否存在
        if self.primaryKeyExist(studentNumber):
            return JsonResponse({'success': False, 'message': '学号已经存在'})

        student = Student() # 新建一个学生信息对象然后获取参数
        student.studentNumber = studentNumber
        student.studentName = request.POST.get('student.studentName')
        student.sex = request.POST.get('student.sex')
        student.classInfoId = ClassInfo.objects.get(classNo=request.POST.get('student.classInfoId.classNo'))
        student.birthday = request.POST.get('student.birthday')
        student.zzmm = request.POST.get('student.zzmm')
        student.telephone = request.POST.get('student.telephone')
        student.address = request.POST.get('student.address')
        try:
            student.photoUrl = self.uploadImageFile(request,'student.photoUrl')
        except ImageFormatException as ife:
            return JsonResponse({'success': False, 'message': ife.error})
        student.save() # 保存学生信息信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class FrontModifyView(BaseView):  # 前台修改学生信息
    def get(self, request, studentNumber):
        context = {'studentNumber': studentNumber}
        return render(request, 'Student/student_frontModify.html', context)


class FrontListView(BaseView):  # 前台学生信息查询列表
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        self.getCurrentPage(request)  # 获取当前要显示第几页
        # 下面获取查询参数
        studentNumber = self.getStrParam(request, 'studentNumber')
        studentName = self.getStrParam(request, 'studentName')
        classInfoId_classNo = self.getStrParam(request, 'classInfoId.classNo')
        birthday = self.getStrParam(request, 'birthday')
        telephone = self.getStrParam(request, 'telephone')
        # 然后条件组合查询过滤
        students = Student.objects.all()
        if studentNumber != '':
            students = students.filter(studentNumber__contains=studentNumber)
        if studentName != '':
            students = students.filter(studentName__contains=studentName)
        if classInfoId_classNo != '':
            students = students.filter(classInfoId=classInfoId_classNo)
        if birthday != '':
            students = students.filter(birthday__contains=birthday)
        if telephone != '':
            students = students.filter(telephone__contains=telephone)
        # 对查询结果利用Paginator进行分页
        self.paginator = Paginator(students, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        students_page = self.paginator.page(self.currentPage)

        # 获取所有班级信息
        classInfos = ClassInfo.objects.all()
        # 构造模板需要的参数
        context = {
            'classInfos': classInfos,
            'students_page': students_page,
            'studentNumber': studentNumber,
            'studentName': studentName,
            'classInfoId_classNo': classInfoId_classNo,
            'birthday': birthday,
            'telephone': telephone,
            'currentPage': self.currentPage,
            'totalPage': self.totalPage,
            'recordNumber': self.recordNumber,
            'startIndex': self.startIndex,
            'pageList': self.pageList,
        }
        # 渲染模板界面
        return render(request, 'Student/student_frontquery_result.html', context)


class FrontShowView(View):  # 前台显示学生信息详情页
    def get(self, request, studentNumber):
        # 查询需要显示的学生信息对象
        student = Student.objects.get(studentNumber=studentNumber)
        context = {
            'student': student
        }
        # 渲染模板显示
        return render(request, 'Student/student_frontshow.html', context)


class ListAllView(View): # 前台查询所有学生信息
    def get(self,request):
        students = Student.objects.all()
        studentList = []
        for student in students:
            studentObj = {
                'studentNumber': student.studentNumber,
                'studentName': student.studentName,
            }
            studentList.append(studentObj)
        return JsonResponse(studentList, safe=False)


class UpdateView(BaseView):  # Ajax方式学生信息更新
    def get(self, request, studentNumber):
        # GET方式请求查询学生信息对象并返回学生信息json格式
        student = Student.objects.get(studentNumber=studentNumber)
        return JsonResponse(student.getJsonObj())

    def post(self, request, studentNumber):
        # POST方式提交学生信息修改信息更新到数据库
        student = Student.objects.get(studentNumber=studentNumber)
        student.studentName = request.POST.get('student.studentName')
        student.sex = request.POST.get('student.sex')
        student.classInfoId = ClassInfo.objects.get(classNo=request.POST.get('student.classInfoId.classNo'))
        student.birthday = request.POST.get('student.birthday')
        student.zzmm = request.POST.get('student.zzmm')
        student.telephone = request.POST.get('student.telephone')
        student.address = request.POST.get('student.address')
        try:
            photoUrlName = self.uploadImageFile(request, 'student.photoUrl')
        except ImageFormatException as ife:
            return JsonResponse({'success': False, 'message': ife.error})
        if photoUrlName != 'img/NoImage.jpg':
            student.photoUrl = photoUrlName
        student.save()
        return JsonResponse({'success': True, 'message': '保存成功'})

class AddView(BaseView):  # 后台学生信息添加
    def primaryKeyExist(self, studentNumber):  # 判断主键是否存在
        try:
            Student.objects.get(studentNumber=studentNumber)
            return True
        except Student.DoesNotExist:
            return False

    def get(self,request):
        classInfos = ClassInfo.objects.all()  # 获取所有班级信息
        context = {
            'classInfos': classInfos,
        }

        # 渲染显示模板界面
        return render(request, 'Student/student_add.html', context)

    def post(self, request):
        # POST方式处理图书添加业务
        studentNumber = request.POST.get('student.studentNumber') # 判断学号是否存在
        if self.primaryKeyExist(studentNumber):
            return JsonResponse({'success': False, 'message': '学号已经存在'})

        student = Student() # 新建一个学生信息对象然后获取参数
        student.studentNumber = studentNumber
        student.studentName = request.POST.get('student.studentName')
        student.sex = request.POST.get('student.sex')
        student.classInfoId = ClassInfo.objects.get(classNo=request.POST.get('student.classInfoId.classNo'))
        student.birthday = request.POST.get('student.birthday')
        student.zzmm = request.POST.get('student.zzmm')
        student.telephone = request.POST.get('student.telephone')
        student.address = request.POST.get('student.address')
        try:
            student.photoUrl = self.uploadImageFile(request,'student.photoUrl')
        except ImageFormatException as ife:
            return JsonResponse({'success': False, 'message': ife.error})
        student.save() # 保存学生信息信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class BackModifyView(BaseView):  # 后台更新学生信息
    def get(self, request, studentNumber):
        context = {'studentNumber': studentNumber}
        return render(request, 'Student/student_modify.html', context)


class ListView(BaseView):  # 后台学生信息列表
    def get(self, request):
        # 使用模板
        return render(request, 'Student/student_query_result.html')

    def post(self, request):
        # 获取当前要显示第几页和每页几条数据
        self.getPageAndSize(request)
        # 收集查询参数
        studentNumber = self.getStrParam(request, 'studentNumber')
        studentName = self.getStrParam(request, 'studentName')
        classInfoId_classNo = self.getStrParam(request, 'classInfoId.classNo')
        birthday = self.getStrParam(request, 'birthday')
        telephone = self.getStrParam(request, 'telephone')
        # 然后条件组合查询过滤
        students = Student.objects.all()
        if studentNumber != '':
            students = students.filter(studentNumber__contains=studentNumber)
        if studentName != '':
            students = students.filter(studentName__contains=studentName)
        if classInfoId_classNo != '':
            students = students.filter(classInfoId=classInfoId_classNo)
        if birthday != '':
            students = students.filter(birthday__contains=birthday)
        if telephone != '':
            students = students.filter(telephone__contains=telephone)
        # 利用Paginator对查询结果集分页
        self.paginator = Paginator(students, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        students_page = self.paginator.page(self.currentPage)
        # 查询的结果集转换为列表
        studentList = []
        for student in students_page:
            student = student.getJsonObj()
            studentList.append(student)
        # 构造模板页面需要的参数
        student_res = {
            'rows': studentList,
            'total': self.recordNumber,
        }
        # 渲染模板页面显示
        return JsonResponse(student_res, json_dumps_params={'ensure_ascii':False})

class DeletesView(BaseView):  # 删除学生信息信息
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        studentNumbers = self.getStrParam(request, 'studentNumbers')
        studentNumbers = studentNumbers.split(',')
        count = 0
        try:
            for studentNumber in studentNumbers:
                Student.objects.get(studentNumber=studentNumber).delete()
                count = count + 1
            message = '%s条记录删除成功！' % count
            success = True
        except Exception as e:
            message = '数据库外键约束删除失败！'
            success = False
        return JsonResponse({'success': success, 'message': message})


class OutToExcelView(BaseView):  # 导出学生信息信息到excel并下载
    def get(self, request):
        # 收集查询参数
        studentNumber = self.getStrParam(request, 'studentNumber')
        studentName = self.getStrParam(request, 'studentName')
        classInfoId_classNo = self.getStrParam(request, 'classInfoId.classNo')
        birthday = self.getStrParam(request, 'birthday')
        telephone = self.getStrParam(request, 'telephone')
        # 然后条件组合查询过滤
        students = Student.objects.all()
        if studentNumber != '':
            students = students.filter(studentNumber__contains=studentNumber)
        if studentName != '':
            students = students.filter(studentName__contains=studentName)
        if classInfoId_classNo != '':
            students = students.filter(classInfoId=classInfoId_classNo)
        if birthday != '':
            students = students.filter(birthday__contains=birthday)
        if telephone != '':
            students = students.filter(telephone__contains=telephone)
        #将查询结果集转换成列表
        studentList = []
        for student in students:
            student = student.getJsonObj()
            studentList.append(student)
        # 利用pandas实现数据的导出功能
        pf = pd.DataFrame(studentList)
        # 设置要导入到excel的列
        columns_map = {
            'studentNumber': '学号',
            'studentName': '姓名',
            'sex': '性别',
            'classInfoId': '所在班级',
            'birthday': '出生日期',
            'zzmm': '政治面貌',
            'telephone': '联系电话',
        }
        pf = pf[columns_map.keys()]
        pf.rename(columns=columns_map, inplace=True)
        # 将空的单元格替换为空字符
        pf.fillna('', inplace=True)
        #设定文件名和导出路径
        filename = 'students.xlsx'
        # 这个路径可以在settings中设置也可以直接手动输入
        root_path = settings.MEDIA_ROOT + '/output/'
        file_path = os.path.join(root_path, filename)
        pf.to_excel(file_path, encoding='utf-8', index=False)
        # 将生成的excel文件输出到网页下载
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="students.xlsx"'
        return response

