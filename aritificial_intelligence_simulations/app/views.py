from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from . import forms
from .models import ContactUser
from django.core.mail import send_mail

class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "app/signup.html"

@login_required
def dashboard(request):
    return render(request, 'app/dashboard.html', {'title':'Dashboard'})


def ContactFormView(request):
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email_address = form.cleaned_data['email_address']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            s = ContactUser(name=name, email_address=email_address, subject=subject, message=message)
            s.save()

            if subject and message and email_address:
                try:
                    new_msg = f'Name: {name}\n Email:{email_address} \n Message:{message}.'
                    send_mail(subject, new_msg, email_address, ['simulations.ai@gmail.com'],fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
            return redirect("app-home")
    else:
        form = forms.ContactForm()
    return render(request, 'app/contact.html', {'form':form})

