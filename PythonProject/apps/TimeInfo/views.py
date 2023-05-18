from django.views.generic import View
from apps.BaseView import BaseView
from django.shortcuts import render
from django.core.paginator import Paginator
from apps.TimeInfo.models import TimeInfo
from django.http import JsonResponse
from django.http import FileResponse
from apps.BaseView import ImageFormatException
from django.conf import settings
import pandas as pd
import os


class FrontAddView(BaseView):  # 前台学时信息添加
    def get(self,request):

        # 使用模板
        return render(request, 'TimeInfo/timeInfo_frontAdd.html')

    def post(self, request):
        timeInfo = TimeInfo() # 新建一个学时信息对象然后获取参数
        timeInfo.timeInfoName = request.POST.get('timeInfo.timeInfoName')
        timeInfo.save() # 保存学时信息信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class FrontModifyView(BaseView):  # 前台修改学时信息
    def get(self, request, timeInfoId):
        context = {'timeInfoId': timeInfoId}
        return render(request, 'TimeInfo/timeInfo_frontModify.html', context)


class FrontListView(BaseView):  # 前台学时信息查询列表
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        self.getCurrentPage(request)  # 获取当前要显示第几页
        # 下面获取查询参数
        # 然后条件组合查询过滤
        timeInfos = TimeInfo.objects.all()
        # 对查询结果利用Paginator进行分页
        self.paginator = Paginator(timeInfos, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        timeInfos_page = self.paginator.page(self.currentPage)

        # 构造模板需要的参数
        context = {
            'timeInfos_page': timeInfos_page,
            'currentPage': self.currentPage,
            'totalPage': self.totalPage,
            'recordNumber': self.recordNumber,
            'startIndex': self.startIndex,
            'pageList': self.pageList,
        }
        # 渲染模板界面
        return render(request, 'TimeInfo/timeInfo_frontquery_result.html', context)


class FrontShowView(View):  # 前台显示学时信息详情页
    def get(self, request, timeInfoId):
        # 查询需要显示的学时信息对象
        timeInfo = TimeInfo.objects.get(timeInfoId=timeInfoId)
        context = {
            'timeInfo': timeInfo
        }
        # 渲染模板显示
        return render(request, 'TimeInfo/timeInfo_frontshow.html', context)


class ListAllView(View): # 前台查询所有学时信息
    def get(self,request):
        timeInfos = TimeInfo.objects.all()
        timeInfoList = []
        for timeInfo in timeInfos:
            timeInfoObj = {
                'timeInfoId': timeInfo.timeInfoId,
                'timeInfoName': timeInfo.timeInfoName,
            }
            timeInfoList.append(timeInfoObj)
        return JsonResponse(timeInfoList, safe=False)


class UpdateView(BaseView):  # Ajax方式学时信息更新
    def get(self, request, timeInfoId):
        # GET方式请求查询学时信息对象并返回学时信息json格式
        timeInfo = TimeInfo.objects.get(timeInfoId=timeInfoId)
        return JsonResponse(timeInfo.getJsonObj())

    def post(self, request, timeInfoId):
        # POST方式提交学时信息修改信息更新到数据库
        timeInfo = TimeInfo.objects.get(timeInfoId=timeInfoId)
        timeInfo.timeInfoName = request.POST.get('timeInfo.timeInfoName')
        timeInfo.save()
        return JsonResponse({'success': True, 'message': '保存成功'})

class AddView(BaseView):  # 后台学时信息添加
    def get(self,request):

        # 渲染显示模板界面
        return render(request, 'TimeInfo/timeInfo_add.html')

    def post(self, request):
        # POST方式处理图书添加业务
        timeInfo = TimeInfo() # 新建一个学时信息对象然后获取参数
        timeInfo.timeInfoName = request.POST.get('timeInfo.timeInfoName')
        timeInfo.save() # 保存学时信息信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class BackModifyView(BaseView):  # 后台更新学时信息
    def get(self, request, timeInfoId):
        context = {'timeInfoId': timeInfoId}
        return render(request, 'TimeInfo/timeInfo_modify.html', context)


class ListView(BaseView):  # 后台学时信息列表
    def get(self, request):
        # 使用模板
        return render(request, 'TimeInfo/timeInfo_query_result.html')

    def post(self, request):
        # 获取当前要显示第几页和每页几条数据
        self.getPageAndSize(request)
        # 收集查询参数
        # 然后条件组合查询过滤
        timeInfos = TimeInfo.objects.all()
        # 利用Paginator对查询结果集分页
        self.paginator = Paginator(timeInfos, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        timeInfos_page = self.paginator.page(self.currentPage)
        # 查询的结果集转换为列表
        timeInfoList = []
        for timeInfo in timeInfos_page:
            timeInfo = timeInfo.getJsonObj()
            timeInfoList.append(timeInfo)
        # 构造模板页面需要的参数
        timeInfo_res = {
            'rows': timeInfoList,
            'total': self.recordNumber,
        }
        # 渲染模板页面显示
        return JsonResponse(timeInfo_res, json_dumps_params={'ensure_ascii':False})

class DeletesView(BaseView):  # 删除学时信息信息
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        timeInfoIds = self.getStrParam(request, 'timeInfoIds')
        timeInfoIds = timeInfoIds.split(',')
        count = 0
        try:
            for timeInfoId in timeInfoIds:
                TimeInfo.objects.get(timeInfoId=timeInfoId).delete()
                count = count + 1
            message = '%s条记录删除成功！' % count
            success = True
        except Exception as e:
            message = '数据库外键约束删除失败！'
            success = False
        return JsonResponse({'success': success, 'message': message})


class OutToExcelView(BaseView):  # 导出学时信息信息到excel并下载
    def get(self, request):
        # 收集查询参数
        # 然后条件组合查询过滤
        timeInfos = TimeInfo.objects.all()
        #将查询结果集转换成列表
        timeInfoList = []
        for timeInfo in timeInfos:
            timeInfo = timeInfo.getJsonObj()
            timeInfoList.append(timeInfo)
        # 利用pandas实现数据的导出功能
        pf = pd.DataFrame(timeInfoList)
        # 设置要导入到excel的列
        columns_map = {
            'timeInfoId': '记录编号',
            'timeInfoName': '学时名称',
        }
        pf = pf[columns_map.keys()]
        pf.rename(columns=columns_map, inplace=True)
        # 将空的单元格替换为空字符
        pf.fillna('', inplace=True)
        #设定文件名和导出路径
        filename = 'timeInfos.xlsx'
        # 这个路径可以在settings中设置也可以直接手动输入
        root_path = settings.MEDIA_ROOT + '/output/'
        file_path = os.path.join(root_path, filename)
        pf.to_excel(file_path, encoding='utf-8', index=False)
        # 将生成的excel文件输出到网页下载
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="timeInfos.xlsx"'
        return response

