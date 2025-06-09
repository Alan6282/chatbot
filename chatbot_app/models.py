from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin


# Create your models here
class user_det(models.Model):
    name = models.CharField(max_length=100)
    contact =models.CharField(max_length=10)
    login_id=models.OneToOneField('user_login',on_delete=models.CASCADE,related_name='user_det')
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # hash password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class user_login(AbstractBaseUser):
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=128)
    user_type=models.IntegerField(default=0)
    status =models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)  # <-- Add this
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()

    def __str__(self):
        return self.email


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
    experience = models.FileField(upload_to='upload')
    language = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=10)
    login_id = models.OneToOneField('user_login', on_delete=models.CASCADE, null=True, blank=True,related_name='expert')
class Expert_user_chat(models.Model):
    message= models.TextField()
    current_date=models.DateField(auto_now_add=True)
    current_time=models.DateTimeField(auto_now_add=True)
    receiver_id= models.ForeignKey('user_login', on_delete=models.CASCADE, related_name="expert_logid")
    sender_id = models.ForeignKey('user_login',on_delete=models.CASCADE, related_name="user_logid")
class Language(models.Model):
     code = models.CharField(max_length=5, unique=True)  # en, es, fr
     Language_name = models.CharField(max_length=50)
     flag_url = models.URLField()
     description = models.TextField()

     
class Language_selection(models.Model):
    DIFFICULTY_LEVELS = [
        ('A1', 'Beginner'), ('A2', 'Elementary'),
        ('B1', 'Intermediate'), ('B2', 'Upper Intermediate'),
        ('C1', 'Advanced'), ('C2', 'Mastery')
    ]
    language=models.CharField(max_length=50)
    difficulty = models.CharField(max_length=2, choices=DIFFICULTY_LEVELS,null=True)
    score=models.IntegerField(null=True)
    current_date=models.DateField(auto_now_add=True)
    current_time=models.TimeField(auto_now_add=True)
    user_id =models.ForeignKey('user_login', on_delete=models.CASCADE,related_name="user_lan_selection")

    
class AssessmentQuestion(models.Model):
    DIFFICULTY_LEVELS = [
        ('A1', 'Beginner'), ('A2', 'Elementary'),
        ('B1', 'Intermediate'), ('B2', 'Upper Intermediate'),
        ('C1', 'Advanced'), ('C2', 'Mastery')
    ]
    languages=[
        ('es', 'Spanish'),('fr', 'French',),('de', 'German'),('it', 'Italian'),('ja', 'Japanese'),('zh', 'Mandarin')
    ]
    
    
    language = models.CharField(max_length=2, choices=languages)
    question_text = models.TextField()
    options1 = models.CharField(max_length=100)
    options2 = models.CharField(max_length=100)
    options3 = models.CharField(max_length=100)
    correct_answer = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=2, choices=DIFFICULTY_LEVELS)
class Expert_request(models.Model):
    user_id=models.ForeignKey('user_login', on_delete=models.CASCADE,related_name="userid_request")
    expert_id=models.ForeignKey('user_login', on_delete=models.CASCADE,related_name="expertid_request")
    status=models.IntegerField(default=1)
    current_date=models.DateField(auto_now_add=True)
    current_time=models.TimeField(auto_now_add=True)
    schedule_date=models.DateField(null=True)
    schedule_time=models.TimeField(null=True)
    url=models.CharField(null=True,max_length=200)
class mock_test(models.Model):
       languages=[
        ('es', 'Spanish'),('fr', 'French',),('de', 'German'),('it', 'Italian'),('ja', 'Japanese'),('zh', 'Mandarin')
       ] 
       language = models.CharField(max_length=2, choices=languages)
       question_text = models.TextField()
       options1 = models.CharField(max_length=100)
       options2 = models.CharField(max_length=100)
       options3 = models.CharField(max_length=100)
       options4 = models.CharField(max_length=100)
       correct_answer = models.CharField(max_length=100)



    










