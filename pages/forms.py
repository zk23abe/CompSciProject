from django import forms
from .models import Student, Invoice, Lesson

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'parent_email']
        
        #styling
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'parent_email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class InvoiceForm(forms.ModelForm):
    class Meta: 
        model = Invoice
        fields = ['student' , 'amount', 'due_date', 'status']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lessonfieds = ['student', 'subject', 'lesson_date','notes']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'lesson_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }