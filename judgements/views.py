from django.http import HttpResponse
from django.template import loader

from .models import Judgement


def index(request):
    judgements = Judgement.objects.all
    context = {"judgement_list": judgements}
    template = loader.get_template("judgement/index.html")
    return HttpResponse(template.render(context, request))
