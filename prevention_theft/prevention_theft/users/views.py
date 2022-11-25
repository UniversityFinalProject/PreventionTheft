from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
from .forms import SignUpForm

def main(request):
    if request.method == 'GET':
        return render(request, 'users/main.html')
        # djangogram/templates/users/main.html 로 어딘가에 설정되어 있는 듯

    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        # authenticate는 DB에 저장할 수 있는 메소드임

        if user is not None:
            login(request, user)
            
            return HttpResponseRedirect(reverse('prevention_theft:main'))
            # return render(request, 'prevention_theft/index.html')
            # reverse 함수는 콜론을 이용해 페이지 이동
            # index는 prevention_theft/urls.py 에 있음 그냥 name은 다 urls 파일에 있음
        
        else:
            return render(request, 'users/main.html')

def signup(request):
    if request.method == 'GET':
        form = SignUpForm()
        return render(request, 'users/signup.html', {'form': form})
        

    elif request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('prevention_theft:main'))
            
        else:
            return render(request, 'users/main.html')