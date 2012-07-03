# Create your views here.
from django.http import HttpResponse
from django.template import loader, RequestContext
from labels.models import DigitalLabel


def digitallabel(request, digitallabel_id, id=None, pos=None):
    dl = DigitalLabel.objects.get(id=digitallabel_id)
    mobjects = dl.museumobjects.all()
    if pos is not None:
        pos = int(pos)
    t = loader.get_template('digitallabel.html')
    c = RequestContext(request, {'mobjects':mobjects, 'id':id, 'pos':pos})
    return HttpResponse(t.render(c))


def index(request):
    """Lists available digital labels"""
    labels = DigitalLabel.objects.all()
    t = loader.get_template('base.html')
    c = RequestContext(request, {'labels':labels})
    return HttpResponse(t.render(c))


def template(request):
    """Preview the layout of fields in the frontend"""
    t = loader.get_template('template.html')
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))
