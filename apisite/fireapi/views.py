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

def profile(request):

    return render(request, 'account/profile.html')

# def delete_user(request, username):
#     context = {}

#     try:
#         u = User.objects.get(username=username)
#         u.delete()
#         context['msg'] = 'The user is deleted.'       
#     except User.DoesNotExist: 
#         context['msg'] = 'User does not exist.'
#     except Exception as e: 
#         context['msg'] = e.message

#     return render(request, 'account/delete_account.html', context=context) 

