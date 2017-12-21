from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from .models import *
from .recommend import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator


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
        username = req.POST.get('fullname', '')
        email = req.POST.get('account', '')
        password = req.POST.get('password', '')
        user = User.objects.create_user(username, email, password)
        user.save()
        return HttpResponseRedirect('/comment/login/')


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
    return render(req, '../templates/html/personal_center.html')


def personal_setting(req):
    return render(req, '../templates/html/setting.html')


def search(req, key):
    user = req.user
    movie = searchMovie(key)
    return render(req, '../templates/html/search_movie.html', {'movie': movie, 'user': user})
