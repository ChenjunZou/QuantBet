from django.conf.urls import patterns, url

urlpatterns = patterns(
  '',
  url(r'^$', 'history.views.index', name='default'),
  url(r'^index$', 'history.views.index', name='index'),
)
