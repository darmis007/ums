from django.shortcuts import render,reverse,redirect,get_object_or_404
from .models import *
from django.http import *
from .forms import *
from django.utils.timezone import datetime
from django.forms import formset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def list_dates(request):
    dates_list=Date.objects.all()
    context={}
    context['dates_list']=dates_list
    return render(request,'dates.html',context)

@login_required
def daywise_attendance(request,id):
    context={}
    context['date']=Date.objects.get(id=id)
    context['students']=Attendance.objects.filter(date=Date.objects.get(id=id).date_today,has_attended='Present')
    return render(request,'daywise.html',context)

@login_required
def student_add(request):
    context={'add_form':addStudentForm()}
    if request.method=='POST':
        form=addStudentForm(request.POST)
        if form.is_valid:
            
            form.save()
            return HttpResponseRedirect(reverse('student_list'))
        else:
            return render(request,'add.html',context=context)
    else:
         form=addStudentForm()
         return render(request,'add.html',context=context)      
    return render(request,'add.html',context=context)

@login_required
def student_details(request,id):
    context={}
    context['student']=Student.objects.get(id=id)
    context['attendance']=Attendance.objects.filter(student_name=Student.objects.get(id=id),has_attended='Present')
    return render(request,'details.html',context)

@login_required
def volounteer_details(request,id):
    context={}
    context['user']=User.username
    context['volounteer']=Volounteer.objects.get(id=id)
    context['attendance']=volounteerAttendance.objects.filter(volounteer_name1=Volounteer.objects.get(id=id),has_attended='Present')
    context['students']=Student.objects.filter(mentor=Volounteer.objects.get(id=id))
    return render(request,'details_volounteer.html',context)    

@login_required
def mark_attendance(request):
    context={}
    students=Student.objects.all()
    count = students.count()
    context = {'students': students}
    attendance_formset = formset_factory(AttendanceForm, extra=count)
    date = datetime.today().date().strftime('%d-%m-%Y')
    if request.method == 'POST':
        formset = attendance_formset(request.POST)
        list = zip(students,formset)
        context['list']=list
        if formset.is_valid():
            for form, student in zip(formset,students):
                date = datetime.today()
                mark = form.cleaned_data['has_attended']
                check_attendance = Attendance.objects.filter(date=date,student_name=student)
                if check_attendance :
                    attendance = Attendance.objects.get(date=date,student_name=student)
                    if attendance.has_attended == 'Absent':
                        student.absent = student.absent - 1
                    elif attendance.has_attended == 'Present':
                        student.present = student.present - 1
                    attendance.has_attended = mark
                    attendance.save()
                
                else: 
                    attendance = Attendance()
                    attendance.student_name = student
                    attendance.date = date
                    attendance.has_attended = mark
                    attendance.save()

                if mark == 'Absent':
                    student.absent = student.absent + 1
                if mark == 'Present':
                    student.present = student.present + 1
                student.save()
            context = {'students': students}
            if Date.objects.filter(date_today=date):
                pass
            else:
                d3=Date()
                d3.date_today=date
                d3.save()
            return render(request,'index.html' ,context)
        else:
            error = "Something went wrong"
            context = {
                'error': error,
                'formset': formset,
                'students': students,
                'date':date,
                }
            return render(request, 'attendance.html', context)

    else:
        list = zip(students, attendance_formset())
        context = {
            'formset': attendance_formset(),
            'students': students,
            'list': list,
            'date':date,
            }

    return render(request,'attendance.html', context)

def mark_school_class_attendance(request,id,id1):
    context={}
    students=Student.objects.filter(school=School.objects.get(id=id),standard=id1,purpose='Attendance')
    count = students.count()
    context = {'students': students}
    attendance_formset = formset_factory(AttendanceForm, extra=count)
    date = datetime.today().date().strftime('%d-%m-%Y')
    if request.method == 'POST':
        formset = attendance_formset(request.POST)
        list = zip(students,formset)
        context['list']=list
        if formset.is_valid():
            for form, student in zip(formset,students):
                date = datetime.today()
                mark = form.cleaned_data['has_attended']
                check_attendance = Attendance.objects.filter(date=date,student_name=student)
                if check_attendance :
                    attendance = Attendance.objects.get(date=date,student_name=student)
                    if attendance.has_attended == 'Absent':
                        student.absent = student.absent - 1
                    elif attendance.has_attended == 'Present':
                        student.present = student.present - 1
                    attendance.has_attended = mark
                    attendance.save()
                
                else: 
                    attendance = Attendance()
                    attendance.student_name = student
                    attendance.date = date
                    attendance.has_attended = mark
                    attendance.save()

                if mark == 'Absent':
                    student.absent = student.absent + 1
                if mark == 'Present':
                    student.present = student.present + 1
                student.save()
            context = {'students': students}
            if Date.objects.filter(date_today=date):
                pass
            else:
                d3=Date()
                d3.date_today=date
                d3.save()
            return render(request,'index.html' ,context)
        else:
            error = "Something went wrong"
            context = {
                'error': error,
                'formset': formset,
                'students': students,
                'date':date,
                }
            return render(request, 'attendance.html', context)

    else:
        list = zip(students, attendance_formset())
        context = {
            'formset': attendance_formset(),
            'students': students,
            'list': list,
            'date':date,
            }

    return render(request,'attendance.html', context)

@login_required
def student_list(request):
    context={}
    context['students']=Student.objects.all()
    return render(request,'index.html',context)

@login_required
def volounteer_list(request):
    context={}
    context['volounteers']=Volounteer.objects.all()
    return render(request,'index_volounteer.html',context)





@login_required
def volounteer_add(request):
    context={'add_form':addVolounteerForm()}
    if request.method=='POST':
        form=addVolounteerForm(request.POST)
        if form.is_valid:
            
            form.save()
            return HttpResponseRedirect(reverse('volounteer_list'))
        else:
            return render(request,'add_volounteer.html',context=context)
    else:
         form=addVolounteerForm()
         return render(request,'add_volounteer.html',context=context)      
    return render(request,'add_volounteer.html',context=context)

@login_required
def subjectDate(request):
    context={}
    date = datetime.today().date().strftime('%Y-%m-%d')
    context['subjectForm']=subjectForm()
    context['date']=date
    if request.method=='POST':
        if Date.objects.get(date_today=date):
            form=subjectForm(request.POST)
            if form.is_valid():
                subject=form.cleaned_data['subject']
                date1= Date.objects.get(date_today=date)
                date1.subject=subject
                date1.save()
                context1={}
                return HttpResponseRedirect(reverse('mark_attendance'))
            else:
                return render(request,'subject.html',context)
        else:
            form=subjectForm(request.POST)
            if form.is_valid():
                d2=Date()
                d2.date_today=date
                d2.subject=form.cleaned_data['subject']
                d2.save()
                return HttpResponseRedirect(reverse('mark_attendance'))
            else:
                return render(request,'subject.html',context)
    return render(request,'subject.html',context)

def volounteer_edit(request,id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user_form = registrationForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()    
            return HttpResponseRedirect(reverse('volounteer_list'))
        else:
            return render(request, 'edit.html', {"user_form": registrationForm})
    else:
        user_form = registrationForm(instance=user)
        return render(request, 'edit.html', {"user_form": registrationForm})

def register(request):
    context={'register_form':registrationForm()}
    context['message']=''
    if request.method=='POST':
        form=registrationForm(request.POST)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse('login'))

        else:
            context['message']='Something went wrong'
            return render(request,'register.html',context)
    else:
        return render(request,'register.html',context)
    
    return render(request,'register.html',context)

def user_login(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('student_list'))
        else:
            context["error"] = "Provide valid credentials !!"
            return render(request, "login.html", context)
    else:
        return render(request, "login.html", context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

@login_required
def createPost(request):
    context={}
    context['posts']=Post.objects.all()
    context['post_form']=createPostForm()
    if request.method=='POST':
        form=createPostForm(request.POST)
        if form.is_valid():
            p1=Post()
            p1.title=form.cleaned_data['title']
            p1.message=form.cleaned_data['message']
            p1.posted_by=Volounteer.objects.get(volounteer_name=request.user.username)
            p1.posted_on=datetime.now()
            p1.save()
            return render(request,'home.html',context)

        else:
            context['message']='Something went wrong'
            return render(request,'post.html',context)
    else:
        return render(request,'post.html',context)
    
    return render(request,'post.html',context)

@login_required
def home(request):
    context={}
    context['posts']=Post.objects.all()
    return render(request,'home.html',context)

@login_required
def post_details(request,id):
    context={}
    context['post']=Post.objects.get(id=id)
    context['username']=Volounteer.objects.get(volounteer_name=request.user.username)
    context['comments']=Comment.objects.filter(on_post=Post.objects.get(id=id))
    return render(request,'post_details.html',context)

@login_required
def student_delete(request,id):
    context={}
    s1=Student.objects.get(id=id)
    s1.delete()
    context['students']=Student.objects.all()
    return HttpResponseRedirect(reverse('student_list'))

@login_required
def comment(request,id):
    context={}
    context['username']=request.user.username
    context['comment_form']=commentForm()
    if request.method=='POST':
        form=commentForm(request.POST)
        if form.is_valid():
            p1=Comment()
            p1.comment_by=Volounteer.objects.get(volounteer_name=request.user.username)
            p1.my_comment=form.cleaned_data['message']
            p1.on_post=Post.objects.get(id=id)
            p1.on_date=datetime.now()
            p1.save()
            return HttpResponseRedirect(reverse('post_details',args=[id]))

        else:
            context['message']='Something went wrong'
            return render(request,'comment.html',context)
    else:
        return render(request,'comment.html',context)
    
    return render(request,'comment.html',context)

@login_required
def edit_post(request,id):
    context={}
    context['post']=Post.objects.get(id=id)
    context['post_form']=createPostForm()
    if request.method=='POST':
        form=createPostForm(request.POST)
        if form.is_valid():
            p1=Post.objects.get(id=id)
            p1.title=form.cleaned_data['title']
            p1.message=form.cleaned_data['message']
            p1.save()
            return HttpResponseRedirect(reverse('post_details',args=[id]))

        else:
            context['message']='Something went wrong'
            return render(request,'post.html',context)
    else:
        return render(request,'post.html',context)
    
    return render(request,'post.html',context)

@login_required
def edit_comment(request,id,id1):
    context={}
    context['comment_form']=commentForm()
    if request.method=='POST':
        form=commentForm(request.POST)
        if form.is_valid():
            p1=Comment.objects.get(id=id1)
            p1.my_comment=form.cleaned_data['message']
            p1.save()
            return HttpResponseRedirect(reverse('post_details',args=[id]))

        else:
            context['message']='Something went wrong'
            return render(request,'comment.html',context)
    else:
        return render(request,'comment.html',context)
    
    return render(request,'comment.html',context)

def myvisits(request):
    context={}
    context['visits']=Student.objects.filter(purpose='Visit')
    return render(request,'myvisits.html',context)

@login_required
def visitInfo(request):
    context={}
    context['backgroundvisit_form']=backgroundVisitForm()
    if request.method=='POST':
        form=backgroundVisitForm(request.POST)
        if form.is_valid():
            form.visit_on=datetime.now()
            form.save()
            return render(request,'myvisits.html',context)
    return render(request,'visit.html',context)

def useWindow(request):
    context={}
    return render(request,'usewindow.html',context)

def addUniversalStudent(request):
    context={}
    context['addUniversalStudent_form']=addUniversalStudentForm()
    if request.method=='POST':
        form=addUniversalStudentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('addUniversalStudent'))
        else:
            context['error']='Something went wrong'
            return render(request,'add_universal_student.html',context)
    return render(request,'universal_student.html',context)

def addSchool(request):
    context={}
    context['addSchool_form']=addSchoolForm()
    if request.method=='POST':
        form=addSchoolForm(request.POST)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse('addSchool'))
        else:
            context['error']='Something went wrong'
            return render(request,'addSchool.html',context)
    return render(request,'addSchool.html',context)

def viewSchool(request,id):
    context={}
    context['school']=School.objects.get(id=id)
    students=Student.objects.filter(school=School.objects.get(id=id),purpose='Attendance')
    standards=[]
    for student in students:
        if student.standard not in standards:
            standards.append(student.standard)
    context['standards']=standards
    return render(request,'viewSchool.html',context)


def allSchool(request):
    context={}
    context['schools']=School.objects.all()
    return render(request,'schoolList.html',context)

def useWindow(request):
    context={}
    return render(request,'usewindow.html',context)

def visitList(request):
    context={}
    context['visits']=Visit.objects.filter(visit_discussion='Not Discussed')
    return(request,'visit_list.html',context)

def visitDetails(request,id):
    visit=Visit.objects.get(id=id)
    context={}
    context['visit']=visit
    context['finalDiscussion_form']=finalDiscussionForm()
    if request.method=='POST':
        form=finalDisscussionForm(request.POST)
        if form.is_valid:
            visit.visit_outcome=form.cleaned_data['outcome']
            visit.visit_final=form.cleaned_data['final']
            visit.visit_discussion='Discussed'
            visit.save()
            return HttpResponseRedirect(reverse('visitList'))
        else:
            context['error']='Something Went Wrong'
            return render(request,'visitDetails.html',context)
    return render(request,'visitDetails.html',context)

def editVisit(request,id):
    visit=Visit.objects.get(id=id)
    context={}
    context['editVisit_form']=editVisitForm()
    if request.method=='POST':
        form=editVisitForm(request.POST)
        if form.is_valid:
            visit.visit_outcome=form.cleaned_data['outcome']
            visit.visit_comments=form.cleaned_data['comment']
            visit.save()
            return HttpResponseRedirect(reverse('visitDetails',args=[id]))
        else:
            context['error']='Something went wrong'
            return render(request,'editVisit.html',context)
    return render(request,'editVisit.html',context)




            
