from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User


@csrf_exempt
def login(request):
    if request.method != "POST":
        return JsonResponse({"status": False, "message": "Invalid request method."}, status=400)

    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(username=username, password=password)

    if user is not None and user.is_active:
        auth_login(request, user)
        return JsonResponse(
            {
                "username": user.username,
                "status": True,
                "message": "Login successful!",
            },
            status=200,
        )

    return JsonResponse(
        {
            "status": False,
            "message": "Login failed, please check your username or password.",
        },
        status=401,
    )


@csrf_exempt
def register(request):
    if request.method != "POST":
        return JsonResponse({"status": False, "message": "Invalid request method."}, status=400)

    username = request.POST.get("username")
    password1 = request.POST.get("password1")
    password2 = request.POST.get("password2")

    if not username or not password1 or not password2:
        return JsonResponse({"status": False, "message": "All fields are required."}, status=400)

    if password1 != password2:
        return JsonResponse({"status": False, "message": "Passwords do not match."}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({"status": False, "message": "Username already exists."}, status=400)

    user = User.objects.create_user(username=username, password=password1)
    user.save()

    return JsonResponse(
        {
            "username": user.username,
            "status": True,
            "message": "User created successfully!",
        },
        status=200,
    )


@csrf_exempt
def logout(request):
    if request.method != "POST":
        return JsonResponse({"status": False, "message": "Invalid request method."}, status=400)

    auth_logout(request)
    return JsonResponse(
        {
            "status": True,
            "message": "Logout successful.",
        },
        status=200,
    )
