import logging
from django.shortcuts import render, render_to_response
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.template import RequestContext
import db_utils

logger = logging.getLogger("bet")


# Create your views here.
def football(request):
    samples = db_utils.get_all_football_game()[1:10]
    params = {'games': samples}
    return render_to_response("history/football.html", params, context_instance=RequestContext(request))

