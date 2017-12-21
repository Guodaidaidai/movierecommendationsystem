from django.conf.urls import url
from . import views
from . import views_zhang

urlpatterns=[
    url(r'^$',views.movie_list,name='movie_list'),
    url(r'^(?P<m_id>[0-9]+)/$',views.movie_info,name='movie_info'),
    url(r'^(?P<m_id>[0-9]+)/sentiment/$',views.sentiment_classify,name='sentiment_classify'),
    url(r'^home/$', views.index, name='home'),
    url(r'^login/$', views.logintest, name='login'),
    url(r'^assign/$', views.assign, name='assign'),
    url(r'^recommend/$', views.recommend, name='recommend'),
    url(r'^recommend/(.+)/$', views.recommend_type, name='recommend_type'),
    url(r'^hot_film/$', views.hot_film, name='hot_film'),  # 这个是优秀电影
    url(r'^hot_film/(.+)/$', views.hot_film_type, name='hot_film_type'),
    url(r'^shown_film/$', views.shown_film, name='shown_film'),
    url(r'^shown_film/(.+)/$', views.shown_film_type, name='shown_film_type'),
    url(r'^all/$', views.shown_film_all, name='shown_film_all'),
    url(r'^all/(.+)/$', views.shown_film_all_type, name='shown_film_all_type'),
    url(r'^personal_center/$', views.personal_center, name='personal_center'),
    url(r'^personal_setting/$', views.personal_setting, name='personal_setting'),
    url(r'^search/(.+)/$', views.search, name='search'),

]