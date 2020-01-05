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
def volounteer_mark_attendance(request):
    context={}
    volounteers=Volounteer.objects.all()
    count = volounteers.count()
    context = {'volounteers': volounteers}
    attendance_formset = formset_factory(AttendanceForm, extra=count)
    date = datetime.today().date().strftime('%d-%m-%Y')
    if request.method == 'POST':
        formset = attendance_formset(request.POST)
        list = zip(volounteers,formset)
        context['list']=list
        if formset.is_valid():
            for form, volounteer in zip(formset,volounteers):
                date = datetime.today()
                mark = form.cleaned_data['has_attended']
                check_attendance = volounteerAttendance.objects.filter(date=date,volounteer_name1=volounteer)
                if check_attendance :
                    attendance = volounteerAttendance.objects.get(date=date,volounteer_name1=volounteer)
                    if attendance.has_attended == 'Absent':
                        volounteer.absent = volounteer.absent - 1
                    elif attendance.has_attended == 'Present':
                        volounteer.present = volounteer.present - 1
                    attendance.has_attended = mark
                    attendance.save()
                
                else: 
                    attendance = volounteerAttendance()
                    attendance.volounteer_name1 = volounteer
                    attendance.date = date
                    attendance.has_attended = mark
                    attendance.save()

                if mark == 'Absent':
                    volounteer.absent = volounteer.absent + 1
                if mark == 'Present':
                    volounteer.present = volounteer.present + 1
                volounteer.save()
            context = {'volounteers': volounteers}
            if Date.objects.get(date_today=date):
                pass
            else:
                d3=Date()
                d3.date_today=date
                d3.save()
            return render(request,'index_volounteer.html' ,context)
        else:
            error = "Something went wrong"
            context = {
                'error': error,
                'formset': formset,
                'volounteers': volounteers,
                'date':date,
                }
            return render(request, 'attendance_volounteer.html', context)

    else:
        list = zip(volounteers, attendance_formset())
        context = {
            'formset': attendance_formset(),
            'volounteers': volounteers,
            'list': list,
            'date':date,
            }

    return render(request,'attendance_volounteer.html', context)


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


