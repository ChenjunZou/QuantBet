from django.conf.urls import patterns, url

urlpatterns = patterns(
  '',
  url(r'^$', 'history.views.football', name='default'),
  url(r'^football$', 'history.views.football', name='football'),
)
