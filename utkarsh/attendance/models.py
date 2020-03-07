from django.db import models
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class_choices = (
        ('I','I'),
    ('II','II'),
    ('III','III'),
    ('IV','IV'),
    ('V','V'),
    ('VI','VI'),
    ('VII','VII'),
    ('VIII','VIII'),
    ('IX','IX'),
    ('X','X'),
    ('XI','XI'),
    ('XII','XII'),
)
gender_choices=(('M','M'),
    ('F','F'),
    )

year_choices = (
        ('I','I'),
    ('II','II'),
    ('III','III'),
    ('IV','IV'),
    )
role_choices=(('Subject POC','Subject POC'),
    ('Mentor','Mentor'),)
attendance_choices=(('Present','Present'),
    ('Absent','Absent'),)
subject_choices=(('Maths','Maths'),('Science','Science'),('English','English'))
visit_choices=(('Green','Green'),('Red','Red'),('Need Discussion','Need Discussion'),('Another Visit','Another Visit'))


class School(models.Model):
    school_name=models.CharField(max_length=100)
    school_contact=models.CharField(max_length=100,blank=True,null=True)
    school_address=models.CharField(max_length=300,blank=True,null=True)
    def __str__(self):
        return f'{self.school_name}'

class Subject(models.Model):
    subject_name=models.CharField(max_length=20)
    date=models.DateField()
    

    def __str__(self):
        return f'{self.subject_name}'
#add default subjects to volounteers students
class Volounteer(models.Model):
    volounteer_name=models.CharField(max_length=50)
    volounteer_year=models.CharField(max_length=10,choices=year_choices)
    volounteer_role=models.CharField(max_length=20,choices=role_choices)
    volounteer_gender=models.CharField(max_length=2,choices=gender_choices,blank=True,null=True)
    absent=models.IntegerField(blank=True,null=True,default=0)
    present=models.IntegerField(blank=True,null=True,default=0)
    volounteer_subject_taught=models.ManyToManyField(Subject)
    volounteer_image=models.ImageField(upload_to ='teacher/displaypic',blank=True,null=True)


    def __str__(self):
        return f'{self.volounteer_name}'

class Student(models.Model):
    name=models.CharField(max_length=100)
    standard=models.CharField(choices=class_choices,max_length=50)
    address=models.CharField(max_length=300,blank=True,null=True)
    contact=models.CharField(max_length=15,blank=True,null=True)
    school=models.ForeignKey(School,on_delete=models.CASCADE,blank=True,null=True)
    gender=models.CharField(max_length=2,choices=gender_choices,blank=True,null=True)
    absent=models.IntegerField(blank=True,null=True,default=0)
    present=models.IntegerField(blank=True,null=True,default=0)
    student_image=models.ImageField(upload_to ='student/displaypic',blank=True,null=True)
    mentor=models.ForeignKey(Volounteer,on_delete=models.CASCADE,blank=True,null=True)
    fees=models.PositiveIntegerField(null=True,blank=True)
    lead=models.ForeignKey(Volounteer,on_delete=models.CASCADE,blank=True,null=True,related_name='volounteer_lead')
    purpose=models.CharField(choices=(('Attendance','Attendance'),('Visit','Visit')),max_length=200,blank=True,null=True)
    def __str__(self):
        return f'{self.name}'

class Attendance(models.Model):
    student_name=models.ForeignKey(Student,on_delete=models.CASCADE)
    date=models.DateField()
    has_attended=models.CharField(choices=attendance_choices,max_length=50,default='Absent')


class volounteerAttendance(models.Model):
    volounteer_name1=models.ForeignKey(Volounteer,on_delete=models.CASCADE)
    date=models.DateField()
    has_attended=models.CharField(choices=attendance_choices,max_length=50)

class Date(models.Model):
    date_today=models.DateField()
    subject=models.CharField(choices=subject_choices,max_length=20,default='Maths')

class Post(models.Model):
    title=models.CharField(max_length=100,blank=True,null=True)
    message=models.TextField(max_length=100000)
    posted_by=models.ForeignKey(Volounteer,on_delete=models.CASCADE,null=True,blank=True)
    posted_on=models.DateTimeField()
    post_image=models.ImageField(blank=True,null=True)
    likes=models.PositiveIntegerField(default=0)

class Comment(models.Model):
    comment_by=models.ForeignKey(Volounteer,on_delete=models.CASCADE,null=True,blank=True)
    my_comment=models.TextField(max_length=100000)
    on_date=models.DateTimeField()
    on_post=models.ForeignKey(Post,on_delete=models.CASCADE,null=True,blank=True)

class Visit(models.Model):
    visit_lead=models.ForeignKey(Volounteer,on_delete=models.CASCADE,null=True,blank=True)
    visit_on=models.DateTimeField(auto_now=True)
    visit_with=models.ManyToManyField(Volounteer,related_name='volounteer_visitors')
    visit_student=models.ForeignKey(Student,on_delete=models.CASCADE,null=True,blank=True)
    visit_comments=models.TextField(max_length=100000,null=True,blank=True)
    visit_outcome=models.CharField(choices=visit_choices,default='Another Visit',max_length=27)
    visit_final=models.PositiveIntegerField(null=True,blank=True)
    visit_discussion=models.CharField(max_length=90,choices=(('Discussed','Discussed'),('Not Discussed','Not Discussed')),default='Not Discussed')


    
    
    