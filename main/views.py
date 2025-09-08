from django.shortcuts import render

def show_home(request):
    context = {
        "app_name": "Garuda Football Shop",  # ganti tema kecilmu
        "student_name": "Rivaldy Putra Rivly",  # ganti sesuai
        "student_class": "PBP A",               # ganti sesuai
    }
    return render(request, "home.html", context)
