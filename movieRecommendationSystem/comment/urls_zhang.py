from django.conf.urls import url
from . import views
from . import views_zhang

app_name="zhang"
urlpatterns=[
       ###zhang############
    url(r'^(?P<m_id>[0-9]+)/detail/$',views_zhang.movie_detail,name='detail'),
    url(r'^(?P<m_id>[0-9]+)/resource/$',views_zhang.movie_resources,name='resource'),
    url(r'^(?P<m_id>[0-9]+)/(?P<lon>[0-9]+.?[0-9]+)/(?P<lat>[0-9]+.?[0-9]+)/price/$',views_zhang.movie_price,name='price'),
    url(r'^ajax/price_in_cinema/$',views_zhang.ajax_price,name="ajax_price"),
    url(r'^$',views_zhang.index,name='index'),
    ###zhang############

]