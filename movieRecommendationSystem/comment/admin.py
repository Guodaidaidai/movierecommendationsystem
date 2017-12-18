from django.contrib import admin
from .models import MovieInfo, ShortComments, Sentimentclassify, User


# Register your models here.
class MovieInfoAdmin(admin.ModelAdmin):
    list_display = ('m_id', 'm_name', 'm_type', 'm_country', 'm_year', 'post_url')

#admin.site.unregister(MovieInfo)
admin.site.register(MovieInfo, MovieInfoAdmin)


class ShortCommentsAdmin(admin.ModelAdmin):
    list_display = ('c_id', 'm_id', 'comments', 'vote_num', 'time', 'u_id', 'star', 'sentiment')

#admin.site.unregister(ShortComments)
admin.site.register(ShortComments, ShortCommentsAdmin)


class SentimentclassifyAdmin(admin.ModelAdmin):
    list_display = ('m_id', 'index', 'bad_count', 'middle_count', 'good_count')

#admin.site.unregister(Sentimentclassify)
admin.site.register(Sentimentclassify, SentimentclassifyAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ('u_id', 'u_name', 'u_url')

#admin.site.unregister(User)
admin.site.register(User, UserAdmin)
