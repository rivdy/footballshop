from django.shortcuts import render

def show_home(request):
    context = {
        "app_name": "Garuda Football Shop",  
        "student_name": "Rivaldy Putra Rivly",  
        "student_class": "PBP B",               
    }
    return render(request, "home.html", context)
