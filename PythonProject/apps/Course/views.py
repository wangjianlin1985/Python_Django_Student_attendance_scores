from django.views.generic import View
from apps.BaseView import BaseView
from django.shortcuts import render
from django.core.paginator import Paginator
from apps.Course.models import Course
from django.http import JsonResponse
from django.http import FileResponse
from apps.BaseView import ImageFormatException
from django.conf import settings
import pandas as pd
import os


class FrontAddView(BaseView):  # 前台课程信息添加
    def primaryKeyExist(self, courseNo):  # 判断主键是否存在
        try:
            Course.objects.get(courseNo=courseNo)
            return True
        except Course.DoesNotExist:
            return False

    def get(self,request):

        # 使用模板
        return render(request, 'Course/course_frontAdd.html')

    def post(self, request):
        courseNo = request.POST.get('course.courseNo') # 判断课程编号是否存在
        if self.primaryKeyExist(courseNo):
            return JsonResponse({'success': False, 'message': '课程编号已经存在'})

        course = Course() # 新建一个课程信息对象然后获取参数
        course.courseNo = courseNo
        course.courseName = request.POST.get('course.courseName')
        course.teacherName = request.POST.get('course.teacherName')
        course.courseCount = int(request.POST.get('course.courseCount'))
        course.courseScore = float(request.POST.get('course.courseScore'))
        course.save() # 保存课程信息信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class FrontModifyView(BaseView):  # 前台修改课程信息
    def get(self, request, courseNo):
        context = {'courseNo': courseNo}
        return render(request, 'Course/course_frontModify.html', context)


class FrontListView(BaseView):  # 前台课程信息查询列表
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        self.getCurrentPage(request)  # 获取当前要显示第几页
        # 下面获取查询参数
        courseNo = self.getStrParam(request, 'courseNo')
        courseName = self.getStrParam(request, 'courseName')
        teacherName = self.getStrParam(request, 'teacherName')
        # 然后条件组合查询过滤
        courses = Course.objects.all()
        if courseNo != '':
            courses = courses.filter(courseNo__contains=courseNo)
        if courseName != '':
            courses = courses.filter(courseName__contains=courseName)
        if teacherName != '':
            courses = courses.filter(teacherName__contains=teacherName)
        # 对查询结果利用Paginator进行分页
        self.paginator = Paginator(courses, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        courses_page = self.paginator.page(self.currentPage)

        # 构造模板需要的参数
        context = {
            'courses_page': courses_page,
            'courseNo': courseNo,
            'courseName': courseName,
            'teacherName': teacherName,
            'currentPage': self.currentPage,
            'totalPage': self.totalPage,
            'recordNumber': self.recordNumber,
            'startIndex': self.startIndex,
            'pageList': self.pageList,
        }
        # 渲染模板界面
        return render(request, 'Course/course_frontquery_result.html', context)


class FrontShowView(View):  # 前台显示课程信息详情页
    def get(self, request, courseNo):
        # 查询需要显示的课程信息对象
        course = Course.objects.get(courseNo=courseNo)
        context = {
            'course': course
        }
        # 渲染模板显示
        return render(request, 'Course/course_frontshow.html', context)


class ListAllView(View): # 前台查询所有课程信息
    def get(self,request):
        courses = Course.objects.all()
        courseList = []
        for course in courses:
            courseObj = {
                'courseNo': course.courseNo,
                'courseName': course.courseName,
            }
            courseList.append(courseObj)
        return JsonResponse(courseList, safe=False)


class UpdateView(BaseView):  # Ajax方式课程信息更新
    def get(self, request, courseNo):
        # GET方式请求查询课程信息对象并返回课程信息json格式
        course = Course.objects.get(courseNo=courseNo)
        return JsonResponse(course.getJsonObj())

    def post(self, request, courseNo):
        # POST方式提交课程信息修改信息更新到数据库
        course = Course.objects.get(courseNo=courseNo)
        course.courseName = request.POST.get('course.courseName')
        course.teacherName = request.POST.get('course.teacherName')
        course.courseCount = int(request.POST.get('course.courseCount'))
        course.courseScore = float(request.POST.get('course.courseScore'))
        course.save()
        return JsonResponse({'success': True, 'message': '保存成功'})

class AddView(BaseView):  # 后台课程信息添加
    def primaryKeyExist(self, courseNo):  # 判断主键是否存在
        try:
            Course.objects.get(courseNo=courseNo)
            return True
        except Course.DoesNotExist:
            return False

    def get(self,request):

        # 渲染显示模板界面
        return render(request, 'Course/course_add.html')

    def post(self, request):
        # POST方式处理图书添加业务
        courseNo = request.POST.get('course.courseNo') # 判断课程编号是否存在
        if self.primaryKeyExist(courseNo):
            return JsonResponse({'success': False, 'message': '课程编号已经存在'})

        course = Course() # 新建一个课程信息对象然后获取参数
        course.courseNo = courseNo
        course.courseName = request.POST.get('course.courseName')
        course.teacherName = request.POST.get('course.teacherName')
        course.courseCount = int(request.POST.get('course.courseCount'))
        course.courseScore = float(request.POST.get('course.courseScore'))
        course.save() # 保存课程信息信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class BackModifyView(BaseView):  # 后台更新课程信息
    def get(self, request, courseNo):
        context = {'courseNo': courseNo}
        return render(request, 'Course/course_modify.html', context)


class ListView(BaseView):  # 后台课程信息列表
    def get(self, request):
        # 使用模板
        return render(request, 'Course/course_query_result.html')

    def post(self, request):
        # 获取当前要显示第几页和每页几条数据
        self.getPageAndSize(request)
        # 收集查询参数
        courseNo = self.getStrParam(request, 'courseNo')
        courseName = self.getStrParam(request, 'courseName')
        teacherName = self.getStrParam(request, 'teacherName')
        # 然后条件组合查询过滤
        courses = Course.objects.all()
        if courseNo != '':
            courses = courses.filter(courseNo__contains=courseNo)
        if courseName != '':
            courses = courses.filter(courseName__contains=courseName)
        if teacherName != '':
            courses = courses.filter(teacherName__contains=teacherName)
        # 利用Paginator对查询结果集分页
        self.paginator = Paginator(courses, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        courses_page = self.paginator.page(self.currentPage)
        # 查询的结果集转换为列表
        courseList = []
        for course in courses_page:
            course = course.getJsonObj()
            courseList.append(course)
        # 构造模板页面需要的参数
        course_res = {
            'rows': courseList,
            'total': self.recordNumber,
        }
        # 渲染模板页面显示
        return JsonResponse(course_res, json_dumps_params={'ensure_ascii':False})

class DeletesView(BaseView):  # 删除课程信息信息
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        courseNos = self.getStrParam(request, 'courseNos')
        courseNos = courseNos.split(',')
        count = 0
        try:
            for courseNo in courseNos:
                Course.objects.get(courseNo=courseNo).delete()
                count = count + 1
            message = '%s条记录删除成功！' % count
            success = True
        except Exception as e:
            message = '数据库外键约束删除失败！'
            success = False
        return JsonResponse({'success': success, 'message': message})


class OutToExcelView(BaseView):  # 导出课程信息信息到excel并下载
    def get(self, request):
        # 收集查询参数
        courseNo = self.getStrParam(request, 'courseNo')
        courseName = self.getStrParam(request, 'courseName')
        teacherName = self.getStrParam(request, 'teacherName')
        # 然后条件组合查询过滤
        courses = Course.objects.all()
        if courseNo != '':
            courses = courses.filter(courseNo__contains=courseNo)
        if courseName != '':
            courses = courses.filter(courseName__contains=courseName)
        if teacherName != '':
            courses = courses.filter(teacherName__contains=teacherName)
        #将查询结果集转换成列表
        courseList = []
        for course in courses:
            course = course.getJsonObj()
            courseList.append(course)
        # 利用pandas实现数据的导出功能
        pf = pd.DataFrame(courseList)
        # 设置要导入到excel的列
        columns_map = {
            'courseNo': '课程编号',
            'courseName': '课程名称',
            'teacherName': '任课教师',
            'courseCount': '总课时',
            'courseScore': '总学分',
        }
        pf = pf[columns_map.keys()]
        pf.rename(columns=columns_map, inplace=True)
        # 将空的单元格替换为空字符
        pf.fillna('', inplace=True)
        #设定文件名和导出路径
        filename = 'courses.xlsx'
        # 这个路径可以在settings中设置也可以直接手动输入
        root_path = settings.MEDIA_ROOT + '/output/'
        file_path = os.path.join(root_path, filename)
        pf.to_excel(file_path, encoding='utf-8', index=False)
        # 将生成的excel文件输出到网页下载
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="courses.xlsx"'
        return response

