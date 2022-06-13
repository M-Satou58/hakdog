from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.indexView, name='index'),

    path('register/teacher/', views.registerTeacherView, name='t-register'),
    path('register/student/', views.registerStudentView, name='s-register'),
    
    path('economy/', views.economyView, name='economy'),
    path('economy/active/<str:pk>/', views.setActive, name='set-active-economy'),
    path('economy/inactive/<str:pk>/', views.setInactive, name='set-inactive-economy'),

    path('settings/account/account-settings/', views.accountSettingsView, name='account-settings'),
    path('settings/school/school-settings/<str:user>/', views.schoolSettingsView, name='school-settings'),

    path('rules/jobs/<str:user>/', views.jobsView, name='jobs'),
    path('rules/jobs/update/<str:user>/<str:pk>/', views.updateJobsView, name='update-jobs'),
    path('rules/jobs/delete/<str:user>/<str:pk>/', views.deleteJobsView, name='delete-jobs'),


    path('rules/opportunities/<str:user>/', views.opportunitiesView, name='opportunities'),
    path('rules/opportunities/update/<str:user>/<str:pk>/', views.updateOpportunitiesView, name='update-opportunities'),
    path('rules/opportunities/delete/<str:user>/<str:pk>/', views.deleteOpportunitiesView, name='delete-opportunities'),

    path('rules/house-rules/<str:user>/', views.houseRulesView, name='house-rules'),
    path('rules/house-rules/update/<str:user>/<str:pk>/', views.updateHouseRulesView, name='update-house-rules'),
    path('rules/house-rules/delete/<str:user>/<str:pk>/', views.deleteHouseRulesView, name='delete-house-rules'),

    path('rules/rent/<str:user>/', views.rentView, name='rent'),

    path('monitoring/student/<str:user>/', views.studentMonitoringView, name='m-student'),

]