from django.contrib import auth
from django.shortcuts import render, HttpResponse, redirect, reverse
from score.forms import RegForm, ScoreRankForm, QueryForm
from score.models import ScoreRank, UserProfile
import redis
from utils.redis_pool import POOL
import json
from django.conf import settings
from collections import OrderedDict
from score import tools

CONN = redis.Redis(connection_pool=POOL)


def reg(request):
    form_obj = RegForm()
    if request.method == 'POST':
        form_obj = RegForm(request.POST)
        if form_obj.is_valid():
            obj = form_obj.save()
            obj.set_password(obj.password)
            obj.save()

            return redirect(reverse('score:login'))
    return render(request, 'score/reg.html', {'form_obj': form_obj})


def login(request):
    err_msg = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        pwd = request.POST.get('password')
        obj = auth.authenticate(request, username=username, password=pwd)
        if obj:
            auth.login(request, obj)
            return redirect(reverse('score:score_rank'))
        err_msg = '账号或者密码错误'
    return render(request, 'score/login.html', {'err_msg': err_msg})


# 查看排名
def score_rank(request):
    score_dict = tools.score_rank_c(request)
    if request.method == 'POST':
        query = request.POST.get('query')
        start, end = tools.query_dill(query)
        all_score = CONN.zrevrange(settings.SCORE_KEY, start-1, end-1, True)
        print(all_score)
        score_dict = tools.score_rank_c(request, start-1, end)

        print(score_dict)
    return render(request, 'score/score_table.html', {'score_dict': score_dict})


# 上传分数接口
def socre(request):
    obj = ScoreRank.objects.filter(customer=request.user).first()
    if not obj:
        obj = ScoreRank(customer=request.user)
    form_obj = ScoreRankForm(instance=obj)
    if request.method == 'POST':
        form_obj = ScoreRankForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            name = form_obj.cleaned_data.get('customer').name
            scor = form_obj.cleaned_data.get('score')
            CONN.zincrby(settings.SCORE_KEY, name, scor)
            return redirect(reverse('score:score_rank'))
    return render(request, 'score/score.html', {'form_obj': form_obj})


