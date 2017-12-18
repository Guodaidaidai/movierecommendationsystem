from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$',views.movie_list,name='movie_list'),
    url(r'^(?P<m_id>[0-9]+)/$',views.movie_info,name='movie_info'),
    url(r'^(?P<m_id>[0-9]+)/sentiment/$',views.sentiment_classify,name='sentiment_classify'),
]