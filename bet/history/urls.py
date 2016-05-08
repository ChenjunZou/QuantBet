from django.conf.urls import patterns, url

urlpatterns = patterns(
  '',
  url(r'^$', 'history.views.football'),
  url(r'^football$', 'history.views.football', name='history_football'),
  url(r'^basketball$', 'history.views.basketball', name='history_basketball'),

  url(r'^json/football/get_details/(\w+)/$', 'history.views.json_get_football_odds'),
  url(r'^json/basketball/get_details/(\w+)/$', 'history.views.json_get_basketball_odds'),
)
