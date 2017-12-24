import json
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from .models import *
from .recommend import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template import loader
from comment import  models
from django.core.paginator import Paginator
#批量注册用户
def user_data2user():
    data_list =models.User.objects.all()
    for data in data_list:
        user = User.objects.create_user('{}@admin.com'.format(data.u_id), '{}@admin.com'.format(data.u_id), '123456', first_name=data.u_name,last_name=data.u_image,id=int(data.u_id))
        user.save()
        user_pro =models.Profile(user=user, url=data.u_url)
        user_pro.save()
        print('创建用户{}'.format(data.u_name))
# Create your views here.
def movie_list(request):
    movies = MovieInfo.objects.all()
    return render(request, "../templates/movie/list.html", {'movies': movies})


def movie_info(request, m_id):
    movie = get_object_or_404(MovieInfo, m_id=m_id)
    return render(request, '../templates/movie/single_movie/info.html', {'movie': movie})


def sentiment_classify(request, m_id):
    if request.method == 'POST':
        key = request.POST.get('movie')
        return HttpResponseRedirect('/comment/search/%s' % key)
    else:
        user = request.user
        movie = get_object_or_404(MovieInfo, m_id=m_id)
        sentiment = get_object_or_404(Sentimentclassify, m=m_id)
        comments = ShortComments.objects.filter(m=m_id).first()
        return render(request, '../templates/html/single_film.html',
                      {'sentiment': sentiment, 'movie': movie, 'comments': comments, 'user': user})


def logintest(req):
    if req.method == 'GET':
        return render(req, '../templates/html/login.html', {'password_is_wrong': True})
    else:
        username = req.POST.get('account', '')
        password = req.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(req, user)
            return HttpResponseRedirect('/comment/home/')
        else:
            return render(req, '../templates/html/login.html', {'password_is_wrong': True})


@login_required
def index(req):
    return render(req, '../templates/index.html', )


def assign(req):
    if req.method == 'GET':
        return render(req, '../templates/html/assign.html')
    else:
        first_name = req.POST.get('fullname', '')
        username = req.POST.get('account', '')
        email = req.POST.get('account', '')
        password = req.POST.get('password', '')
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.save()

        return HttpResponseRedirect('/comment/login/')

@login_required
def recommend(req):
    if req.method == 'POST':
        key = req.POST.get('movie')
        return HttpResponseRedirect('/comment/search/%s' % key)
    else:
        user = req.user
        movieIds = loadMovies()
        movie = getUserOnshowRating(user.id, 100, movieIds)
        limit = 20
        paginatior = Paginator(movie, limit)
        page = req.GET.get('page', 1)
        loaded = paginatior.page(page)
        return render(req, '../templates/html/recommanding_film.html', {'movie': loaded, 'user': user})


def recommend_type(req, type):
    if req.method == 'POST':
        key = req.POST.get('movie')
        return HttpResponseRedirect('/comment/search/%s' % key)
    else:
        user = req.user
        movieIds = type_select(type, "全部")
        movie = getUserOnshowRating(user.id, 60, movieIds)
        limit = 20
        paginatior = Paginator(movie, limit)
        page = req.GET.get('page', 1)
        loaded = paginatior.page(page)
        return render(req, '../templates/html/recommanding_film.html', {'movie': loaded, 'user': user})


def hot_film(req):  # 优秀电影
    if req.method == 'POST':
        key = req.POST.get('movie')
        return HttpResponseRedirect('/comment/search/%s' % key)
    else:
        user = req.user
        movie = loadGoodMovie(100, "全部")
        limit = 20
        paginatior = Paginator(movie, limit)
        page = req.GET.get('page', 1)
        loaded = paginatior.page(page)
        return render(req, '../templates/html/hot_flim.html', {'movie': loaded, 'user': user})


def hot_film_type(req, type):
    if req.method == 'POST':
        key = req.POST.get('movie')
        return HttpResponseRedirect('/comment/search/%s' % key)
    else:
        user = req.user
        movie = loadGoodMovie(60, type)
        limit = 20
        paginatior = Paginator(movie, limit)
        page = req.GET.get('page', 1)
        loaded = paginatior.page(page)
        return render(req, '../templates/html/hot_flim.html', {'movie': loaded, 'user': user})


def shown_film(req):  # 热映电影
    if req.method == 'POST':
        key = req.POST.get('movie')
        return HttpResponseRedirect('/comment/search/%s' % key)
    else:
        user = req.user
        movieIds = loadOnshowMovie()
        movie = getUserOnshowRating(user.id, 60, movieIds)
        limit = 20
        paginatior = Paginator(movie, limit)
        page = req.GET.get('page', 1)
        loaded = paginatior.page(page)
        return render(req, '../templates/html/shown_film.html', {'movie': loaded, 'user': user, 'top': "/shown_film/"})


def shown_film_all(req):
    if req.method == 'POST':
        key = req.POST.get('movie')
        return HttpResponseRedirect('/comment/search/%s' % key)
    else:
        user = req.user
        movieIds = loadOnshowMovie()
        movie = []
        for id in movieIds:
            movie.append(MovieInfo.objects.get(m_id=id))
        limit = 20
        paginatior = Paginator(movie, limit)
        page = req.GET.get('page', 1)
        loaded = paginatior.page(page)
    return render(req, '../templates/html/shown_film.html', {'movie': loaded, 'user': user, 'top': "/all/"})


def shown_film_type(req, type):
    if req.method == 'POST':
        key = req.POST.get('movie')
        return HttpResponseRedirect('/comment/search/%s' % key)
    else:
        user = req.user
        top = "/shown_film/"
        movieIds = type_select(type, "热映")
        movie = getUserOnshowRating(user.id, 60, movieIds)
        limit = 20
        paginatior = Paginator(movie, limit)
        page = req.GET.get('page', 1)
        loaded = paginatior.page(page)
    return render(req, '../templates/html/shown_film.html', {'movie': loaded, 'user': user, 'top': top})


def shown_film_all_type(req, type):
    if req.method == 'POST':
        key = req.POST.get('movie')
        return HttpResponseRedirect('/comment/search/%s' % key)
    else:
        user = req.user
        movieIds = type_select(type, "热映")
        movie = []
        for id in movieIds:
            movie.append(MovieInfo.objects.get(m_id=id))
        limit = 20
        paginatior = Paginator(movie, limit)
        page = req.GET.get('page', 1)
        loaded = paginatior.page(page)
        return render(req, '../templates/html/shown_film.html', {'movie': loaded, 'user': user, 'top': "/all/"})


def personal_center(req):
    if req.method == 'POST':
        key = req.POST.get('movie')
        return HttpResponseRedirect('/comment/search/%s' % key)
    else:
        user = req.user
        movie_history = ShortComments.objects.filter(u_id=user.id)
        movie_history_list = []
        movie_collect_list = []
        for u in UCollect.objects.filter(u_id=user.id):
            movie_collect_list.append(MovieInfo.objects.filter(m_id=u.m_id)[0])
        for movie in movie_history:
            movie_history_list.append(MovieInfo.objects.filter(m_id=movie.m_id)[0])

        return render(req, '../templates/html/personal_center.html',{"movie_history_list": movie_history_list, "movie_collect_list": movie_collect_list})

def personal_setting(req):
    user=req.user
    return render(req, '../templates/html/setting.html',{'user':user})


def search(req, key):
    if req.method == 'POST':
        key = req.POST.get('movie')
        return HttpResponseRedirect('/comment/search/%s' % key)
    else:
        user = req.user
        movie = searchMovie(key)
        limit = 20
        paginatior = Paginator(movie, limit)
        page = req.GET.get('page', 1)
        loaded = paginatior.page(page)
        return render(req, '../templates/html/search_movie.html', {'movie': loaded, 'user': user})


@csrf_exempt
def add_user_collect(request):
    print("用户手册")
    """用户收藏"""
    for key in ('m_id','u_id' ):
        if key not in request.POST:
            msg = json.dumps({'msgcode': 0, 'errmsg': '{}数据缺失'.format(key)}, ensure_ascii=False)
            return HttpResponse(msg, content_type="application/json")
    #获取参数
    m_id = request.POST['m_id']
    u_id = request.POST['m_id']
    print('收藏')

    # 处理用户收藏
    collect_ob, created = models.UCollect.objects.get_or_create(m_id=m_id, u_id=u_id)
    if not created:
        msg = json.dumps({'msgcode': 0, 'errmsg': '已收藏过'}, ensure_ascii=False)
    else:
        msg = json.dumps({'msgcode': 1, 'errmsg': '收藏success'}, ensure_ascii=False)
    return HttpResponse(msg, content_type="application/json")
@csrf_exempt
def change_user_info(request):
    print("改变信息")

    for key in ('name1','email','u_id'):
        print("comem")
        if key not in request.POST:
            msg = json.dumps({'msgcode': 0, 'errmsg': '{}数据缺失'.format(key)}, ensure_ascii=False)
            return HttpResponse(msg, content_type="application/json")
    #获取参数
    name1 = request.POST['name1']
    print(name1)
    email = request.POST['email']
    request.user.email = email
    print(request.user.first_name)
    request.user.first_name = name1
    request.user.save()
    print(request.user.first_name)

    msg = json.dumps({'msgcode': 1, 'errmsg': '修改个人信息成功'}, ensure_ascii=False)
    return HttpResponse(msg, content_type="application/json")