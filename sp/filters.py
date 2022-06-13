import django_filters
from django_filters import CharFilter

from .models import *

class TeacherFilter(django_filters.FilterSet):
	t_last_name = CharFilter(field_name='last_name', lookup_expr='icontains')
	t_first_name = CharFilter(field_name='first_name', lookup_expr='icontains')
	class Meta:
		model = Teacher
		fields = []
		
class StudentFilter(django_filters.FilterSet):
	s_last_name = CharFilter(field_name='last_name', lookup_expr='icontains')
	s_first_name = CharFilter(field_name='first_name', lookup_expr='icontains')
	class Meta:
		model = Student
		fields = []