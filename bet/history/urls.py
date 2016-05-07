from django.conf.urls import patterns, url

urlpatterns = patterns(
  '',
  url(r'^$', 'history.views.history', name='default'),
  url(r'^history$', 'history.views.football', name='history'),
  url(r'^football$', 'history.views.football', name='history_football'),
  url(r'^basketball$', 'history.views.basketball', name='history_basketball'),

  url(r'^json/get_odds/(\w+)/$', 'history.views.json_get_football_odds'),
)
