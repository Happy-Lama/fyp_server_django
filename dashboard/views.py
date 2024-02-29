from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
# Create your views here.

class CustomLoginView(LoginView):
    success_url = reverse_lazy('home')

@login_required
def index(request):
    return render(request, 'dashboard/index.html')
