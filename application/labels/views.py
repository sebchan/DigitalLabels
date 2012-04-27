# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from labels.models import Group

def group(request, group_id=None, format='html'):

    group = Group.objects.get(id=group_id)
    labels = group.digitallabels.all()
    
    t = loader.get_template('group.html')
    c = RequestContext(request, { 'labels':labels })

    return HttpResponse(t.render(c))
    
def index(request):
    
    t = loader.get_template('base.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))
        