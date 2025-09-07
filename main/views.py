from django.shortcuts import render

def show_home(request):
    return render(request, "home.html", {
        "app_name": "Garuda Merah Putih Football Shop",
        "student_name": "Rivaldy Putra Rivly",
        "student_class": "PBP B",
    })
