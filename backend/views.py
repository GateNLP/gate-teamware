import json
from django.http import JsonResponse, HttpRequest
from django.shortcuts import render
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









