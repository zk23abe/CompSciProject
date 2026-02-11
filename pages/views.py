from django.shortcuts import render, redirect, get_object_or_404
from .forms import StudentForm, InvoiceForm, LessonForm
from .models import Student, Invoice, Lesson
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

@login_required
def home(request):
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
    
