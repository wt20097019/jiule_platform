# coding=utf8


from django.conf.urls import url, include

from demo import urls as demo_urls

from demo import frontend_views, backend_views
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^$', frontend_views.IndexView.as_view()),
    url(r'^frontend_charts_list/$', frontend_views.FrontendEchartsTemplate.as_view()),
    url('^backend_charts_list/$', backend_views.BackendEChartsTemplate.as_view()),

    url(r'options/simpleBar/', frontend_views.SimpleBarView.as_view()),
    url(r'options/simpleKLine/', frontend_views.SimpleKLineView.as_view()),
    url(r'options/simpleData/', frontend_views.SimpleDataView.as_view()),
    url(r'options/simpleData1/', frontend_views.SimpleData1View.as_view()),
    url(r'options/simpleListUp/', frontend_views.SimpleListUpView.as_view()),
    url(r'options/simpleListDn/', frontend_views.SimpleListDnView.as_view()),
    url(r'options/simpleRate/', frontend_views.SimpleRateView.as_view()),
    url(r'options/simpleMap/', frontend_views.SimpleMapView.as_view()),
    url(r'options/simplePie/', frontend_views.SimplePieView.as_view()),
    url(r'page_demo/', backend_views.PageDemoView.as_view()),
    url(r'^login/$', frontend_views.login),
    url(r'^choose/$', frontend_views.choose),
    #url(r'^static/$', frontend_views.static),
    url(r'^show/$', frontend_views.show),

]
