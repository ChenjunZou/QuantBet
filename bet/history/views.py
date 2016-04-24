from django.shortcuts import render, render_to_response
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.template import RequestContext


# Create your views here.
def index(request):
    return render_to_response("history/stats_overview.html", context_instance=RequestContext(request))

