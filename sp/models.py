from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from djmoney.models.fields import MoneyField

# Create your models here.

class Teacher(models.Model):
	last_name = models.CharField(max_length=200, null=True)
	first_name = models.CharField(max_length=200, null=True)
	middle_name = models.CharField(max_length=200, null=True)
	employee_id_no = models.CharField(max_length=200, null=True)
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	school_name = models.CharField(max_length=200, null=True)
	school_logo = models.ImageField(default='default_logo.jpg',null=True, blank=True)
	date_created = models.DateTimeField(default=timezone.now, null=True)
	def __str__(self):
		return f'{self.last_name} {self.first_name}'


class Student(models.Model):
	GRADE_LEVEL = (
    (0,"Kinder"),
    (1,"1")
	)

	last_name = models.CharField(max_length=200, null=True)
	first_name = models.CharField(max_length=200, null=True)
	middle_name = models.CharField(max_length=200, null=True)
	lrn = models.CharField(max_length=200, null=True)
	grade_level = models.IntegerField(choices=GRADE_LEVEL, default=0, null=True)
	section = models.CharField(max_length=200, null=True)
	date_created = models.DateTimeField(default=timezone.now, null=True)

	def __str__(self):
		return f'{self.last_name} {self.first_name}'

class StudentEconomy(models.Model):
	name = models.ForeignKey(Student, null=True, on_delete=models.CASCADE)
	teacher = models.CharField(max_length=200, null=True)
	jobs = models.CharField(max_length=200, null=True)
	spend = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='PHP',
        max_digits=11
    )
	salary = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='PHP',
        max_digits=11
    )    
	purchased = models.CharField(max_length=200, null=True)
	status = models.CharField(max_length=200, null=True)
	date_created = models.DateTimeField(default=timezone.now, null=True)
	def __str__(self):
		return f'{self.name.last_name} {self.name.first_name}'
	money = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='PHP',
        max_digits=11
    )
	

class Economy(models.Model):
	teacher = models.OneToOneField(Teacher, null=True, on_delete=models.CASCADE)
	student = models.ManyToManyField(StudentEconomy)



class Job(models.Model):
	teacher = models.CharField(max_length=200, null=True)
	job = models.CharField(max_length=200, null=True)
	suggested_per_class = models.CharField(max_length=200, null=True)
	job_description = models.TextField(max_length=1000, null=True)
	salary = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='PHP',
        max_digits=11
    )
	student_assigned = models.OneToOneField(StudentEconomy, null=True, on_delete=models.SET_NULL)
	date_created = models.DateTimeField(default=timezone.now, null=True)

	def __str__(self):
		return self.job

class Opportunitie(models.Model):
	teacher = models.CharField(max_length=200, null=True)
	activity = models.TextField(max_length=1000, null=True)
	amount = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='PHP',
        max_digits=11
    )
	date_created = models.DateTimeField(default=timezone.now, null=True)
	def __str__(self):
		return self.activity	

class HouseRule(models.Model):
	teacher = models.CharField(max_length=200, null=True)
	rule = models.TextField(max_length=1000, null=True)
	fine = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='PHP',
        max_digits=11
    )
	date_created = models.DateTimeField(default=timezone.now, null=True)
	def __str__(self):
		return self.rule

class Rent(models.Model):
	POSTING = (
    ("Daily","Daily"),
    ("Weekly","Weekly"),
    ("Bi-Weekly ","Bi-Weekly"),
    ("End Of Each Month","End Of Each Month"),
    ("Monthly","Monthly"),
	)
	teacher = models.CharField(max_length=200, null=True)
	start_date = models.DateField(null=True)
	end_date = models.DateField(null=True)
	posting = models.CharField(choices=POSTING, max_length=200, default=0, null=True)
	amount = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='PHP',
        max_digits=11)
	date_created = models.DateTimeField(default=timezone.now, null=True)
