from django.shortcuts import render

def index(request):

    return render(request, 'index.html')

def docs(request):

    return render(request, 'docs.html')

def dataproviders(request):

    return render(request, 'dataproviders.html')

def examples(request):

    return render(request, 'examples.html')

def getstarted(request):

    return render(request, 'getstarted.html')