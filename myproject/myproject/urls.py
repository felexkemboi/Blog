
from django.conf.urls import url
from django.contrib import admin

from boards import views
from accounts import views as accounts_views

urlpatterns = [
    url(r'^$', views.home,name='home'),
    url(r'^signup/$', accounts_views.signup,name='signup'),
    url(r'^boards/(?P<pk>\d+)/$',views.board_topics, name='board_topics'),
    url(r'^boards/(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),
    url(r'^admin/', admin.site.urls),

]
