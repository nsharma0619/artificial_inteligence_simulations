from django.views import generic
from app.forms import ContactForm
from django.shortcuts import render


def HomeView(request):
    form = ContactForm()
    return render(request, 'app/app_home.html', {'title':'Home', 'form': form})