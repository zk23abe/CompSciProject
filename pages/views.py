from django.shortcuts import render

def home(request):

    dashboard_stats = {
        "total_students" : 15,
        "active_students" : 12,
        "pending_invoices" : 3,

    }
    #simulate timetable
    upcoming_lessons = [
        {"student": "Sarah Jones", "subject": "GCSE Math", "time": "16:00 Today"},
        {"student": "Mike Ross", "subject": "A-Level Physics", "time": "17:30 Today"},
        {"student": "John Doe", "subject": "GCSE English", "time": "10:00 Tomorrow"},
    ]

    #simulate payments and cash flow management
    recent_invoices = [
        {"id": "INV001", "student": "Sarah Jones", "amount": "£45.00", "status": "Paid"},
        {"id": "INV002", "student": "Mike Ross", "amount": "£60.00", "status": "Pending"},
    ]

    
    context = {
        "stats": dashboard_stats,
        "lessons": upcoming_lessons,
        "invoices": recent_invoices,
        "tutor_name": "Zayan" 
    }

    return render(request, "home.html", context)

def about(request):
    return render(request, "about.html")

