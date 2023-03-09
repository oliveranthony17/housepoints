from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.homepage, name='homepage'),
    path('register/', views.register_request, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),

    path('houses/', views.houses, name='houses'),
    path('houses/details/<int:id>', views.houseDetails, name='house_details'),

    path('houses/create_house', views.createHouse, name="create_house"),
    path('houses/delete_house/<int:id>', views.deleteHouse, name="delete_house"),
    path('houses/update_house/<int:id>', views.updateHouse, name="update_house"),

    path('students/', views.students, name='students'),
    path('students_sort_by_points/', views.studentsSortByPoints, name='students_sort_by_points'),
    path('students_clear_points/', views.studentsClearPoints, name='students_clear_points'),
    path('students/students_award_all/', views.studentsAwardAll, name='students_award_all'),
    path('students/create_student', views.createStudent, name="create_student"),

    path('students/update_student/<int:id>', views.updateStudent, name='update_student'),
    path('students/delete_student/<int:id>', views.deleteStudent, name="delete_student"),
    path('students/award_points/<int:id>', views.awardPoints, name='award_points'),

    path('summary/', views.summary, name="summary"),

]
