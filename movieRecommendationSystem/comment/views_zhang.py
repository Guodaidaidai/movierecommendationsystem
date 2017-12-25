from django.shortcuts import render,get_object_or_404,get_list_or_404
from django.http import HttpResponse,Http404,JsonResponse
from .models import MovieInfo,movie_resource,cinema_info,price_info
import json
from django.core.serializers.json import DjangoJSONEncoder
from math import sin,cos,sqrt,atan2,radians
import decimal

from django.core import serializers
import datetime
# Create your views here.

def index(request):
    return HttpResponse("Hello,world.Your're at the index view")

def movie_detail(request,m_id):
    movie=get_object_or_404(MovieInfo,pk=m_id)
    return render(request,'../templates/zhang/movie_detail.html',{'movie':movie})

def movie_resources(request,m_id):
    try:
        resources=get_list_or_404(movie_resource,movie__m_id=m_id)
        return render(request, '../templates/zhang/movie_resource.html', {'resources': resources})
    except Exception as e:
        message='这个电影暂时没有资源呢'
        print(e)
    return render(request, '../templates/zhang/movie_resource.html', {'message': message})

def ajax_price(request):
    c_id=request.GET.get("c_id")
    m_id=request.GET.get("m_id")
    date=request.GET.get("date")
    first=request.GET.get("first")
    dates=[]
    try:
        print("i am here........")
        print(m_id)
        print(c_id)
        print(date)
        print(first)
        prices = list(get_list_or_404(price_info, cinema__c_id=c_id,#找到这家影院该电影所有的排片信息
                                      movie__m_id=m_id))
        dates = get_dates(prices)  # 找到这家影院全部的日期
        if first==0:
            date=dates[0]
        print(dates)
        print("after find the movies in the cinema .........")
        #这个是获取到这一天的票价信息
        prices_today=list(get_list_or_404(price_info,cinema__c_id=c_id,movie__m_id=m_id,date=date))
        prices_today=sort_prices(prices_today)
        #这里需要对这个票价按照时间进行排序
        return HttpResponse(json.dumps({'prices':serializers.serialize('json',prices_today),'dates':dates}))
    except Exception as e:
        print("error:"+str(e))
        message="暂时没有拍片信息噢"
        return HttpResponse(json.dumps({'message':message,'dates':dates}))

def get_dates(prices):
    dates=[]
    i = datetime.datetime.now()
    month = i.month
    day = i.day
    today_date = str(month) + "月" + str(day) + "日"
    for price in prices:
        if price.date not in dates and price.date>=today_date:
            dates.append(price.date)


    dates=sorted(dates)
    return dates
def sort_prices(prices):
    return sorted(prices,key=lambda price:price.start_time )

def get_distance(lon1,lon2,lat1,lat2):
    R=6373.0
    #print(lon1+" "+str(lon2)+" "+lat1+" "+str(lat2))
    lon1=float(lon1)
    lon2=float(lon2)
    lat1=float(lat1)
    lat2=float(lat2)

    dlon=lon1-lon2
    dlat=lat1-lat2
    a=sin(dlat/2)**2+cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c=2*atan2(sqrt(a),sqrt(1-a))
    distance=R*c
    return distance

def sort_cinema(cinemas,lon,lat):
    return sorted(cinemas,key=lambda cinema:get_distance(lon,cinema.longitude,lat,cinema.latitude))

def get_distances(cinemas,lon,lat):
    dises=[]
    for cinema in cinemas:
        if cinema.longitude=="" or cinema.latitude=="":
            continue
        dis=get_distance(lon,cinema.longitude,lat,cinema.latitude)
        dises.append(str(int(dis))+"米")
    return dises

def movie_price(request,m_id,lon,lat):
    print(str(lon+lat))
    #area = "普陀区"#这里需要找到离用户最近影院
    cinemas=[]
    dis=[]
    movie=None
    dates=[]
    user = request.user
    print(movie)
    #这里需要对影院的根据远近进行排序
    try:
        if lon=="0.0":#未获取到地理位置
            cinemas=list(get_list_or_404(cinema_info,area="普陀区"))#未能获取位置信息
        else:
            cinemas = list(get_list_or_404(cinema_info))
            cinemas = sort_cinema(cinemas, lon, lat)  # 对电影院进行排序
            dis = get_distances(cinemas, lon, lat)

        movie = get_object_or_404(MovieInfo, pk=m_id)
        near_cinema = cinemas[0]  # 找到最近的电影院



        prices = list(get_list_or_404(price_info, cinema__c_id=near_cinema.c_id,
                                      movie__m_id=m_id))
        dates = get_dates(prices)  # 找到这家影院全部的日期
        prices_today = list(get_list_or_404(price_info, cinema__c_id=near_cinema.c_id,
                                            movie__m_id=m_id, date=dates[0]))
        prices_today = sort_prices(prices_today)  # 对票价进行排序

        return render(request, '../templates/html/cinema_comparing.html',
                      {'user':user,'cinema_dis_list': serializers.serialize('json', cinemas),
                       'm_id': m_id, 'movie': movie, 'dates': dates, 'dis': dis,
                       'prices': serializers.serialize('json', prices_today)})


    except Exception as e:

        print("error:"+str(e))
        print(dis)
        message="暂时没有拍片信息噢"
        return render(request, '../templates/html/cinema_comparing.html', {'cinema_dis_list':serializers.serialize('json',cinemas),
                                                      'm_id':m_id,'movie':movie,'dates':dates,'dis':dis,
                                                      'message': message,'prices':[]})








