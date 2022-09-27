from django.shortcuts import render

# Create your views here.

def info(request):

    return render(request, 'profile/info.html', {})

def charts(request):

    return render(request, 'profile/charts.html', {})

