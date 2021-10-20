from django.conf import settings
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
        context = {
            "settings": settings
        }


        return render(request, self.template_page, context=context)
