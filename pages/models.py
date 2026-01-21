from django.db import models


class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    parent_email = models.EmailField(blank=True, null=True)
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Invoice(models.Model):
    STATUS_CHOICES = [
        ('PAID', 'PAID'),
        ('PENDING', 'PENDING'),
        ('OVERDUE', 'OVERDUE'),
    ]
    
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"Invoice #{self.id} - {self.student}"