from django.shortcuts import render
from datetime import datetime

def index(request):
    return render(request, "main_app/index.html")


def logInUser(request):
    context={
        "today": datetime.today().year
    }
    return render(request, "main_app/login.html",context)
