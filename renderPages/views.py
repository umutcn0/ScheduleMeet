from django.shortcuts import render

def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

def create_meet(request):
    return render(request, 'meet/create_meet.html')

def edit_meet(request):
    return render(request, 'edit/edit_meet.html')