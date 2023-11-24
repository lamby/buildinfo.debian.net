from django.shortcuts import render

def landing(request):
    return render(request, 'static/landing.html')
