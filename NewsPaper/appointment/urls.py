from django.urls import path
# from django.contrib.auth.views import LoginView, LogoutView
from .views import AppointmentView

app_name = 'appointment'
urlpatterns = [
    path('make_appointment', AppointmentView.as_view(), name='make_appointment')
]
