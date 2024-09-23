from django.shortcuts import render

def home(request):
    template = loader.get_template("app/home.html")
    return HttpResponse(template.render({}, request))