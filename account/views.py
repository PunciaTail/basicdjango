from django.shortcuts import render, redirect
from .models import UserModel
# 로그인 성공시 메시지 출력
from django.http import HttpResponse
# 사용자가 데이터베이스 안에 있는지 검사하는 함수
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# user의 signup.html을 화면에 보여주는 함수


def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'account/signup.html')
    elif request.method == 'POST':
        # username과 password는 필수이므로 None처리시 에러가 남
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        bio = request.POST.get('bio', '')

        if password != password2:
            # 패스워드가 같지 않다고 알람 (error부분)
            return render(request, 'account/signup.html', {'error': '패스워드를 확인 해 주세요'})
        else:
            if username == '' or password == '':
                return render(request, 'account/signup.html', {'error': '사용자 이름과 비번은 필수입니다'})

            id_duplicate_check = get_user_model().objects.filter(username=username)

            # id가 중복이라면 알람
            if id_duplicate_check:
                return render(request, 'account/signup.html', {'error': '사용자가 이미 존재합니다'})
            else:
                # DB에 저장하기
                UserModel.objects.create_user(
                    username=username, password=password, bio=bio)
                # 데이터가 저장된 후에 로그인 페이지로 넘어가기
                return redirect('/sign-in')


def sign_in_view(request):
    if request.method == 'POST':
        # 로그인도 에러 사항 고쳐주기
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        me = auth.authenticate(request, password=password, username=username)
        if me is not None:
            auth.login(request, me)
            return redirect('/')
        else:
            # 로그인 실패 시
            # redirect : 연결, render : 화면에 보여줌
            return render(request, 'account/signin.html', {'error': '유저이름 혹은 패스워드를 확인해주세요'})

    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'account/signin.html')


# 데코레이터 = 사용자가 로그인이 되어있어야 접근 가능한 함수
@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')
