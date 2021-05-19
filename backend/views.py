from django.contrib.auth import authenticate, get_user_model, login as djlogin, logout as djlogout
from django.http import JsonResponse, HttpRequest
from django.shortcuts import redirect, render
from django.views import View


class MainView(View):
    """
    The main view of the app (index page)
    """

    template_page = "base-vue.html"


    def get(self, request, *args, **kwargs):
        """
        :param request:
        :return:
        """
        context = {}

        return render(request, self.template_page, context=context)


def login(request):
    context = {}
    if "username" in request.POST and "password" in request.POST:
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if user is not None:
            djlogin(request, user)
            return redirect("/")
        else:
            context["error"] = "Invalid username or password."

    return render(request, "login.html", context)


def logout(request):
    djlogout(request)
    return redirect("/")


def register(request):
    context = {}
    if "username" in request.POST and "password" in request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]

        if not get_user_model().objects.filter(username=username).exists():
            user = get_user_model().objects.create_user(username=username, password=password, email=email)
            djlogin(request, user)
            return redirect("/")
        else:
            context["error"] = "Username already exists"
        # User.objects.get()
        # print("User created!")

    return render(request, "register.html", context=context)