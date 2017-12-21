from .models import *
from math import sqrt
import datetime
import random

def loadShortComments() :
    result = ShortComments.objects.all().values_list('u_id','m_id','star')
    prefer = {}
    for item in result:
        (userId, movieId, rating) = item
        prefer.setdefault(userId, {})
        prefer[userId][movieId] = float(rating)
    return prefer

def loadOnshowMovie():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    string = str(year) + '-' + str(month)
    result = MovieInfo.objects.filter(m_year__contains=string)
    movieIds = list(result.values_list('m_id', flat=True))
    return movieIds

def loadMovies():
    result = list(MovieRating.objects.values_list('m_id', flat=True))
    return result

# 计算pearson相关度
def sim_pearson(prefer, person1, person2):
    sim = {}
    # 查找双方都评价过的项
    for item in prefer[person1]:
        if item in prefer[person2]:
            sim[item] = 1  # 将相同项添加到字典sim中
    # 元素个数
    n = len(sim)
    if len(sim) == 0:
        return -1

    # 所有偏好之和
    sum1 = sum([prefer[person1][item] for item in sim])
    sum2 = sum([prefer[person2][item] for item in sim])

    # 求平方和
    sum1Sq = sum([pow(prefer[person1][item], 2) for item in sim])
    sum2Sq = sum([pow(prefer[person2][item], 2) for item in sim])

    # 求乘积之和 ∑XiYi
    sumMulti = sum([prefer[person1][item] * prefer[person2][item] for item in sim])

    num1 = sumMulti - (sum1 * sum2 / n)
    num2 = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    # 如果分母为0，本处将返回0
    if num2 == 0:
        return 0

    result = num1 / num2
    return result


# 获取对item评分的K个最相似用户（K默认20）
def topKMatches(prefer, person, itemId, k=20, sim = sim_pearson):
    userSet = []
    scores = []
    users = []
    # 找出所有prefer中评价过Item的用户,存入userSet
    for user in prefer:
        if itemId in prefer[user]:
            userSet.append(user)
    # 计算相似性
    scores = [(sim(prefer, person, other),other) for other in userSet if other!=person]

    # 按相似度排序
    scores.sort()
    scores.reverse()

    if len(scores)<=k:       # 如果小于k，只选择这些做推荐
        for item in scores:
            users.append(item[1])  # 提取每项的userId
        return users
    else:                   # 如果>k,截取k个用户
        kscore = scores[0:k]
        for item in kscore:
            users.append(item[1])  # 提取每项的userId
        return users               # 返回K个最相似用户的ID

# 计算用户的平均评分
def getAverage(prefer, userId):
    count = 0
    sum = 0
    for item in prefer[userId]:
        sum = sum + prefer[userId][item]
        count = count + 1
    return sum / count


### 平均加权策略，预测userId对itemId的评分
def getRating(prefer1, userId, itemId, knumber=20, similarity=sim_pearson):
    sim = 0.0
    averageOther = 0.0
    weightAverage = 0.0
    simSums = 0.0
    # 获取K近邻用户(评过分的用户集)
    users = topKMatches(prefer1, userId, itemId, k=knumber, sim=sim_pearson)

    # 获取userId 的平均值
    averageOfUser = getAverage(prefer1, userId)

    # 计算每个用户的加权，预测
    for other in users:
        sim = similarity(prefer1, userId, other)  # 计算比较其他用户的相似度
        averageOther = getAverage(prefer1, other)  # 该用户的平均分
        # 累加
        simSums += abs(sim)  # 取绝对值
        weightAverage += (prefer1[other][itemId] - averageOther) * sim  # 累加，一些值为负

    # simSums为0，即该项目尚未被其他用户评分，这里的处理方法：返回用户平均分
    if simSums == 0:
        return averageOfUser
    else:
        return (averageOfUser + weightAverage / simSums)


def getUserOnshowRating(userId, k, movieIds):
    prefer = loadShortComments()
    movies = []
    if userId in prefer:
        scores = []
        hadComment = []
        for itemId in prefer[userId]:
            hadComment.append(itemId)
        for movieId in movieIds:
            if movieId not in hadComment:
                rating = getRating(prefer, userId, movieId, 20)
                scores.append((rating, movieId))
        scores.sort()
        scores.reverse()
        kscore = scores[0:k]
        for item in kscore:
            movies.append(MovieInfo.objects.get(m_id=item[1]))
    else:
        randomIds = random.sample(movieIds,k)
        for movieId in randomIds:
            movies.append(MovieInfo.objects.get(m_id=movieId))
    return movies

def loadGoodMovie(k,type):
    result = MovieRating.objects.order_by('-rating')
    movieIds = list(result.values_list('m_id', flat=True))
    movies = []
    if type=="全部":
        movieIds = movieIds[0:k]
        for item in movieIds:
            movies.append(MovieInfo.objects.get(m_id=item))
    else:
        n = 0
        for movieId in movieIds:
            m = MovieInfo.objects.get(m_id=movieId)
            if type in m.m_type:
                movies.append(m)
                n = n+1
            if n==k:
                break
    return movies

def searchMovie(key):
    result = MovieInfo.objects.filter(m_name__contains=key)
    return result

def type_select(type,scale):
    if scale == "热映":
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        string = str(year) + '-' + str(month)
        result = MovieInfo.objects.filter(m_year__contains=string, m_type__contains=type)
    else:
        result = MovieInfo.objects.filter(m_type__contains=type)
    movieIds = list(result.values_list('m_id', flat=True))
    return movieIds