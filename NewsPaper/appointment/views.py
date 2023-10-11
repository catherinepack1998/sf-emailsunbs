from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import send_mail
from datetime import datetime
from django.template.loader import render_to_string 
from django.core.mail import EmailMultiAlternatives
from .models import Appointment
 
class AppointmentView(View):
    template_name = 'appointment/make_appointment.html'
    def get(self, request, *args, **kwargs):
        return render(request, 'appointment/make_appointment.html', {})
 
    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()

        html_content = render_to_string( 
            'appointment/appointment_created.html',
            {
                'appointment': appointment,
            }
        )
 
        msg = EmailMultiAlternatives(
            subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
            body=appointment.message, #  это то же, что и message
            from_email='testpochta@ya.ru',
            to=['testpochta@ya.ru'], # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html") # добавляем html
        msg.send()
 
        return redirect('appointments:make_appointment')