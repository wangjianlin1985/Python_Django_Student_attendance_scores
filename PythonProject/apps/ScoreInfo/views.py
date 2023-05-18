from django.views.generic import View
from apps.BaseView import BaseView
from django.shortcuts import render
from django.core.paginator import Paginator
from apps.ScoreInfo.models import ScoreInfo
from apps.Course.models import Course
from apps.Student.models import Student
from apps.TermInfo.models import TermInfo
from django.http import JsonResponse
from django.http import FileResponse
from apps.BaseView import ImageFormatException
from django.conf import settings
import pandas as pd
import os


class FrontAddView(BaseView):  # 前台成绩信息添加
    def get(self,request):
        courses = Course.objects.all()  # 获取所有课程信息
        students = Student.objects.all()  # 获取所有学生信息
        termInfos = TermInfo.objects.all()  # 获取所有学期信息
        context = {
            'courses': courses,
            'students': students,
            'termInfos': termInfos,
        }

        # 使用模板
        return render(request, 'ScoreInfo/scoreInfo_frontAdd.html', context)

    def post(self, request):
        scoreInfo = ScoreInfo() # 新建一个成绩信息对象然后获取参数
        scoreInfo.studentNumber = Student.objects.get(studentNumber=request.POST.get('scoreInfo.studentNumber.studentNumber'))
        scoreInfo.courseNo = Course.objects.get(courseNo=request.POST.get('scoreInfo.courseNo.courseNo'))
        scoreInfo.termId = TermInfo.objects.get(termId=request.POST.get('scoreInfo.termId.termId'))
        scoreInfo.score = float(request.POST.get('scoreInfo.score'))
        scoreInfo.save() # 保存成绩信息信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class FrontModifyView(BaseView):  # 前台修改成绩信息
    def get(self, request, scoreId):
        context = {'scoreId': scoreId}
        return render(request, 'ScoreInfo/scoreInfo_frontModify.html', context)


class FrontListView(BaseView):  # 前台成绩信息查询列表
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        self.getCurrentPage(request)  # 获取当前要显示第几页
        # 下面获取查询参数
        studentNumber_studentNumber = self.getStrParam(request, 'studentNumber.studentNumber')
        courseNo_courseNo = self.getStrParam(request, 'courseNo.courseNo')
        termId_termId = self.getIntParam(request, 'termId.termId')
        # 然后条件组合查询过滤
        scoreInfos = ScoreInfo.objects.all()
        if studentNumber_studentNumber != '':
            scoreInfos = scoreInfos.filter(studentNumber=studentNumber_studentNumber)
        if courseNo_courseNo != '':
            scoreInfos = scoreInfos.filter(courseNo=courseNo_courseNo)
        if termId_termId != '0':
            scoreInfos = scoreInfos.filter(termId=termId_termId)
        # 对查询结果利用Paginator进行分页
        self.paginator = Paginator(scoreInfos, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        scoreInfos_page = self.paginator.page(self.currentPage)

        # 获取所有课程信息
        courses = Course.objects.all()
        # 获取所有学生信息
        students = Student.objects.all()
        # 获取所有学期信息
        termInfos = TermInfo.objects.all()
        # 构造模板需要的参数
        context = {
            'courses': courses,
            'students': students,
            'termInfos': termInfos,
            'scoreInfos_page': scoreInfos_page,
            'studentNumber_studentNumber': studentNumber_studentNumber,
            'courseNo_courseNo': courseNo_courseNo,
            'termId_termId': int(termId_termId),
            'currentPage': self.currentPage,
            'totalPage': self.totalPage,
            'recordNumber': self.recordNumber,
            'startIndex': self.startIndex,
            'pageList': self.pageList,
        }
        # 渲染模板界面
        return render(request, 'ScoreInfo/scoreInfo_frontquery_result.html', context)


class FrontShowView(View):  # 前台显示成绩信息详情页
    def get(self, request, scoreId):
        # 查询需要显示的成绩信息对象
        scoreInfo = ScoreInfo.objects.get(scoreId=scoreId)
        context = {
            'scoreInfo': scoreInfo
        }
        # 渲染模板显示
        return render(request, 'ScoreInfo/scoreInfo_frontshow.html', context)


class ListAllView(View): # 前台查询所有成绩信息
    def get(self,request):
        scoreInfos = ScoreInfo.objects.all()
        scoreInfoList = []
        for scoreInfo in scoreInfos:
            scoreInfoObj = {
                'scoreId': scoreInfo.scoreId,
            }
            scoreInfoList.append(scoreInfoObj)
        return JsonResponse(scoreInfoList, safe=False)


class UpdateView(BaseView):  # Ajax方式成绩信息更新
    def get(self, request, scoreId):
        # GET方式请求查询成绩信息对象并返回成绩信息json格式
        scoreInfo = ScoreInfo.objects.get(scoreId=scoreId)
        return JsonResponse(scoreInfo.getJsonObj())

    def post(self, request, scoreId):
        # POST方式提交成绩信息修改信息更新到数据库
        scoreInfo = ScoreInfo.objects.get(scoreId=scoreId)
        scoreInfo.studentNumber = Student.objects.get(studentNumber=request.POST.get('scoreInfo.studentNumber.studentNumber'))
        scoreInfo.courseNo = Course.objects.get(courseNo=request.POST.get('scoreInfo.courseNo.courseNo'))
        scoreInfo.termId = TermInfo.objects.get(termId=request.POST.get('scoreInfo.termId.termId'))
        scoreInfo.score = float(request.POST.get('scoreInfo.score'))
        scoreInfo.save()
        return JsonResponse({'success': True, 'message': '保存成功'})

class AddView(BaseView):  # 后台成绩信息添加
    def get(self,request):
        courses = Course.objects.all()  # 获取所有课程信息
        students = Student.objects.all()  # 获取所有学生信息
        termInfos = TermInfo.objects.all()  # 获取所有学期信息
        context = {
            'courses': courses,
            'students': students,
            'termInfos': termInfos,
        }

        # 渲染显示模板界面
        return render(request, 'ScoreInfo/scoreInfo_add.html', context)

    def post(self, request):
        # POST方式处理图书添加业务
        scoreInfo = ScoreInfo() # 新建一个成绩信息对象然后获取参数
        scoreInfo.studentNumber = Student.objects.get(studentNumber=request.POST.get('scoreInfo.studentNumber.studentNumber'))
        scoreInfo.courseNo = Course.objects.get(courseNo=request.POST.get('scoreInfo.courseNo.courseNo'))
        scoreInfo.termId = TermInfo.objects.get(termId=request.POST.get('scoreInfo.termId.termId'))
        scoreInfo.score = float(request.POST.get('scoreInfo.score'))
        scoreInfo.save() # 保存成绩信息信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class BackModifyView(BaseView):  # 后台更新成绩信息
    def get(self, request, scoreId):
        context = {'scoreId': scoreId}
        return render(request, 'ScoreInfo/scoreInfo_modify.html', context)


class ListView(BaseView):  # 后台成绩信息列表
    def get(self, request):
        # 使用模板
        return render(request, 'ScoreInfo/scoreInfo_query_result.html')

    def post(self, request):
        # 获取当前要显示第几页和每页几条数据
        self.getPageAndSize(request)
        # 收集查询参数
        studentNumber_studentNumber = self.getStrParam(request, 'studentNumber.studentNumber')
        courseNo_courseNo = self.getStrParam(request, 'courseNo.courseNo')
        termId_termId = self.getIntParam(request, 'termId.termId')
        # 然后条件组合查询过滤
        scoreInfos = ScoreInfo.objects.all()
        if studentNumber_studentNumber != '':
            scoreInfos = scoreInfos.filter(studentNumber=studentNumber_studentNumber)
        if courseNo_courseNo != '':
            scoreInfos = scoreInfos.filter(courseNo=courseNo_courseNo)
        if termId_termId != '0':
            scoreInfos = scoreInfos.filter(termId=termId_termId)
        # 利用Paginator对查询结果集分页
        self.paginator = Paginator(scoreInfos, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        scoreInfos_page = self.paginator.page(self.currentPage)
        # 查询的结果集转换为列表
        scoreInfoList = []
        for scoreInfo in scoreInfos_page:
            scoreInfo = scoreInfo.getJsonObj()
            scoreInfoList.append(scoreInfo)
        # 构造模板页面需要的参数
        scoreInfo_res = {
            'rows': scoreInfoList,
            'total': self.recordNumber,
        }
        # 渲染模板页面显示
        return JsonResponse(scoreInfo_res, json_dumps_params={'ensure_ascii':False})

class DeletesView(BaseView):  # 删除成绩信息信息
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        scoreIds = self.getStrParam(request, 'scoreIds')
        scoreIds = scoreIds.split(',')
        count = 0
        try:
            for scoreId in scoreIds:
                ScoreInfo.objects.get(scoreId=scoreId).delete()
                count = count + 1
            message = '%s条记录删除成功！' % count
            success = True
        except Exception as e:
            message = '数据库外键约束删除失败！'
            success = False
        return JsonResponse({'success': success, 'message': message})


class OutToExcelView(BaseView):  # 导出成绩信息信息到excel并下载
    def get(self, request):
        # 收集查询参数
        studentNumber_studentNumber = self.getStrParam(request, 'studentNumber.studentNumber')
        courseNo_courseNo = self.getStrParam(request, 'courseNo.courseNo')
        termId_termId = self.getIntParam(request, 'termId.termId')
        # 然后条件组合查询过滤
        scoreInfos = ScoreInfo.objects.all()
        if studentNumber_studentNumber != '':
            scoreInfos = scoreInfos.filter(studentNumber=studentNumber_studentNumber)
        if courseNo_courseNo != '':
            scoreInfos = scoreInfos.filter(courseNo=courseNo_courseNo)
        if termId_termId != '0':
            scoreInfos = scoreInfos.filter(termId=termId_termId)
        #将查询结果集转换成列表
        scoreInfoList = []
        for scoreInfo in scoreInfos:
            scoreInfo = scoreInfo.getJsonObj()
            scoreInfoList.append(scoreInfo)
        # 利用pandas实现数据的导出功能
        pf = pd.DataFrame(scoreInfoList)
        # 设置要导入到excel的列
        columns_map = {
            'scoreId': '成绩编号',
            'studentNumber': '学生姓名',
            'courseNo': '课程名称',
            'termId': '所在学期',
            'score': '成绩得分',
        }
        pf = pf[columns_map.keys()]
        pf.rename(columns=columns_map, inplace=True)
        # 将空的单元格替换为空字符
        pf.fillna('', inplace=True)
        #设定文件名和导出路径
        filename = 'scoreInfos.xlsx'
        # 这个路径可以在settings中设置也可以直接手动输入
        root_path = settings.MEDIA_ROOT + '/output/'
        file_path = os.path.join(root_path, filename)
        pf.to_excel(file_path, encoding='utf-8', index=False)
        # 将生成的excel文件输出到网页下载
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="scoreInfos.xlsx"'
        return response

