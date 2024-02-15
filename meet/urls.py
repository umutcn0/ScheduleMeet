from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('handler/', csrf_exempt(views.MeetHandler.as_view())),
    path('handler/<str:id>/', csrf_exempt(views.MeetHandler.as_view())),
]
