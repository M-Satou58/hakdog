from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import *
from .filters import *

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.conf import settings

# Create your views here.
def indexView(request):
	context = {}
	return render(request, 'main/index01.html', context)

def registerTeacherView(request):
	if request.method == 'POST':
		teacher_form = RegisterTeacherForm(request.POST)
		teacher_form01 = RegisterTeacherForm01(request.POST)
		if teacher_form.is_valid() and teacher_form01.is_valid():
			teacher_form01.save()
			teacher_form.save()
			username = teacher_form01.cleaned_data['username']
			t = Teacher.objects.last()
			u = User.objects.last()
			t.user = u
			t.save()
			messages.success(request, f'{username} created successfully!')
			return redirect('/register/teacher')
		else:
			messages.error(request, f'Please fill up the form correctly')
	teacher_form = RegisterTeacherForm()
	teacher_form01 = RegisterTeacherForm01()
	context = {'teacher_form':teacher_form, 'teacher_form01':teacher_form01}
	return render(request, 'registration/teacher-registration-form.html', context)

def registerStudentView(request,):
	if request.method == 'POST':
		form = RegisterStudentForm(request.POST)
		if form.is_valid():
			last_name = form.cleaned_data['last_name']
			first_name = form.cleaned_data['first_name']
			form.save()
			messages.success(request, f'{last_name} {first_name} has been registered successfully.')
			return redirect('/register/student/')

	form = RegisterStudentForm()
	context = {'form':form}		
	return render(request, 'registration/student-registration-form.html', context)

def economyView(request):
	e = Economy.objects.all()

	if request.method == 'POST':
		form = EconomyForm(request.POST)
		if form.is_valid():
			teacher = form.cleaned_data['teacher']
			student = form.cleaned_data['student']


			print('Valid form')
			if Economy.objects.filter(teacher=teacher):
				e = Economy.objects.get(teacher=teacher)
				print('Teacher already exists')
			else:
				print('Teacher added')
				Economy(teacher=teacher).save()
				e = Economy.objects.get(teacher=teacher)
			sid = student.values_list('id', flat=True)
			print(f'sid: {sid.all()}')
			for i in sid.all():
				print(f'Loop {i}')
				if StudentEconomy.objects.filter(name=student.get(id=i), teacher=teacher):
					print('Student already exists')
				else:
					StudentEconomy(name=student.get(id=i), teacher=teacher).save()
					se = StudentEconomy.objects.get(name=student.get(id=i), teacher=teacher)
					se.status='Active'
					se.save()
					print(se.status)
					e.student.add(StudentEconomy.objects.get(name=student.get(id=i), teacher=teacher))
					e.save()
					print('Student Added')
			return redirect('/economy/')
		else:
			print('invalid form')

	form = EconomyForm()
	context = {'form':form, 'e':e}
	return render(request, 'economy/economy.html', context)

def setActive(request, pk):
	se = StudentEconomy.objects.get(id=pk)
	se.status = 'Active'
	se.save()
	messages.success(request, f'{se.name} set to active')
	return redirect('/economy/')

def setInactive(request, pk):
	se = StudentEconomy.objects.get(id=pk)
	se.status = 'Inactive'
	se.save()
	print(f'Nam: {se.name}')
	print(f'Status {se.status}')
	messages.success(request, f'{se.name} set to inactive')
	return redirect('/economy/')

def accountSettingsView(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)
			messages.success(request, 'Your password was successfully updated!')
			return redirect('/')
		else:
			messages.error(request, 'Please correct the error below.')
	form = PasswordChangeForm(request.user)
	context = {'form':form}
	return render(request, 'settings/account/account-settings.html', context)

def schoolSettingsView(request, user):
	t = Teacher.objects.get(user=user)
	if request.method == 'POST':
		form = SchoolSettingsForm(request.POST, request.FILES)
		if form.is_valid():
			school_name = form.cleaned_data['school_name']
			school_logo = form.cleaned_data['school_logo']
			t.school_name = school_name
			t.school_logo = school_logo
			t.save()
			messages.success(request, 'School Settings successfully updated!')
			return redirect('/')

	form = SchoolSettingsForm()
	context = {'form':form}
	return render(request, 'settings/school/school-settings.html', context)

def jobsView(request, user):
	teacher = Teacher.objects.get(user=user)
	if request.method == 'POST':
		form = CreateJobsForm(teacher,request.POST)
		if form.is_valid():
			print('form is valid')
			job = form.cleaned_data['job']
			suggested_per_class = form.cleaned_data['suggested_per_class']
			job_description = form.cleaned_data['job_description']
			salary = form.cleaned_data['salary']
			student_assigned = form.cleaned_data['student_assigned']

			s = StudentEconomy.objects.get(name=student_assigned.name.id, teacher=teacher)
			Job(teacher=teacher, job=job, suggested_per_class=suggested_per_class, job_description=job_description, salary=salary, student_assigned=s).save()
			print('Job Created')

			s.jobs = job
			s.salary = salary
			s.save()

			messages.success(request, 'Job added successfully!')
			print(f'Jobs: {s.jobs} Salary:')
			print('Job Success')
			
		else:
			messages.success(request, 'Student Already has a job!')

	
	student = StudentEconomy.objects.filter(teacher=teacher)
	j = Job.objects.filter(teacher=teacher)
	form = CreateJobsForm(teacher)
	context = {'form':form, 'j':j}
	return render(request, 'rules/jobs/jobs.html', context)


def updateJobsView(request, user, pk):
	jobs = Job.objects.get(id=pk)
	teacher = Teacher.objects.get(user=user)

	form = UpdateJobsForm()
	if request.method == 'POST':
		form = UpdateJobsForm(request.POST)
		if form.is_valid():
			print('Form is valid')
			job = form.cleaned_data['job']
			suggested_per_class = form.cleaned_data['suggested_per_class']
			salary = form.cleaned_data['salary']
			job_description = form.cleaned_data['job_description']

			jobs.job = job
			jobs.suggested_per_class = suggested_per_class
			jobs.salary = salary
			jobs.job_description = job_description
			jobs.save()

			s = StudentEconomy.objects.get(name=jobs.student_assigned.name)
			s.jobs = job
			s.salary = salary
			print(f'Student" {s}')
			print(s.jobs)
			print(s.salary)
			s.save()




			messages.success(request, 'Jobs successfully updated!')
			return redirect(f'/rules/jobs/{user}/')

		else:
			print('Invalid Form')
	
	context = {'form':form,'jobs':jobs}
	return render(request, 'rules/jobs/update-jobs.html', context)


def deleteJobsView(request, user, pk):
	jobs = Job.objects.get(id=pk)
	se = StudentEconomy.objects.get(name=jobs.student_assigned.name)
	if request.method == 'POST':
		se.jobs = ''
		se.salary = 0
		se.save()
		jobs.delete()
		messages.success(request, 'Job successfully deleted!')
		return redirect(f'/rules/jobs/{user}/')
	context = {'jobs':jobs}
	return render(request, 'rules/jobs/delete-jobs.html', context)


def opportunitiesView(request, user):
	teacher = Teacher.objects.get(user=user)
	if request.method == 'POST':
		form = CreateOpportunitiesForm(request.POST)
		if form.is_valid():
			activity = form.cleaned_data['activity']
			amount = form.cleaned_data['amount']
			Opportunitie(teacher=teacher, activity=activity, amount=amount).save()
			messages.success(request, 'Opportunities successfully added!')
			return redirect(f'/rules/opportunities/{user}/')

	opportunities = Opportunitie.objects.filter(teacher=teacher)
	form = CreateOpportunitiesForm()
	context = {'form':form, 'opportunities':opportunities}
	return render(request, 'rules/opportunities/opportunities.html', context)


def updateOpportunitiesView(request, user, pk):
	opportunities = Opportunitie.objects.get(id=pk)
	form = CreateOpportunitiesForm(instance=opportunities)
	if request.method == 'POST':
		form = CreateOpportunitiesForm(request.POST, instance=opportunities)
		if form.is_valid():
			form.save()
			messages.success(request, f'{opportunities.activity} successfully updated!')
			return redirect(f'/rules/opportunities/{user}')

	context = {'form':form, 'opportunities':opportunities}
	return render(request, 'rules/opportunities/update-opportunities.html', context)

def deleteOpportunitiesView(request, user, pk):
	opportunities = Opportunitie.objects.get(id=pk)
	if request.method == 'POST':
		opportunities.delete()
		messages.success(request, f'{opportunities.activity} successfully deleted!')
		return redirect(f'/rules/opportunities/{user}/')
	context = {'opportunities':opportunities}
	return render(request, 'rules/opportunities/delete-opportunities.html', context)

def houseRulesView(request, user):
	teacher = Teacher.objects.get(user=user)
	if request.method == 'POST':
		form = CreateHouseRulesForm(request.POST)
		if form.is_valid():
			rule = form.cleaned_data['rule']
			fine = form.cleaned_data['fine']

			HouseRule(teacher=teacher, rule=rule, fine=fine).save()
			messages.success(request, 'House Rules successfully added!')
			return redirect(f'/rules/house-rules/{user}/')

	h = HouseRule.objects.filter(teacher=teacher)
	form = CreateHouseRulesForm()
	context = {'form':form, 'h':h}
	return render(request, 'rules/house-rules/house-rules.html', context)


def updateHouseRulesView(request, user, pk):
	h = HouseRule.objects.get(id=pk)
	form = CreateHouseRulesForm(instance=h)
	if request.method == 'POST':
		form = CreateHouseRulesForm(request.POST, instance=h)
		if form.is_valid():
			form.save()
			messages.success(request, f'{h.rule} successfully updated!')
			return redirect(f'/rules/house-rules/{user}/')

	context = {'form':form, 'h':h}
	return render(request, 'rules/house-rules/update-house-rules.html', context)

def deleteHouseRulesView(request, user, pk):
	h = HouseRule.objects.get(id=pk)
	if request.method == 'POST':
		h.delete()
		messages.success(request, f'{h.rule} successfully deleted!')
		return redirect(f'/rules/house-rules/{user}')
	context = {'h':h}
	return render(request, 'rules/house-rules/delete-house-rules.html', context)


def rentView(request, user):
	teacher = Teacher.objects.get(user=user)
	if request.method == 'POST':
		form = RentForm(request.POST)
		if form.is_valid():
			sdate = form.cleaned_data['sdate']
			edate = form.cleaned_data['edate']
			posting = form.cleaned_data['posting']
			amount = form.cleaned_data['amount']
			Rent(teacher=teacher, start_date=sdate, end_date=edate, posting=posting, amount=amount).save()
			
			se = StudentEconomy.objects.all().filter(teacher=teacher)

			for i in se:
				i.money = i.money - amount
				i.save()
				print('Rent Success')

			messages.success(request, 'Rent added successfully!')
			return redirect(f'/rules/rent/{user}')
		else:
			messages.error(request, 'Please fill up the form correctly')
			return redirect(f'/rules/rent/{user}')
	form = RentForm()
	context = {'form':form}
	return render(request, 'rules/rent/rent.html', context)


def studentMonitoringView(request, user):
	teacher = Teacher.objects.get(user=user)
	se = StudentEconomy.objects.filter(teacher=teacher)
	context = {'se':se}
	return render(request, 'monitoring/student/student.html', context)

