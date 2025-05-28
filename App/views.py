from django.contrib.auth.hashers import make_password  # 使用 Django 内置的密码哈希工具

import hashlib
import random
import re
import time
import webbrowser

from django.contrib.messages import get_messages
from django.core.mail import message
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
# from App.models import User
from django.template import RequestContext

from App.models import User, Session, Tickets, Order, Station, Chat


def index(request):
    return render(request, 'index.html')


def public_left(request):
    return render(request, 'public_left.html')


def public_header(request):
    data = Session.objects.first()
    if data==None:
        username = '未登录'
        return render(request,'public_header.html',locals())
    elif data.is_login=='True':
        username = data.username
        # print(username)
        return render(request,'public_header.html',locals())


def public_main(request,page=1):

    return main_show_train(request,page=page)

def admin_main(request,page=1):

    return admin_main_show_train(request,page=page)    #加载首页也调用一次


def public_foot(request):
    return render(request, 'public_foot.html')


def main_show_train(request,page=1):

    tickets = Tickets.objects.filter(status=1).order_by('start_time')
    # 产生分页对象，一个对象5个tickets数据
    paginator=Paginator(tickets,7)
    pager = paginator.page(page)
    return render(request, 'main_show_train.html', locals())

def admin_main_show_train(request,page=1):

    tickets = Tickets.objects.filter(status=1).order_by('start_time')
    # 产生分页对象，一个对象5个tickets数据
    paginator=Paginator(tickets,7)
    pager = paginator.page(page)
    return render(request, 'admin_main_show_train.html', locals())


def main_name_select(request,page=1):
    if request.method=='POST':
        tname = request.POST.get('t_name')
        # print(t_name)
        if tname=='':
            status=1
            tip='请输入车次！'
        else:
            tickets = Tickets.objects.filter(t_name=tname)
            print(tickets)
            if not tickets:
                status=1
                tip='未找到该次列车！'
            else:
                paginator = Paginator(tickets, 7)
                print(tickets)
                pager = paginator.page(page)
                return render(request,'main_show_train.html',locals())

    return render(request, 'main_name_select.html', locals())

def admin_name_select(request,page=1):
    if request.method=='POST':
        tname = request.POST.get('t_name')
        # print(t_name)
        if tname=='':
            status=1
            tip='请输入车次！'
        else:
            tickets = Tickets.objects.filter(t_name=tname)
            print(tickets)
            if not tickets:
                status=1
                tip='未找到该次列车！'
            else:
                paginator = Paginator(tickets, 7)
                print(tickets)
                pager = paginator.page(page)
                return render(request,'admin_main_show_train.html',locals())

    return render(request, 'admin_name_select.html', locals())


def main_city_selcet(request):

    if request.method == 'POST':
        start = request.POST.get('start')
        end = request.POST.get('end')
        if start == '' or end == '':
            status = 1
            tip = '请输入完整信息！'
        else:
            starts = Station.objects.filter(city=start)
            ends = Station.objects.filter(city=end)
            tickets = []
            for start_ in starts:
                for end_ in ends:
                    tickets += Tickets.objects.filter(start_station__contains=start_.station).filter(end_station__contains=end_.station)

            tickets = list(set(tickets))
            # print(tickets)
            if not tickets:
                status = 1
                tip = '没有符合的车次！'
            else:
                return main_show_train2(request,page=1, start_city=start, end_city=end)
    return render(request, 'main_city_select.html', locals())
def main_show_train2(request, page=1,**kwargs):
    start_city = kwargs['start_city']
    end_city = kwargs['end_city']
    # print(start)
    starts = Station.objects.filter(city=start_city)
    ends = Station.objects.filter(city=end_city)
    # print(starts)
    tickets=[]
    for start in starts:
        for end in ends:
            tickets += Tickets.objects.filter(start_station__contains=start.station).filter(end_station__contains=end.station).filter(status=1)

    tickets=list(set(tickets))  #去重
    paginator = Paginator(tickets, 7)
    pager = paginator.page(page)
    # print(tickets)
    return render(request, 'main_show_train2.html', locals())


def main_station_selcet(request,page=1):
    if request.method=='POST':
        start = request.POST.get('start')
        end = request.POST.get('end')
        if start=='' or end =='':
            status=1
            tip='请输入起始站或终点站！'
        else:
            tickets = Tickets.objects.filter(start_station__contains=start).filter(end_station__contains=end)
            # print(tickets)
            if not tickets:
                status=1
                tip='没有符合的车次！'
            else:
                paginator = Paginator(tickets, 7)
                pager = paginator.page(page)
                return main_show_train1(request,page,start=start,end=end)
    return render(request, 'main_station_select.html', locals())

def main_show_train1(request, page=1,**kwargs):
    start = kwargs['start']
    end = kwargs['end']
    # print(start)
    tickets = Tickets.objects.filter(start_station__contains=start).filter(end_station__contains=end).filter(status=1)
    paginator = Paginator(tickets, 7)
    pager = paginator.page(page)
    print(tickets)
    return render(request, 'main_show_train1.html', locals())


def main_order_selcet(request,page=1):
    user = Session.objects.first()
    if not user:
        return render(request,'main_login_register.html')
    else:
        username=user.username
        # print(username)
        name = User.objects.filter(username=username)[0].name
        orders = Order.objects.filter(username=username)[0:2]
        if not orders:
            print('暂无订单信息！')
            tip='暂无订单信息！'
            return render(request,'main_order_select.html',locals())
        else:
            tip='全部订单'
            carid = User.objects.filter(username=username)[0].carid
            # print(carid)
            carid=carid[0:10]+'****'+carid[14:]
            # print(carid)
            return render(request, 'main_order_select.html', locals())


def main_user_home(request):
    login_user = Session.objects.first()
    if not login_user:
        return render(request,'main_login_register.html')
    else:
        user = User.objects.filter(username=login_user.username)[0]
        # print(user.username)
        carid = user.carid
        # print(carid)
        carid = carid[0:10] + '****' + carid[14:]
        if carid=='****':
            carid=''
        name = user.name
        # name=None
        if not name:
            name='未知'
        elif len(name)==2:
            name = name[0]+'*'
        elif len(name)==3:
            name = name[0]+'*'+name[2]
        elif len(name)==4:
            name = name[0]+'**'+name[3]

        # print(name)

        sex = user.sex
        if not sex:
            sex='保密'
        money =user.money
        if not money:
            money=0.0
        return render(request, 'main_user_home.html', locals())


def main_call_admin(request):
    if request.method=='POST':
        sendtext=request.POST.get('text')
        # print(text)
        username=Session.objects.first().username
        chat = Chat(sendfrom=username,sendto='admin',text=sendtext)
        if not sendtext:
            status=1
            tip='请输入内容！'
        else:
            chat.save()
    return render(request, 'main_call_admin.html', locals())

def talk_area(request):
    username = Session.objects.first().username
    chat=Chat.objects.filter(Q(sendfrom=username)|Q(sendto=username))
    return render(request,'talk_area.html',locals())

def main_login_register(request):

    md5 = hashlib.md5()
    if request.method == 'POST':
        if request.POST.get('login')=='>  登录  <':

            # 获取登录信息
            username = request.POST.get('username')
            password = request.POST.get('password')

            # 登录验证
            if username=='':
                status = 1
                tip = '请输入用户名！'
            elif password=='':
                status=1
                tip = '请输入密码！'

            if username!='' and password!='':
                # exists = User.objects.filter(username=username)
                md5.update(password.encode('utf8'))
                user = User.objects.filter(username=username)
                # print(user)
                # print(user[0].password)

                if re.fullmatch(r'[a-zA-Z0-9]{6,16}', username) == None:
                    status = 1
                    tip = '用户名格式错误！'
                elif re.fullmatch(r'[a-zA-Z0-9]{6,16}', password) == None:
                    status = 1
                    tip = '密码格式错误！'

                # 判断用户是否存在
                if not user:
                    status=1
                    tip='用户名不存在！'
                else:
                    # 如果存在
                    upwd=user[0].password
                    if md5.hexdigest()!= upwd:
                        status=1
                        tip='密码错误！'
                    elif md5.hexdigest()==upwd:
                        print('登陆成功')
                        session = Session(is_login='True',username=username)
                        session.save()
                        # return render(request,'main_show_train.html',locals(),)
                        return main_show_train(request,page=1)

        if request.POST.get('register')=='>  注册  <':

            # 获取注册信息
            rusername = request.POST.get('rusername')
            rpassword = request.POST.get('rpassword')
            md5.update(rpassword.encode('utf8'))
            repassword = request.POST.get('repassword')
            email = request.POST.get('email')
            # print(email)
            # 查看数据库中是否有重名用户
            userdata = User.objects.filter(username=rusername)

            # 注册验证
            if rusername == '':
                rstatus = 1
                rtip = '请输入用户名！'
            elif re.fullmatch(r'[a-zA-Z0-9]{6,16}', rusername) == None:
                rstatus = 1
                rtip = '用户名格式错误！'
            elif rpassword == '':
                rstatus = 1
                rtip = '请输入密码！'
            elif re.fullmatch(r'[a-zA-Z0-9]{6,16}', rpassword) == None:
                rstatus = 1
                rtip = '密码格式错误！'
            elif repassword != rpassword:
                rstatus = 1
                rtip = '两次输入的密码不一致！'
            elif email == '':
                rstatus = 1
                rtip = '请输入邮箱！'
            elif re.fullmatch(r'^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$',
                              email) == None:
                rstatus = 1
                rtip = '邮箱格式错误！'
            elif userdata :
                rstatus = 1
                rtip = '该用户已存在！'
            else:
                hashed_password = make_password(rpassword)

                user = User(
                    username=rusername,
                    password=md5.hexdigest(),
                    email=email,
                    money = 0.00
                )
                user.save()
                rsuccess=1
                rtip='注册成功！'

    return render(request, 'main_login_register.html', locals())


def main_logout(request):
    try:
        session = Session.objects.first()
        if session:
            session.delete()
            username='未登录'
    except Exception as e:
        print(e)
    return render(request,'public_header.html',locals())


def test(request):

    return HttpResponse('测试页面')



# 创建一个车票类
# class Ticket(object):
#     def __init__(self,):


def admin_add_ticket(request):
    if request.method=='POST':
        t_name          = request.POST.get('t_name')
        start_station   = request.POST.get('start_station')
        end_station     = request.POST.get('end_station')
        start_time      = request.POST.get('start_time')
        end_time        = request.POST.get('end_time')
        time            = request.POST.get('time')
        c_seat          = request.POST.get('c_seat')
        c_price         = request.POST.get('c_price')
        b_seat          = request.POST.get('b_seat')
        b_price         = request.POST.get('b_price')
        a_seat          = request.POST.get('a_seat')
        a_price         = request.POST.get('a_price')

        if t_name== '' :
            status=1
            tip='请输入车次！'
        elif start_station== '':
            status = 1
            tip = '请输入始发站！'
        elif end_station== '':
            status = 1
            tip = '请输入终点站！'
        elif start_time== '':
            status = 1
            tip = '请输入发车时间！'
        elif end_time== '':
            status = 1
            tip = '请输入到站时间！'
        elif time== '':
            status = 1
            tip = '请输入总时长！'
        elif c_seat== '':
            status = 1
            tip = '请输入二等座数量！'
        elif c_price== '':
            status = 1
            tip = '请输入二等座价格！'
        elif b_seat== '':
            status = 1
            tip = '请输入一等座数量！'
        elif b_price== '':
            status = 1
            tip = '请输入一等座价格！'
        elif a_seat== '':
            status = 1
            tip = '请输入商务座数量！'
        elif a_price== '':
            status = 1
            tip = '请输入商务座价格！'
        elif check_price(c_price,b_price,a_price):
            status=1
            tip='价格错误！'
        else:
            print('---------------')
            count = Tickets.objects.filter(t_name=t_name).count()
            if count==0:
                print('可以插入信息！')
                ticket = Tickets(
                    t_name=t_name,
                    start_station=start_station,
                    end_station=end_station,
                    start_time=start_time,
                    end_time=end_time,
                    time=time,
                    c_seat=c_seat,
                    c_price=float(c_price),
                    b_seat=b_seat,
                    b_price=float(b_price),
                    a_seat=a_seat,
                    a_price=float(a_price),
                    status=1
                )
                ticket.save()
                print('插入成功')
                status = 1
                tip = '插入成功！'

            else:
                print('不可以插入')
                status = 1
                tip = '已存在该车次！'
    return render(request,'admin_add_ticket.html',locals())


def buy_ticket(request,id):
    # 获得车次信息
    ticket = Tickets.objects.get(id=id)
    # 获取用户信息
    session_user = Session.objects.first()
    # print(session_user)
    if not session_user:
       return render(request,'main_login_register.html')
    else:
        username = session_user.username
        user = User.objects.get(username=username)
        carid = user.carid
        name = user.name
        if carid==None:
            carid=''
        if name == None:
            name=''
        if request.method=='POST':
            seat=request.POST.get('sel')
            go_day = request.POST.get('go_day')
            # 生成订单编号
            oid = 'T'+time.strftime('%Y%m%d%H%M%S')+str(user.id)
            # 生成座位号
            a = str(random.randint(1,16))
            b = str(random.randint(1,20))
            c=random.choice(['A','B','C','D','F'])
            seat_id =a+'车'+b+c+'号'

            print(oid)
            if seat == '':
                status = 1
                tip='请选择座位类型！'
                print(tip)
            elif go_day=='':
                status=1
                tip = '请选择出行日期！'
            elif name=='':
                status=1
                tip = '请前往个人中心补全信息！'
            elif carid=='':
                status = 1
                tip = '请前往个人中心补全信息！'
            elif seat == '二等座':
                seat = 'c_seat'
                print(seat)
            elif seat == '一等座':
                seat = 'b_seat'
                print(seat)
            elif seat == '商务座':
                seat = 'a_seat'
                print(seat)
            if seat!='' and go_day!='' and name!='' and carid!='':
                # 获取座位对应的价格
                s = seat[0]
                # print(s)
                if s!='a' and s!='b' and s!='c':
                    status=1
                    tip='座位类型错误！'
                else:

                    pricename = '{}_price'.format(s)
                    # print(pricename)
                    price = Tickets.objects.filter(id=ticket.id).values(pricename)
                    # print(price[0][pricename])
                    if seat!='' and go_day!='' and name!='' and carid!='':
                        order = Order(
                            oid = oid,
                            t_name=ticket.t_name,
                            start_station=ticket.start_station,
                            end_station=ticket.end_station,
                            start_time=ticket.start_time,
                            end_time=ticket.end_time,
                            go_day=go_day,
                            seat_id=seat_id,
                            seat_type=seat,
                            price=price[0][pricename],
                            username=username,
                            u_carid=carid
                        )
                        print('购买成功！')
                        # 购票成功后，该座位数量-1
                        if seat=='a_seat':
                            ticket.a_seat=ticket.a_seat-1
                            print(ticket.a_seat)
                        elif seat=='b_seat':
                            ticket.b_seat=ticket.b_seat-1
                            print(ticket.b_seat)
                        elif seat=='c_seat':
                            ticket.c_seat=ticket.c_seat-1
                            print(ticket.c_seat)
                        # elif seat!='a_seat' and seat!='b_seat' and seat!='c_seat':
                        #     status=1
                        #     tip='座位类型错误！'
                        if ticket.a_seat<1 or ticket.b_seat<1 or ticket.c_seat<1:
                            status=1
                            tip='余票不足！'
                        else:
                            #购票后，钱包扣除对应金额
                            user.money=user.money-price[0][pricename]
                            if user.money<=0:
                                status=1
                                tip='余额不足！请充值。'
                            else:
                                order.save()
                                ticket.save()
                                user.save()
                                success = 1
                                tip = '购票成功，请提前取票！'


    return render(request,'buy_ticket.html',locals())


def main_order_all(request,page=1):
    username = Session.objects.first().username
    # print(username)
    orders = Order.objects.filter(username=username)
    for order in orders:
        if order.seat_type=='a_seat':
            order.seat_type = '商务座'
        elif order.seat_type=='b_seat':
            order.seat_type = '一等座'
        elif order.seat_type=='c_seat':
            order.seat_type = '二等座'
    paginator = Paginator(orders, 25)
    pager = paginator.page(page)
    return render(request,'main_order_all.html',locals())


def user_edit(request):
    login_user = Session.objects.first()
    if not login_user:
        return render(request, 'main_login_register.html')
    else:
        user = User.objects.filter(username=login_user.username)[0]
        if request.method=='POST':
            new_username = request.POST.get('username')
            new_sex = request.POST.get('sex')
            new_email = request.POST.get('email')
            new_name = request.POST.get('name')
            new_carid = request.POST.get('carid')

            if not new_username:
                status = 1
                tip = '用户名不能为空！'
            elif new_username:
                exit_user = User.objects.filter(username=new_username)
                # print(exit_user)
                if not exit_user:
                    # print('不重复')
                    user.username=new_username
                    user.save()
                elif exit_user[0].username==user.username:
                    # print('是当前用户')
                    user.username=new_username
                else:
                    status=1
                    tip='用户已存在！'

            if not new_email:
                status = 1
                tip = '邮箱不能为空！'
            elif new_email:
                exit_email = User.objects.filter(email=new_email)
                # print(exit_email)
                if not exit_email:
                    # print('不重复')
                    user.email = new_email
                    user.save()
                elif exit_email[0].email == user.email:
                    # print('是当前用户的邮箱')
                    pass
                else:
                    status = 1
                    tip = '邮箱已被注册！'


            if not new_carid:
                status = 1
                tip = '身份证号不能为空！'
            elif new_carid:
                exit_carid = User.objects.filter(carid=new_carid)
                # print(exit_carid)
                if not exit_carid:
                    # print('不重复')
                    user.carid=new_carid
                    user.save()
                elif exit_carid[0].carid==user.carid:
                    # print('是当前用户的身份证号')
                    pass
                else:
                    status=1
                    tip='该身份证号已被注册！'

            if  not new_name:
                status=1
                tip='请输入真实姓名'
            else:
                user.name = new_name
                user.save()
            if not  new_sex:
                status=1
                tip='请输入性别'
            else:
                user.sex = new_sex
                user.save()



    return render(request,'user_edit.html',locals())


def admin_call_user(request,user='duanyinan9'):
    users = Chat.objects.order_by('sendfrom').values('sendfrom').distinct()
    print(users)
    for i in users:
        if i['sendfrom']=='admin':
            i['sendfrom']='聊天列表'
    print(users)
    if request.method=='POST':
        text = request.POST.get('text')
        chat = Chat(sendfrom='admin',sendto=user,text=text)
        chat.save()
    return render(request,'admin_call_user.html',locals())


def admin_talk_area(request,user):
    chat = Chat.objects.filter(Q(sendfrom=user)|Q(sendto=user))
    return render(request,'admin_talk_area.html',locals())


def add_money(request):
    username = Session.objects.first().username
    user = User.objects.filter(username=username)[0]
    if request.method=='POST':
        money = request.POST.get('money')
        if not money:
            status=1
            tip='请输入金额！'
        else:
            user.money += int(money)
            user.save()
    return render(request,'add_money.html',locals())


def edit_pswd(request):
    username = Session.objects.first().username
    user = User.objects.filter(username=username)[0]

    if request.method=='POST':
        password = request.POST.get('password')
        new_password = request.POST.get('new_password')
        if not password or not  new_password:
            status=1
            tip='请输入密码!'
        else:
            md5 = hashlib.md5()
            md5.update(password.encode('utf8'))
            if md5.hexdigest()!=user.password:
                status=1
                tip='原密码错误!'
            else:
                md5.update(new_password.encode('utf8'))
                user.password=md5.hexdigest()
                user.save()

    return render(request,'edit_pswd.html',locals())


def wait(request):
    return render(request,'wait.html')


def admin_login(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            status=1
            tip='请输入用户名或密码！'
        else:
            if username=='admin' and password=='123456':
                return render(request,'admin_index.html',locals())
            else:
                status=1
                tip='用户名或密码错误！'
    return render(request,'admin_login.html',locals())


def admin_left(request):
    return render(request,'admin_left.html',locals())


def admin_header(request):
    return render(request,'admin_header.html',locals())


def admin_foot(request):
    return render(request,'admin_foot.html',locals())

def check_price(c,b,a):

    if re.fullmatch(r'\d*\.?\d{0,2}', c) == None:
        print(1)
        return 1
    elif re.fullmatch(r'\d*\.?\d{0,2}', b) == None:
        print(2)
        return 1
    elif re.fullmatch(r'\d*\.?\d{0,2}', a) == None:
        print(3)
        return 1
    else:
        return 0

def edit_ticket(request,id):
    ticket = Tickets.objects.filter(id=id)[0]
    if request.method=='POST':
        t_name          = request.POST.get('t_name')
        start_station   = request.POST.get('start_station')
        end_station     = request.POST.get('end_station')
        start_time      = request.POST.get('start_time')
        end_time        = request.POST.get('end_time')
        time            = request.POST.get('time')
        c_seat          = request.POST.get('c_seat')
        c_price         = request.POST.get('c_price')
        b_seat          = request.POST.get('b_seat')
        b_price         = request.POST.get('b_price')
        a_seat          = request.POST.get('a_seat')
        a_price         = request.POST.get('a_price')

        if t_name== '' :
            status=1
            tip='请输入车次！'
        elif start_station== '':
            status = 1
            tip = '请输入始发站！'
        elif end_station== '':
            status = 1
            tip = '请输入终点站！'
        elif start_time== '':
            status = 1
            tip = '请输入发车时间！'
        elif end_time== '':
            status = 1
            tip = '请输入到站时间！'
        elif time== '':
            status = 1
            tip = '请输入总时长！'
        elif c_seat== '':
            status = 1
            tip = '请输入二等座数量！'
        elif c_price== '':
            status = 1
            tip = '请输入二等座价格！'
        elif b_seat== '':
            status = 1
            tip = '请输入一等座数量！'
        elif b_price== '':
            status = 1
            tip = '请输入一等座价格！'
        elif a_seat== '':
            status = 1
            tip = '请输入商务座数量！'
        elif a_price== '':
            status = 1
            tip = '请输入商务座价格！'
        elif check_price(c_price,b_price,a_price):
            status=1
            tip='价格错误！'
        else:

            ticket.t_name=t_name
            ticket.start_station=start_station
            ticket.end_station=end_station
            ticket.start_time=start_time
            ticket.end_time=end_time
            ticket.time=time
            ticket.c_seat=c_seat
            ticket.c_price=float(c_price)
            ticket.b_seat=b_seat
            ticket.b_price=float(b_price)
            ticket.a_seat=a_seat
            ticket.a_price=float(a_price)

            ticket.save()
            print('修改成功')
            status = 1
            tip = '修改成功！'

    return render(request,'admin_edit_ticket.html',locals())


def del_ticket(request,id):
    try:
        ticket=Tickets.objects.get(id=id)
        if ticket:
            ticket.status=0
            ticket.save()
    except Exception as e:
        print(e)
    return admin_main_show_train(request,page=1)


def ticket_del_log(request,page=1):
    tickets = Tickets.objects.filter(status=0)
    paginator = Paginator(tickets, 7)
    pager = paginator.page(page)
    return render(request,'ticket_del_log.html',locals())


def restore_ticket(request,id):
    ticket = Tickets.objects.get(id=id)
    ticket.status=1
    ticket.save()
    return ticket_del_log(request,page=1)


def user_manage(request):
    users = User.objects.all()
    if request.method=='POST':
        username = request.POST.get('username')
        users = User.objects.filter(username=username)
    return render(request,'user_manage.html',locals())


def del_user(request,id):
    try:
        user = User.objects.get(id=id)
        if user:
            user.delete()
    except Exception as e:
        print(e)
    return user_manage(request)


def station_manage(request):
    stations = Station.objects.order_by('station').all()
    if request.method=='POST' and 'sel' in request.POST:
        sel_sta = request.POST.get('sel_sta')
        sta = Station.objects.filter(station=sel_sta)
        if not sta:
            status=1
            tip='没有该车站！'
        else:
            return render(request,'station_manage.html',locals())
    elif request.method=='POST' and 'add' in request.POST:
        station =request.POST.get('station')
        en_station =request.POST.get('en_station')
        city =request.POST.get('city')
        sta = Station.objects.filter(station=station)
        if sta:
            status=1
            tip='已存在该车站！'
        elif not en_station:
            status=1
            tip='请输入英文名'
        elif not city:
            status=1
            tip='请输入城市'
        else:
            new_sta = Station(station=station,en_station=en_station,city=city)
            new_sta.save()
            return render(request,'station_manage.html',locals())
    elif request.method=='POST' and 'save' in request.POST:
        station = request.POST.get('station')
        en_station = request.POST.get('en_station')
        city = request.POST.get('city')

        if not station:
            status = 1
            tip = '请输入车站名！'
        elif not en_station:
            status = 1
            tip = '请输入英文名'
        elif not city:
            status = 1
            tip = '请输入城市！'
        else:
            sta = Station.objects.filter(station=station)
            if not sta:
                status=1
                tip='没有该车站！'
            else:
                sta[0].station = station
                sta[0].en_station = en_station
                sta[0].city=city
                sta[0].save()
                return render(request,'station_manage.html',locals())
    elif request.method=='POST' and 'del' in request.POST:
        station = request.POST.get('station')
        en_station = request.POST.get('en_station')
        city = request.POST.get('city')

        if not station:
            status = 1
            tip = '请输入车站名！'
        elif not en_station:
            status = 1
            tip = '请输入英文名'
        elif not city:
            status = 1
            tip = '请输入城市！'
        else:
            sta = Station.objects.filter(station=station)
            if not sta:
                status=1
                tip='没有该车站！'
            elif sta[0].station == station and sta[0].en_station == en_station and sta[0].city == city:
                sta[0].delete()
                return render(request,'station_manage.html',locals())
            else:
                status=1
                tip='车次信息不匹配！'
    return render(request,'station_manage.html',locals())