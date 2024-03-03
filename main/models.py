from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Bus_Type(models.Model):
    bus_type = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.bus_type

class Carousel(models.Model):
    head_line = models.CharField(max_length=99,default="")
    desc_line = models.CharField(max_length=99,default="")
    image_link = models.CharField(max_length=999,default="")

    def __str__(self) -> str:
        return self.head_line

class Route(models.Model):
    route_code = models.CharField(max_length=10,default="")
    route = models.CharField(max_length=100)

    def __str__(self):
        return self.route
    

class Schedule(models.Model):
    schedule_code = models.CharField(max_length=10,default="")
    schedule = models.CharField(max_length=100)


    def __str__(self):
        return self.schedule
    

class Driver(models.Model):
    driver_ID = models.IntegerField(default=0)
    name = models.CharField(max_length=150,default="")
    cnic = models.CharField(max_length=150,default="")
    city = models.CharField(max_length=100,default="")
    phone = models.CharField(max_length=12,default="")
    email = models.CharField(max_length=50,default="")
    licnese = models.CharField(max_length=50,default="")
    salary = models.IntegerField()

    def __str__(self):
        return self.name

class Buse(models.Model):
    bus_code = models.CharField(max_length=10,default="")
    type = models.OneToOneField(Bus_Type,on_delete=models.CASCADE,default="")
    capacity = models.IntegerField(default=0)
    bus_no = models.CharField(max_length=20,default="")
    route = models.OneToOneField(Route,on_delete=models.CASCADE)
    schedule = models.ManyToManyField(Schedule)
    driver = models.OneToOneField(Driver,on_delete=models.CASCADE)
    is_available = models.BooleanField(default=False)


    def __str__(self):
        return self.bus_no
    

class Passenger(models.Model):
    first_name = models.CharField(max_length=50,default="")
    last_name = models.CharField(max_length=50,default="")
    cnic = models.CharField(max_length=150,default="")
    city = models.CharField(max_length=100,default="")
    phone = models.CharField(max_length=12,default="")
    email = models.CharField(max_length=50,default="")


    def __str__(self):
        return self.first_name + self.last_name

class Ticket(models.Model):
    destination = models.CharField(max_length=100,default="")
    fare = models.IntegerField()
    availables = models.IntegerField()

    def __str__(self):
        return self.destination
    

class Reservation(models.Model):
    user = models.OneToOneField(Passenger,on_delete=models.CASCADE)
    ticket = models.OneToOneField(Ticket,on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=150,default="")
    boarding_point = models.CharField(max_length=150,default="")

    def __str__(self) -> str:
        return self.user + " booked ticket for " + self.ticket
    

class Routine(models.Model):
    route = models.OneToOneField(Route,on_delete=models.CASCADE,default="")
    Schedule = models.OneToOneField(Schedule,on_delete=models.CASCADE,default="")
    fare = models.IntegerField()
    bus_type = models.OneToOneField(Bus_Type,on_delete=models.CASCADE,default="")
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.route} at {self.Schedule}"
    
class OTP(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.IntegerField(blank=True)
    time_stamp = models.DateTimeField(auto_now=True)

class Contact(models.Model):
    serial_no = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    phone = models.CharField(max_length=100, default="")
    email = models.EmailField(max_length=100, default="")
    content = models.TextField()
    time_stamp = models.TimeField(auto_now_add=True)

    def __str__(self):
        return 'Message From'+f'{self.first_name}{self.last_name} - {self.email}'

class Userdetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=60, default="")
    first_name = models.CharField(max_length=60, default="")
    last_name = models.CharField(max_length=60, default="")
    phone = models.CharField(max_length=40, null=True)
    gender = models.CharField(max_length=10,default="")

    def __str__(self):
        return self.username+"'s "+" detail"