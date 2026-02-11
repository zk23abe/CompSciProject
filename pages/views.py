from django.shortcuts import render, redirect, get_object_or_404
from .forms import StudentForm, InvoiceForm, LessonForm
from .models import Student, Invoice, Lesson, Message
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.contrib.auth.models import User

@login_required
def home(request):
    #check for studentor tutor
    if not request.user.is_superuser:
        return redirect('student_dashboard')
    #fech data from database
    all_students = Student.objects.all()
    all_invoices = Invoice.objects.all()
    all_lessons = Lesson.objects.all().order_by('lesson_date') 

    income_data = Invoice.objects.filter(status='PAID').aggregate(Sum('amount'))
    total_income = income_data['amount__sum'] or 0

    
    dashboard_stats = {
        "total_students": all_students.count(),
        #unpaid invoices
        "pending_invoices": all_invoices.filter(status='PENDING').count(),
        # total income
        "total_income": total_income,
        "active_students": all_students.count() 
    }

    
    context = {
        "stats": dashboard_stats,
        "lessons": all_lessons[:5],  #next 5 lessons + recent 5 invoices
        "invoices": all_invoices[:5], 
        "tutor_name": request.user.username,
        "all_students": all_students
    }

    return render(request, "home.html", context)
def about(request):
    return render(request, "about.html")

@login_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('home')  
    else:
        form = StudentForm()

    return render(request, 'add_student.html', {'form': form})

@login_required
def add_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            print("FORM IS INVALID")
            print(form.errors)
    else:
        form = InvoiceForm()

    return render(request, 'add_invoice.html',{'form': form})

@login_required
def add_lesson(request):
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form= LessonForm()

    return render(request, 'add_lesson.html', {'form': form})

@login_required
def delete_lesson(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)

    if request.method == 'POST':
        lesson.delete()
        return redirect('home')

    return render(request, 'delete_lesson.html', {'item': lesson})


@login_required
def edit_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method =='POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = InvoiceForm(instance=invoice)
    return render(request, 'add_invoice.html',{'form': form})

@login_required
def delete_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        invoice.delete()
        return redirect('home')
    return render(request, 'delete_confirmation.html',{'item': invoice})

@login_required
def student_detail(request,pk):
    student = get_object_or_404(Student, pk=pk)
#getting related data for that spcific student
    lessons = Lesson.objects.filter(student=student).order_by('lesson_date')
    invoices = Invoice.objects.filter(student=student).order_by('-due_date')
#calc personal invoice
    total_billed = invoices.aggregate(Sum('amount'))['amount__sum'] or 0
    total_paid = invoices.filter(status='PAID').aggregate(Sum('amount'))['amount__sum'] or 0
    balance_due = total_billed - total_paid
    context = {
        'student': student,
        'lessons': lessons,
        'invoices': invoices,
        'stats': {
            'billed': total_billed,
            'paid': total_paid,
            'balance': balance_due
        }
    }
    return render(request, 'student_detail.html', context)

@login_required
def student_dashboard(request):
    #check if user exists and type of user
    try:
        student_profile = request.user.student
    except Student.DoesNotExist:
        return redirect('home')

    # ensure only THIS student data is shown
    my_lessons = Lesson.objects.filter(student=student_profile).order_by('lesson_date')
    my_invoices = Invoice.objects.filter(student=student_profile).order_by('-due_date')

    #invoice for student
    total_billed = my_invoices.aggregate(Sum('amount'))['amount__sum'] or 0
    total_paid = my_invoices.filter(status='PAID').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_billed - total_paid

    context = {
        'student': student_profile,
        'lessons': my_lessons,
        'invoices': my_invoices,
        'balance': balance
    }
    
    return render(request, 'student_dashboard.html', context)
    

@login_required
def chat_view(request, user_id):
    #define ho is talking to who
    other_user = get_object_or_404(User, pk=user_id)
    
    #student can only contact tutor
    if not request.user.is_superuser and not other_user.is_superuser:
         return redirect('student_dashboard')

    #get chat history
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) | 
        Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')

    # handle new message(POST)
    if request.method == 'POST':
        body = request.POST.get('message_body')
        if body:
            Message.objects.create(
                sender=request.user,
                receiver=other_user, 
                body=body
            )
            return redirect('chat_view', user_id=user_id)

    context = {
        'other_user': other_user,
        'messages': messages
    }
    return render(request, 'chat.html', context)