from django.views.generic import View
from apps.BaseView import BaseView
from django.shortcuts import render
from django.core.paginator import Paginator
from apps.AttendanceState.models import AttendanceState
from django.http import JsonResponse
from django.http import FileResponse
from apps.BaseView import ImageFormatException
from django.conf import settings
import pandas as pd
import os


class FrontAddView(BaseView):  # 前台出勤状态添加
    def primaryKeyExist(self, stateId):  # 判断主键是否存在
        try:
            AttendanceState.objects.get(stateId=stateId)
            return True
        except AttendanceState.DoesNotExist:
            return False

    def get(self,request):

        # 使用模板
        return render(request, 'AttendanceState/attendanceState_frontAdd.html')

    def post(self, request):
        stateId = request.POST.get('attendanceState.stateId') # 判断状态编号是否存在
        if self.primaryKeyExist(stateId):
            return JsonResponse({'success': False, 'message': '状态编号已经存在'})

        attendanceState = AttendanceState() # 新建一个出勤状态对象然后获取参数
        attendanceState.stateId = stateId
        attendanceState.stateName = request.POST.get('attendanceState.stateName')
        attendanceState.save() # 保存出勤状态信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class FrontModifyView(BaseView):  # 前台修改出勤状态
    def get(self, request, stateId):
        context = {'stateId': stateId}
        return render(request, 'AttendanceState/attendanceState_frontModify.html', context)


class FrontListView(BaseView):  # 前台出勤状态查询列表
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        self.getCurrentPage(request)  # 获取当前要显示第几页
        # 下面获取查询参数
        # 然后条件组合查询过滤
        attendanceStates = AttendanceState.objects.all()
        # 对查询结果利用Paginator进行分页
        self.paginator = Paginator(attendanceStates, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        attendanceStates_page = self.paginator.page(self.currentPage)

        # 构造模板需要的参数
        context = {
            'attendanceStates_page': attendanceStates_page,
            'currentPage': self.currentPage,
            'totalPage': self.totalPage,
            'recordNumber': self.recordNumber,
            'startIndex': self.startIndex,
            'pageList': self.pageList,
        }
        # 渲染模板界面
        return render(request, 'AttendanceState/attendanceState_frontquery_result.html', context)


class FrontShowView(View):  # 前台显示出勤状态详情页
    def get(self, request, stateId):
        # 查询需要显示的出勤状态对象
        attendanceState = AttendanceState.objects.get(stateId=stateId)
        context = {
            'attendanceState': attendanceState
        }
        # 渲染模板显示
        return render(request, 'AttendanceState/attendanceState_frontshow.html', context)


class ListAllView(View): # 前台查询所有出勤状态
    def get(self,request):
        attendanceStates = AttendanceState.objects.all()
        attendanceStateList = []
        for attendanceState in attendanceStates:
            attendanceStateObj = {
                'stateId': attendanceState.stateId,
                'stateName': attendanceState.stateName,
            }
            attendanceStateList.append(attendanceStateObj)
        return JsonResponse(attendanceStateList, safe=False)


class UpdateView(BaseView):  # Ajax方式出勤状态更新
    def get(self, request, stateId):
        # GET方式请求查询出勤状态对象并返回出勤状态json格式
        attendanceState = AttendanceState.objects.get(stateId=stateId)
        return JsonResponse(attendanceState.getJsonObj())

    def post(self, request, stateId):
        # POST方式提交出勤状态修改信息更新到数据库
        attendanceState = AttendanceState.objects.get(stateId=stateId)
        attendanceState.stateName = request.POST.get('attendanceState.stateName')
        attendanceState.save()
        return JsonResponse({'success': True, 'message': '保存成功'})

class AddView(BaseView):  # 后台出勤状态添加
    def primaryKeyExist(self, stateId):  # 判断主键是否存在
        try:
            AttendanceState.objects.get(stateId=stateId)
            return True
        except AttendanceState.DoesNotExist:
            return False

    def get(self,request):

        # 渲染显示模板界面
        return render(request, 'AttendanceState/attendanceState_add.html')

    def post(self, request):
        # POST方式处理图书添加业务
        stateId = request.POST.get('attendanceState.stateId') # 判断状态编号是否存在
        if self.primaryKeyExist(stateId):
            return JsonResponse({'success': False, 'message': '状态编号已经存在'})

        attendanceState = AttendanceState() # 新建一个出勤状态对象然后获取参数
        attendanceState.stateId = stateId
        attendanceState.stateName = request.POST.get('attendanceState.stateName')
        attendanceState.save() # 保存出勤状态信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class BackModifyView(BaseView):  # 后台更新出勤状态
    def get(self, request, stateId):
        context = {'stateId': stateId}
        return render(request, 'AttendanceState/attendanceState_modify.html', context)


class ListView(BaseView):  # 后台出勤状态列表
    def get(self, request):
        # 使用模板
        return render(request, 'AttendanceState/attendanceState_query_result.html')

    def post(self, request):
        # 获取当前要显示第几页和每页几条数据
        self.getPageAndSize(request)
        # 收集查询参数
        # 然后条件组合查询过滤
        attendanceStates = AttendanceState.objects.all()
        # 利用Paginator对查询结果集分页
        self.paginator = Paginator(attendanceStates, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        attendanceStates_page = self.paginator.page(self.currentPage)
        # 查询的结果集转换为列表
        attendanceStateList = []
        for attendanceState in attendanceStates_page:
            attendanceState = attendanceState.getJsonObj()
            attendanceStateList.append(attendanceState)
        # 构造模板页面需要的参数
        attendanceState_res = {
            'rows': attendanceStateList,
            'total': self.recordNumber,
        }
        # 渲染模板页面显示
        return JsonResponse(attendanceState_res, json_dumps_params={'ensure_ascii':False})

class DeletesView(BaseView):  # 删除出勤状态信息
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        stateIds = self.getStrParam(request, 'stateIds')
        stateIds = stateIds.split(',')
        count = 0
        try:
            for stateId in stateIds:
                AttendanceState.objects.get(stateId=stateId).delete()
                count = count + 1
            message = '%s条记录删除成功！' % count
            success = True
        except Exception as e:
            message = '数据库外键约束删除失败！'
            success = False
        return JsonResponse({'success': success, 'message': message})


class OutToExcelView(BaseView):  # 导出出勤状态信息到excel并下载
    def get(self, request):
        # 收集查询参数
        # 然后条件组合查询过滤
        attendanceStates = AttendanceState.objects.all()
        #将查询结果集转换成列表
        attendanceStateList = []
        for attendanceState in attendanceStates:
            attendanceState = attendanceState.getJsonObj()
            attendanceStateList.append(attendanceState)
        # 利用pandas实现数据的导出功能
        pf = pd.DataFrame(attendanceStateList)
        # 设置要导入到excel的列
        columns_map = {
            'stateId': '状态编号',
            'stateName': '状态名称',
        }
        pf = pf[columns_map.keys()]
        pf.rename(columns=columns_map, inplace=True)
        # 将空的单元格替换为空字符
        pf.fillna('', inplace=True)
        #设定文件名和导出路径
        filename = 'attendanceStates.xlsx'
        # 这个路径可以在settings中设置也可以直接手动输入
        root_path = settings.MEDIA_ROOT + '/output/'
        file_path = os.path.join(root_path, filename)
        pf.to_excel(file_path, encoding='utf-8', index=False)
        # 将生成的excel文件输出到网页下载
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="attendanceStates.xlsx"'
        return response

