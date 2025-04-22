from django.shortcuts import render
from django.http import HttpResponse
import mysql.connector
# Create your views here.
def index(request):
    
    return render(request,"index.html")
def registration(request):
    
    return render(request,"registration.html")
def login(request):
    
    return render(request,"login.html")
def about(request):
    
    return render(request,"about.html")
def events(request):
    
    return render(request,"events.html")
def contact(request):
    
    return render(request,"contact.html")