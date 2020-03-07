from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('student/',views.student_list,name='student_list'),
    path('volounteer/',views.volounteer_list,name='volounteer_list'),
    path('date/<int:id>/',views.daywise_attendance,name='day_attendance'),
    path('student/add/',views.student_add,name='add_attendance_student'),
    path('volounteer/add/',views.volounteer_add,name='add_volounteer'),
   #path('student/takeattendance/',views.mark_attendance,name='mark_attendance'),
    path('school/<int:id>/standard/<str:id1>/takeattendance',views.mark_school_class_attendance,name='mark_school_class'),
    path('student/<int:id>',views.student_details,name='student_details'),
    path('volounteer/<int:id>',views.volounteer_details,name='volounteer_details'),
    path('student/subject',views.subjectDate,name='subjectDate'),
    path('date/list',views.list_dates,name='list_dates'),
    path('register/',views.register,name='register'),
    path('volounteer/<int:id>/edit',views.volounteer_edit,name='volounteer_edit'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('',views.useWindow,name='mainpage'),
    path('home/',views.home,name='home'),
    path('post/create',views.createPost,name='post'),
    path('post/details/<int:id>',views.post_details,name='post_details'),
    path('post/details/<int:id>/edit',views.edit_post,name='post_edit'),
    path('student/details/<int:id>/delete',views.student_delete,name='student_delete'),
    path('post/details/<int:id>/comment',views.comment,name='comment'),
    path('post/details/<int:id>/comment/<int:id1>/edit',views.edit_comment,name='comment_edit'),
    path('visit/create',views.visitInfo,name='visitcreate'),
    path('universal/',views.useWindow,name='useWindow'),
    path('universal/student/add',views.addUniversalStudent,name='addUniversalStudent'),
    path('universal/school/add',views.addSchool,name='addSchool'),
    path('universal/school/<int:id>/view',views.viewSchool,name='viewSchool'),
    path('universal/school/list',views.allSchool,name='allSchool'),
    path('visit/<int:id>/details',views.visitDetails,name='visitDetails'),

]