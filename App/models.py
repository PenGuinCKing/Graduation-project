from django.db import models

# Create your models here.
# 用户模型
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=16,unique=True)
    password = models.CharField(max_length=255,unique=True)
    email = models.CharField(max_length=255,unique=True)
    reg_time = models.DateTimeField(auto_now_add=True)
    sex = models.CharField(max_length=50)
    money =models.DecimalField(max_digits=10,decimal_places=2)
    carid = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    class Meta:
        db_table='users'
        ordering = ['id']

# 登陆状态模型
class Session(models.Model):
    id = models.AutoField(primary_key=True)
    is_login = models.CharField(max_length=10)
    username = models.CharField(max_length=16)
    class Meta:
        db_table='session'
        ordering=['id']

# 车票模型
class Tickets(models.Model):
    id              = models.AutoField(primary_key=True)
    t_name          = models.CharField(max_length=50,unique=True)
    start_station   = models.CharField(max_length=50)
    end_station     = models.CharField(max_length=50)
    start_time      = models.TimeField()
    end_time        = models.TimeField()
    time            = models.TimeField()
    c_seat          = models.IntegerField(max_length=10)
    c_price         = models.DecimalField(max_digits=10,decimal_places=2)
    b_seat          = models.IntegerField(max_length=10)
    b_price         = models.DecimalField(max_digits=10,decimal_places=2)
    a_seat          = models.IntegerField(max_length=10)
    a_price         = models.DecimalField(max_digits=10,decimal_places=2)
    status          = models.IntegerField(max_length=10)
    class Meta:
        db_table='tickets'
        ordering=['start_time']

# 订单模型
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    oid = models.CharField(max_length=50)
    t_name = models.CharField(max_length=50)
    start_station = models.CharField(max_length=50)
    end_station = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    go_day = models.DateField()
    seat_id = models.CharField(max_length=50)
    seat_type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    username = models.CharField(max_length=50)
    u_carid = models.CharField(max_length=50)
    buy_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table='orders'
        ordering=['-buy_time']

# 站点类
class Station(models.Model):
    id = models.AutoField(primary_key=True)
    station = models.CharField(max_length=50)
    en_station= models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    class Meta:
        db_table='stations'
        ordering=['id']

# 聊天记录类
class Chat(models.Model):
    id=models.AutoField(primary_key=True)
    sendfrom=models.CharField(max_length=50)
    sendto = models.CharField(max_length=50)
    text =models.CharField(max_length=255)
    time=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table='chat'
        ordering=['time']