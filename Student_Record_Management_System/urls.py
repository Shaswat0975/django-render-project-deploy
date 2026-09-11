"""
URL configuration for Student_Record_Management_System project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
# from Student.views import index
# from Student.views import about
from Student.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",index,name="home"),
    path("about",about,name="about"),
    # path("Student_feedback",Student_feedback,name="Student_feedback"),
    path("login",login,name="login"),
    path("AdminHome",AdminHome,name="AdminHome"),
    path("add_student",add_student,name="add_student"),
    path("view_students",view_students,name="view_students"),
    path("edit_student/<int:id>",edit_student,name="edit_student"),
    path("Student_feedback",Student_feedback,name="Student_feedback"),
    path("del_student/<int:id>",del_student,name="del_student"),
    path("view_feedback",view_feedback,name="view_feedback"),
    path("search_students",search_students,name="search_students"),
    path("search_records",search_records,name="search_records"),
    path("admin_logout",admin_logout,name="admin_logout"),
    path("change_password",change_password,name="change_password"),
    path("update_password",update_password,name="update_password"),
    path("student_home",student_home,name="student_home"),
    path("edit_profile",edit_profile,name="edit_profile"),
    path("student_fee",fee_details,name='student_fee'),
    path("fee_receipt",fee_receipt,name='fee_receipt'),
    path("change_user_password",change_user_password,name='change_user_password'),
    path("user_update_password",user_update_password,name='user_update_password')
]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)