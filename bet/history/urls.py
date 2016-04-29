from django.conf.urls import patterns, url

urlpatterns = patterns(
  '',
  url(r'^$', 'history.views.football', name='default'),
  url(r'^football$', 'history.views.football', name='football'),
  url(r'^json/get_odds/(\w+)/$', 'history.views.json_get_football_odds'),
)
