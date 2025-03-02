from django.db import models


# Create your models here
class user_det(models.Model):
    name = models.CharField(max_length=100)
    contact =models.CharField(max_length=10)
    login_id=models.ForeignKey('user_login',on_delete=models.CASCADE)

class user_login(models.Model):
    email=models.EmailField()
    password=models.CharField(max_length=100)
    user_type=models.IntegerField(default=0)
    status =models.IntegerField(default=0)


class Expert_det(models.Model):
    OPTIONS = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    ]
    
    name = models.CharField(max_length=50)
    gender = models.CharField(
        max_length=6,  
        choices=OPTIONS,
        default='Male'
    )
    age = models.IntegerField()
    experience = models.CharField(max_length=50)
    language = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=10)
    login_id = models.ForeignKey('user_login', on_delete=models.CASCADE, null=True, blank=True)
class Expert_user_chat(models.Model):
    message= models.TextField()
    current_date=models.DateField(auto_now_add=True)
    current_time=models.TimeField(auto_now_add=True)
    receiver_id= models.ForeignKey('user_login', on_delete=models.CASCADE, related_name="expert_logid")
    sender_id = models.ForeignKey('user_login',on_delete=models.CASCADE, related_name="user_logid")
class Language_selection(models.Model):
    language=models.CharField(max_length=50)
    current_date=models.DateField(auto_now_add=True)
    current_time=models.TimeField(auto_now_add=True)
    user_id =models.ForeignKey('user_login', on_delete=models.CASCADE,related_name="user_lan_selection")

    










