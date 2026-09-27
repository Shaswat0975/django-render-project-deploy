from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User,auth
from .models import Student,Feedback
from django.contrib.auth.decorators import login_required
from functools import wraps

def student_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('student_id'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

from django.http import HttpResponse
from reportlab.pdfgen import canvas
import datetime

# Create your views here.
def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")


def login(request):
    error = ""
    role = request.GET.get('role', request.POST.get('role', ''))

    if request.method == "POST":
        u = request.POST['email']
        p = request.POST['password']

        # Student Login
        if role == "student":
            try:
                stu = Student.objects.get(username=u, password=p)
                request.session['student_id'] = stu.id
                return redirect("student_home")
            except Student.DoesNotExist:
                error = "Invalid Student Username or Password"

        # Admin Login
        elif role == "admin":
            admin = auth.authenticate(username=u, password=p)

            if admin is not None and admin.is_staff:
                auth.login(request, admin)
                return redirect("AdminHome")
            else:
                error = "Invalid Admin Username or Password"

    return render(request, "login.html", {
        "error": error,
        "role": role
    })

@login_required(login_url='/login?role=admin')
def AdminHome(request):
    return render(request,"AdminHome.html")

@login_required(login_url='/login?role=admin')
def add_student(request):
    error=""
    if request.method=="POST":
        n=request.POST['sname']   # [they are form name]
        e=request.POST['email']
        u=request.POST['uname']
        ps=request.POST['password']
        c=request.POST['college']
        city=request.POST['city']
        jd=request.POST['jdate']
        tf=request.POST['tfee']
        pf=request.POST['pfee']
        lf=request.POST['lfee']
        ph=request.POST['phone']
        tech=request.POST['technology']
        img=request.FILES['img']
        try:
            Student.objects.create(name=n,email=e,username=u,password=ps,college=c,city=city,jdate=jd,total_fee=tf,paid_fee=pf,left_fee=lf,phone=ph,technology=tech,image=img)
            error="no"
        except Exception as e:
            print("ADD STUDENT ERROR:",e)
            error="yes"
    d={"error":error}
    return render(request,"add_student.html",d)

@login_required(login_url='/login?role=admin')
def view_students(request):
    data=Student.objects.all()
    d={'data':data}
    return render(request,"view_students.html",d)

@login_required(login_url='/login?role=admin')
def edit_student(request,id):
    data=Student.objects.get(id=id)
    error=""
    if request.method == "POST":
        n=request.POST['fname']
        e=request.POST['email']
        c=request.POST['college']
        city=request.POST['city']
        jd=request.POST['jdate']
        tf=request.POST['tfee']
        pf=request.POST['pfee']
        lf=request.POST['lfee']
        ph=request.POST['ph']
        tech=request.POST['technology']

        #update data
        data.name=n
        data.email=e
        data.college=c
        data.city=city
        data.jdate=jd
        data.total_fee=tf
        data.paid_fee=pf
        data.left_fee=lf
        data.phone=ph
        data.technology=tech
        try:
            data.save();
            error="no"
        except Exception as e:
            print(e)
            error="yes"
    return render(request,"edit_student.html",{'data':data,'erroe':error})

@student_login_required
def Student_feedback(request):
    error=""
    if request.method=="POST":
        n=request.POST['sname']
        e=request.POST['email']
        f=request.POST['Feedback']
        try:
            Feedback.objects.create(name=n,email=e,feedback=f)
            error="no"
        except:
            error="yes"
    d={"error":error}
    return render(request,"Student_feedback.html",d)

@login_required(login_url='/login?role=admin')
def del_student(request,id):
    data=Student.objects.get(id=id)
    data.delete()
    return redirect('view_students')

@login_required(login_url='/login?role=admin')
def view_feedback(request): 
    data=Feedback.objects.all()
    d={'data':data}
    return render(request,"view_feedback.html",d)

@login_required(login_url='/login?role=admin')
def search_students(request):
    return render(request,"search_students.html",)

@login_required(login_url='/login?role=admin')
def search_records(request):
    n=request.POST['sname']
    data=Student.objects.filter(name__icontains=n)
    d={"data":data}
    return render(request,"view_students.html",d)


def admin_logout(request):
    logout(request)
    return redirect('login')


def change_password(request):
    return render(request,"change_password.html")


def update_password(request):
    op=request.POST['old_password']
    np=request.POST['new_password']
    user=request.user
    if not user.check_password(op):
        return redirect('change_password.html')
    user.set_password(np)
    user.save()
    return redirect('login')

@student_login_required
def student_home(request):
    sid = request.session.get('student_id')

    if not sid:
        return redirect('login')

    stu = Student.objects.get(id=sid)

    return render(request, "student_home.html", {'student': stu})

@student_login_required
def edit_profile(request):
    if 'student_id' not in request.session:
        return redirect('login')

    sid = request.session['student_id']
    stu = Student.objects.get(id=sid)

    if request.method == "POST":
        stu.name = request.POST.get('fname', stu.name)
        stu.email = request.POST.get('email', stu.email)
        stu.city = request.POST.get('city', stu.city)
        stu.phone = request.POST.get('phone', stu.phone)

        # Image optional hai
        img = request.FILES.get('img')
        if img:
            stu.image = img

        stu.save()

    d = {'student': stu}
    return render(request, 'edit_profile.html', d)

@student_login_required
def fee_details(request):
    sid=request.session.get('student_id')
    if sid is None:
        return redirect('login')
    stu=Student.objects.get(id=sid)
    return render(request,"fee_details.html",{"student":stu})

@student_login_required
def fee_receipt(request):
    sid=request.session.get('student_id')
    if sid is None:
        return redirect('login')
    stu=Student.objects.get(id=sid)
    response=HttpResponse(content_type='application/pdf')
    response['content-Disposition']='attachment;filename="fee_receipt.pdf"'
    pdf=canvas.Canvas(response) 
    # Headings

    pdf.setTitle("Student Fee Receipt")
    pdf.setFont("Helvetica-Bold",22)

    pdf.drawString(140,800,"Student Record System")
    pdf.setFont("Helvetica",13)
    pdf.drawString(180,780,"STUDENT FEE RECEIPT")
    pdf.line(40,765,550,765)

    # Receipt Details

    receipt_no="SRM" +str(stu.id).zfill(4)
    #SRM0007
    pdf.setFont("Helvetica",12)
    pdf.drawString(50,740,"Receipt no :" +receipt_no)
    pdf.drawString(530,740,"Date :"+datetime.datetime.now().strftime("%d %n %y"))
    pdf.line(40,725,550,725)

    #Student details
    pdf.setFont("Helvetica-Bold",14)
    pdf.drawString(50,700,"Student Details")

    pdf.setFont("Helvetica",12)
    pdf.drawString(50,670,"Name : " +str(stu.name))
    pdf.drawString(50,645,"Email : " +str(stu.email))
    pdf.drawString(50,620,"Phone : " +str(stu.phone))
    pdf.drawString(50,595,"College : " +str(stu.college))
    pdf.drawString(50,570,"Course : " +str(stu.technology))
    pdf.line(40,545,550,545)

    # FEE Details
    pdf.setFont("Helvetica-Bold",14)
    pdf.drawString(50,520,"Fee Details")

    pdf.setFont("Helvetica",12)

    pdf.drawString(50,490,"Total_fee")
    pdf.drawString(250,490,"Rs" +str(stu.total_fee))

    pdf.drawString(50,465,"Paid_fee")
    pdf.drawString(250,465,"Rs" +str(stu.paid_fee))

    pdf.drawString(50,440,"Remaining_fee")
    pdf.drawString(250,440,"Rs" +str(stu.left_fee))

    pdf.line(40,410,550,410)

    #Footer
    pdf.setFont("Helvetica",11)
    pdf.drawString(50,380,"This is a computer generated fee receipt")

    pdf.setFont("Helvetica",11)
    pdf.drawString(395,140,"Authorized sign")
    pdf.save()
    return response

@student_login_required
def change_user_password(request):
    return render(request,"change_user_password.html")

@student_login_required
def user_update_password(request):
    sid=request.session.get('student_id')
    if sid is None:
        return redirect('login')
    stu=Student.objects.get(id=sid)
    error={}
    if request.method == "POST":
        old_password=request.POST['old_password']
        new_password=request.POST['new_password']
        if stu.password != old_password:
            error="Current password is incorrect"
        else:
            stu.password=new_password
            stu.save()
            error="done"
    return render(request,"change_user_password.html",{"error":error})

def student_logout(request):
    request.session.pop('student_id',None)
    return redirect('login')
