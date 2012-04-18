import urllib2
from django.utils import simplejson
from django.conf import settings
from django.db.models.signals import pre_save
from labels.models import DigitalLabel

@receiver(pre_save, sender=DigitalLabel)
def get_cms_labels(sender, **kwargs):

    item_url = 'http://%s/api/json/museumobject/%s' % (
                                settings.COLLECTIONS_API_HOSTNAME, 'O7351/')

    response = urllib2.urlopen(item_url)
    museum_object = simplejson.load(response)[0]
    for l in museum_object['fields']['labels']:

        print l

    print 'saving'




