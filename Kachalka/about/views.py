from django.shortcuts import render

# Create your views here.
def description(request):
    tempate = 'about/description.html'
    return render(request, tempate)