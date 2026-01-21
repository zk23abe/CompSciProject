from django.shortcuts import render
from .forms import StudentForm
from .models import Student, Invoice, Lesson 
from django.shortcuts import render, redirect

def home(request):
    #fech data from database
    all_students = Student.objects.all()
    all_invoices = Invoice.objects.all()
    all_lessons = Lesson.objects.all().order_by('lesson_date') 

    
    dashboard_stats = {
        "total_students": all_students.count(),
        #unpaid invoices
        "pending_invoices": all_invoices.filter(status='Pending').count(),
        # total income
        "active_students": all_students.count() 
    }

    
    context = {
        "stats": dashboard_stats,
        "lessons": all_lessons[:5],  #next 5 lessons + recent 5 invoices
        "invoices": all_invoices[:5], 
        "tutor_name": "Zayan"
    }

    return render(request, "home.html", context)
def about(request):
    return render(request, "about.html")

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('home')  
    else:
        form = StudentForm()

    return render(request, 'add_student.html', {'form': form})