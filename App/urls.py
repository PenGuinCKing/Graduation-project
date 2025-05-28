"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from App import views
app_name = 'App'
urlpatterns = [
    path('test/',views.test,name='test'),
    path('',views.index,name='index'),
    #左边导航栏
    path('left/',views.public_left,name = 'left'),
    #右边标题栏
    path('header/',views.public_header,name='header'),
    #右边主要内容
    path('main/<int:page>/',views.public_main,name='main'),
    # 最下面的foot
    path('foot/',views.public_foot,name='foot'),

    # 列车时刻表页面
    path('show_train/<int:page>/',views.main_show_train,name='show_train'),
    path('show_train1/<int:page>/<start>/<end>/',views.main_show_train1,name='show_train1'),
    path('show_train2/<int:page>/<start_city>/<end_city>/',views.main_show_train2,name='show_train2'),
    # 购票页面
    path('buy_ticket/<int:id>/',views.buy_ticket,name='buy_ticket'),
    # 按车次查询
    path('main_name_select/',views.main_name_select,name='main_name_select'),
    # 按城市查询
    path('main_city_select/',views.main_city_selcet,name='main_city_select'),
    # 按车站查询
    path('main_station_select/',views.main_station_selcet,name='main_station_select'),
    # 查询订单
    path('main_order_select/<int:page>/',views.main_order_selcet,name='main_order_select'),
    # 查询所有订单
    path('main_order_all/<int:page>/',views.main_order_all,name='main_order_all'),
    # 个人中心
    path('main_user_home/',views.main_user_home,name='main_user_home'),
    # 用户修改个人信息
    path('user_edit/',views.user_edit,name='user_edit'),
    # 联系客服
    path('main_call_admin/',views.main_call_admin,name='main_call_admin'),
    # 聊天区域
    path('talk_area/',views.talk_area,name='talk_area'),
    # 登录|注册
    path('main_login_register/',views.main_login_register,name='main_login_register'),
    # 退出登录
    path('main_logout/',views.main_logout,name='main_logout'),
    # 充值
    path('add_money/',views.add_money,name='add_money'),
    # 修改密码
    path('edit_pswd/',views.edit_pswd,name='edit_pswd'),
    # 敬请期待
    path('wait/',views.wait,name='wait'),


#admin功能
#左边导航栏
    path('admin_left/',views.admin_left,name = 'admin_left'),
    #右边标题栏
    path('admin_header/',views.admin_header,name='admin_header'),
    #右边主要内容
    path('main/<int:page>/',views.admin_main,name='admin_main'),
    # 最下面的foot
    path('admin_foot/',views.admin_foot,name='admin_foot'),


    # 管理员登录
    path('admin_login/',views.admin_login,name='admin_login'),
    # 显示所有车次
    path('admin_main_show_train/<page>/',views.admin_main_show_train,name='admin_main_show_train'),
    # 添加车次
    path('admin_add_ticket/',views.admin_add_ticket,name='admin_add_ticket'),
    # 修改车次
    path('edit_ticket/<int:id>/',views.edit_ticket,name='edit_ticket'),
    # 删除车次
    path('del_ticket/<int:id>/',views.del_ticket,name='del_ticket'),
    # 删除记录
    path('ticket_del_log/<page>/',views.ticket_del_log,name='ticket_del_log'),
    # 恢复车次
    path('restore_ticket/<int:id>/',views.restore_ticket,name='restore_ticket'),
    # 联系客服
    path('admin_call_user/<user>/', views.admin_call_user, name='admin_call_user'),
    # 聊天区域
    path('admin_talk_area/<user>/', views.admin_talk_area, name='admin_talk_area'),
    # 按车次查询
    path('admin_name_select/', views.admin_name_select, name='admin_name_select'),
    # 用户管理
    path('user_manage/', views.user_manage, name='user_manage'),
    # 删除用户
    path('del_user/<int:id>/', views.del_user, name='del_user'),
    # 车站管理
    path('station_manage', views.station_manage, name='station_manage'),

]

