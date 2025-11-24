from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse

def password(request):
    error = None
    if request.method == 'POST':
        password = request.POST.get('password')
        if password == '20080206':
            request.session['authenticated'] = True
            next_url = request.GET.get('next') or '/'
            return redirect(next_url)
        else:
            error = 'Incorrect password. Please try again.'
    return render(request, 'main/password.html', {'error': error})
