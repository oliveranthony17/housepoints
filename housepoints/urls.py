from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),

    path('houses/', views.houses, name='houses'),
    path('houses/details/<int:id>', views.houseDetails, name='house_details'),

    path('houses/create_house', views.createHouse, name="create_house"),
    path('houses/delete_house/<int:id>', views.deleteHouse, name="delete_house"),
    path('houses/update_house/<int:id>', views.updateHouse, name="update_house"),

    path('students/', views.students, name='students'),
    path('students/award_points/<int:id>', views.awardPoints, name='award_points'),

    path('students/create_student', views.createStudent, name="create_student"),
    path('students/update_student/<int:id>', views.updateStudent, name='update_student'),
    path('students/delete_student/<int:id>', views.deleteStudent, name="delete_student"),

    path('testing/', views.testing, name='testing'),
]
