from django.contrib.auth import views as auth_views
from django.urls import path
from .views import register, school_list,delete_school,edit_school, add_student, delete_student,school_detail,SchoolList, SchoolAPIView


urlpatterns = [ 
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/',register, name='register'),
    path('', school_list, name='school_list'),
    path('delete/<int:pk>/', delete_school, name='delete_school'),
    path('edit/<int:pk>/', edit_school, name='edit_school'),
    path('school/<int:school_id>/add_student/', add_student, name='add_student'),
    path('student/<int:student_id>/delete/', delete_student, name='delete_student'),
    path('school/<int:school_id>/',school_detail, name='school_detail'),
    #path('api/schools/', SchoolList.as_view(), name='school_list_api'),
    #path('api/schools/', school_list ,name='school_list_api'),
    path('api/schools/', SchoolAPIView.as_view(), name='school_list_create'),       
    path('api/schools/<int:school_id>/', SchoolAPIView.as_view(), name='school_detail')
]


