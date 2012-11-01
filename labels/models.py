import logging
import os
import urllib2
import httplib
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import simplejson
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from sorl.thumbnail import ImageField, get_thumbnail
# Create your models here.
# import the logging library

# Get an instance of a logger
logger = logging.getLogger('labels')


class BaseScreen(models.Model):
    name = models.CharField(max_length=255, null=False)
    timeout_images = models.ManyToManyField("Image", blank=True)

    _thumbnail_url = None

    def __unicode__(self):
        return self.name

    def referrer(self):
        return self._meta.object_name.lower()

    @property
    def model_name(self):
        return self._meta.object_name.lower()

    def _Objects(self):
        return self.museumobjects.count()

    class Meta:
        abstract = True


class BaseLabel(models.Model):
    _thumbnail_url = None

    def digital_label(self):
        href = reverse('admin:%s_%s_change' % (self._meta.app_label, 'digitallabel'),
                       args=[self.digitallabel.pk])
        return mark_safe('<a href="%s">%s</a>' % (href, self.digitallabel))

    digital_label.allow_tags = True

    def _portal(self):
        href = reverse('admin:%s_%s_change' % (self._meta.app_label, 'portal'),
                       args=[self.portal.pk])
        return mark_safe('<a href="%s">%s</a>' % (href, self.portal))

    _portal.allow_tags = True


    def admin_template(self):
        return 'admin:%s_%s_change' % (self._meta.app_label, self._meta.object_name.lower())

    @property
    def display_text(self):
        return NotImplementedError

    @property
    def thumbnail_url(self):

        if not self._thumbnail_url:

            if self.image_set.count() > 0:

                # images are sorted by priority, so take the first
                image_file = self.image_set.all()[0]

                im = get_thumbnail(image_file.local_filename, '44x44',
                                                    quality=85, pad=True)

                self._thumbnail_url = im.url

        return self._thumbnail_url

    def thumbnail_tag(self):

        if self.thumbnail_url:
            return mark_safe('<img alt="%s" src="%s" />' % (
                            strip_tags(self.display_text), self.thumbnail_url))
        else:
            return mark_safe('<em>No Images</em>')

    thumbnail_tag.allow_tags = True
    thumbnail_tag.short_description = 'Thumb'

    class Meta:
        abstract = True


class MuseumObject(BaseLabel):
    """
    A label describing an individual object
    """
    name = models.CharField(max_length=255, null=False, blank=True)
    date_text = models.CharField(max_length=255, null=False, blank=True)
    artist_maker = models.CharField("Designer / Maker",
                                    max_length=255, null=False, blank=True)
    restored_altered = models.CharField("Restored / Altered",
                                    max_length=255, null=False, blank=True)
    place = models.TextField("Place of Design / Manufacture", blank=True)
    materials_techniques = models.TextField(blank=True)
    museum_number = models.CharField(max_length=255, null=False, blank=True)
    object_number = models.CharField(max_length=16, null=False, blank=True,
                db_index=True, help_text="""Optional. Unique "O" number, For
                                             example, O9138, as used on
                                         Search the Collections""")
    credit_line = models.CharField(max_length=255, null=False, blank=True)
    artfund = models.BooleanField(default=False)
    main_text = models.TextField(blank=True)
    redownload = models.BooleanField(help_text="""WARNING: This may
                                         replace your existing content""")

    @property
    def display_text(self):
        return self.name

    class Meta:
        verbose_name = "object"

    def __unicode__(self):
        if self.museum_number:
            return u"%s %s (%s)" % (self.object_number,
                                 self.name, self.museum_number)
        else:
            return self.name

    _museumobject_json = None

    @property
    def museumobject_json(self):

        if self._museumobject_json == None and self.object_number:
            item_url = 'http://%s/api/json/museumobject/%s/' % (
                                        settings.COLLECTIONS_API_HOSTNAME,
                                        self.object_number)
            try:
                response = urllib2.urlopen(item_url)
                self._museumobject_json = simplejson.load(response)[0]

            except urllib2.HTTPError, e:
                if e.code == 404:
                    # Missing object
                    pass
                else:
                    # other error
                    pass

        return self._museumobject_json

    def create_cms_labels(self):

        museum_object = self.museumobject_json
        if museum_object:
            for l in museum_object['fields']['labels']:
                cms_label = CMSLabel()
                cms_label.date = l['fields']['date']
                cms_label.text = l['fields']['label_text']
                cms_label.museumobject = self
                cms_label.save()

    def create_images(self):

        museum_object = self.museumobject_json
        if museum_object:
            for i in museum_object['fields']['image_set']:
                image_id = i['fields']['image_id']
                try:
                    cms_image, cr = Image.objects.get_or_create(
                                museumobject=self, image_id=image_id)
                    # retreive image from media server
                    image_success = cms_image.store_vadar_image()
                    if image_success:
                        cms_image.caption = image_id
                        cms_image.image_file = os.path.join(
                                        cms_image.image_file.field.upload_to,
                                        unicode(cms_image.image_id) + '.jpg')
                        if image_id == \
                                museum_object['fields']['primary_image_id']:
                            cms_image.position = 0
                        cms_image.save()
                    else:
                        cms_image.delete()

                except urllib2.HTTPError, e:
                    cms_image.image_file = ''
                    if e.code == 404:
                        # Missing object
                        pass
                    else:
                        # other error
                        pass


class TextLabel(BaseLabel):
    """
    A label describing biography or a historical notes
    """
    title = models.CharField(max_length=255, null=False, blank=True)

    main_text = models.TextField(blank=True)

    @property
    def display_text(self):
        return self.title

    def __unicode__(self):
        return self.title


class CMSLabel(models.Model):

    date = models.CharField(max_length=255, null=False)
    text = models.TextField()
    museumobject = models.ForeignKey(MuseumObject)

    def __unicode__(self):
        return u"%s for %s" % (self.date, self.museumobject.museum_number)


class Image(models.Model):

    image_id = models.CharField(max_length=16, null=False, blank=True)
    caption = models.TextField(blank=True)
    image_file = ImageField(upload_to="labels/images")
    position = models.PositiveIntegerField(null=False, default=1)
    museumobject = models.ForeignKey(MuseumObject, null=True, blank=True)
    textlabel = models.ForeignKey(TextLabel, null=True, blank=True)

    class Meta:
        ordering = ['position']

    def __unicode__(self):
        if self.museumobject:
            desc = self.museumobject
        elif self.textlabel:
            desc = self.textlabel
        else:
            desc = self.caption

        return '%s - %s' % (os.path.basename(self.image_file.name), desc)

    def object_link(self):
        href = reverse('admin:%s_%s_change' % (self._meta.app_label, 'museumobject'),
                       args=[self.museumobject.pk])
        return mark_safe('<a href="%s">%s</a>' % (href, self.museumobject))

    object_link.allow_tags = True

    def label_link(self):
        href = reverse('admin:%s_%s_change' % (self._meta.app_label, 'textlabel'),
                       args=[self.textlabel.pk])
        return mark_safe('<a href="%s">%s</a>' % (href, self.textlabel))

    label_link.allow_tags = True

    @property
    def local_filename(self):
        """Where is the file stored regardless of source"""
        if unicode(self.image_file):
            return os.path.join(settings.MEDIA_ROOT,
                                self.image_file.field.upload_to,
                                unicode(self.image_file.file))
        else:
            return None

    def thumb(self):
        im = get_thumbnail(self.local_filename, '44x44',
                                                    quality=85, pad=True)

        return mark_safe('<img alt="%s" src="%s" />' % (
                                            strip_tags(self.caption), im.url))
    thumb.allow_tags = True

    @property
    def local_vadar_filename(self):
        """Where should this image be stored if it can be retrieved?"""
        if self.image_id:
            return "%s%s/%s.jpg" % (settings.MEDIA_ROOT,
                                        self.image_file.field.upload_to,
                                         unicode(self.image_id))
        else:
            raise Exception('No Image ID set')

    def store_vadar_image(self):
        #create the url and the request
        image_url = 'http://%s/media/thira/collection_images/%s/%s.jpg' % \
                     (settings.MEDIA_SERVER, self.image_id[:6], self.image_id)
        req = urllib2.Request(image_url)

        # Open the url
        try:
            logging.info("downloading " + image_url)
            f = urllib2.urlopen(req)
            meta = f.info()
            if meta.type == 'image/jpeg':
                # Open our local file for writing
                local_file = open(self.local_vadar_filename, "wb")
                #Write to our local file
                local_file.write(f.read())
                local_file.close()
                return True
            else:
                logging.error("Image Error: Wrong type %s" % (meta.type))
                return False
        #handle errors
        except urllib2.HTTPError, e:
            logging.error("HTTP Error: %s %s" % (e.code, image_url))
            self.image_file = None
            return False
        except httplib.BadStatusLine, e:
            logging.error("HTTP Bad Status: %s %s" % (e.reason, image_url))
            self.image_file = None
            return False
        except urllib2.URLError, e:
            logging.error("URL Error: %s %s" % (e.reason, image_url))
            self.image_file = None
            return False


class DigitalLabel(BaseScreen):
    museumobjects = models.ManyToManyField(MuseumObject, through='DigitalLabelObject')


class Portal(BaseScreen):
    museumobjects = models.ManyToManyField(MuseumObject, through='PortalObject')
    textlabels = models.ManyToManyField(TextLabel, through='PortalTextLabel')

    def _Labels(self):
        return self.textlabels.count()


class BaseRelation(models.Model):
    position = models.PositiveIntegerField(null=False, default=1)

    class Meta:
        ordering = ['position']

    def target(self):
        raise NotImplementedError()


class BaseObjectRelation(BaseRelation):
    museumobject = models.ForeignKey(MuseumObject)

    def target(self):
        return self.museumobject

    class Meta:
        abstract = True


class DigitalLabelObject(BaseObjectRelation):
    digitallabel = models.ForeignKey(DigitalLabel)
    gateway_object = models.BooleanField(default=False)


class PortalObject(BaseObjectRelation):
    portal = models.ForeignKey(Portal)


class PortalTextLabel(BaseRelation):
    portal = models.ForeignKey(Portal)
    textlabel = models.ForeignKey(TextLabel)
    biography = models.BooleanField(default=False)

    def target(self):
        return self.textlabel


from django.db.models.signals import pre_save, post_save
from labels.signals import get_api_data, get_related_api_data, \
                                                        create_thumbnails

pre_save.connect(get_api_data, MuseumObject)
post_save.connect(get_related_api_data, MuseumObject)
post_save.connect(create_thumbnails, Image)
