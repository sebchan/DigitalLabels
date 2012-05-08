"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from labels.models import DigitalLabel, Image


class SimpleTest(TestCase):

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class LabelTest(TestCase):

    def setUp(self):
        """
        Tests that we can create a copy of the API data in the
        DigitalLabel model
        """
        dl, cr = DigitalLabel.objects.get_or_create(object_number='O7351')

    def test_label_download(self):

        # get our label
        dl = DigitalLabel.objects.get(id=1)

        # test the data fields
        self.assertTrue(len(dl.name) > 0)
        self.assertTrue(len(dl.museum_number) > 0)
        self.assertTrue(len(dl.artist_maker) > 0)

        # test the labels
        self.assertTrue(dl.cmslabel_set.count() > 0)

    def test_missing_object(self):
        dl, cr = DigitalLabel.objects.get_or_create(object_number='OMISSING')

        self.assertTrue(dl.name.find('UNABLE') > -1)
        # test the labels
        self.assertTrue(dl.cmslabel_set.count() == 0)

    def test_thumbnail_url(self):

        # get our label
        dl = DigitalLabel.objects.get(id=1)
        self.assertTrue(dl.thumbnail_url.endswith('jpg'))
        self.assertTrue(dl.thumbnail_tag().find('cache') > -1)

    def test_redownload(self):

        # get our label
        dl = DigitalLabel.objects.get(id=1)
        original_name = dl.name
        replaced_name = 'Foo Bar Baz'
        self.assertNotEqual(dl.name, replaced_name)

        # change the name
        dl.name = replaced_name
        dl.save()
        self.assertEqual(dl.name, replaced_name)

        dl.redownload = True
        dl.save()

        # ensure original name was redownloaded
        self.assertEqual(dl.name, original_name)
        self.assertFalse(dl.redownload)

    def test_download_image(self):

        # count image
        dl = DigitalLabel.objects.get(id=1)

        ims = dl.image_set.all()
        ic = ims.count()
        self.assertTrue(ic > 0)

        test_image = ims[0]
        self.assertEquals(
            unicode(test_image.image_file).find(test_image.image_id), 14)

        # check primary image position
        self.assertEquals(dl.image_set.filter(position=0).count(), 1)
        self.assertTrue(dl.image_set.filter(position=1).count() > 0)
