from django.db import models
from django.contrib.auth.models import User

# 1. Student Model
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    parent_email = models.EmailField(blank=True, null = True)
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# 2. Invoice Model
class Invoice(models.Model):
    STATUS_CHOICES = [
        ('PAID', 'Paid'),
        ('PENDING', 'Pending'),
        ('OVERDUE', 'Overdue'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"Invoice #{self.id} - {self.student}"


class Lesson(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    lesson_date = models.DateTimeField()
    notes = models.TextField(blank=True)

    # creates subfolder to help with organisation of files
    homework_file = models.FileField(upload_to='homework_files/', blank=True, null=True)

    def __str__(self):
        return f"{self.subject} with {self.student} on {self.lesson_date.strftime('%Y-%m-%d %H:%M')}"