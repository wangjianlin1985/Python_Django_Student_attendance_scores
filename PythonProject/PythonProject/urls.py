"""PythonProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.views.static import serve #需要导入
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),#这部分很重要
    url(r'^TermInfo/', include('apps.TermInfo.urls', namespace='TermInfo')),  # 学期信息模块
    url(r'^ClassInfo/', include('apps.ClassInfo.urls', namespace='ClassInfo')),  # 班级信息模块
    url(r'^Student/', include('apps.Student.urls', namespace='Student')),  # 学生信息模块
    url(r'^Course/', include('apps.Course.urls', namespace='Course')),  # 课程信息模块
    url(r'^ScoreInfo/', include('apps.ScoreInfo.urls', namespace='ScoreInfo')),  # 成绩信息模块
    url(r'^Attendance/', include('apps.Attendance.urls', namespace='Attendance')),  # 学生点名模块
    url(r'^TimeInfo/', include('apps.TimeInfo.urls', namespace='TimeInfo')),  # 学时信息模块
    url(r'^AttendanceState/', include('apps.AttendanceState.urls', namespace='AttendanceState')),  # 出勤状态模块

    url(r'^', include("apps.Index.urls", namespace="Index")),  # 首页模块

    url(r'^tinymce/', include('tinymce.urls')),
]
