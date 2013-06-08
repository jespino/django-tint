from django.utils import unittest
from django.template import Template, Context
from django.core.files.images import ImageFile
from django.core.urlresolvers import reverse
from django.test import TestCase

from django_jinja.base import env

from django_tits import models

import os

class ViewsTestCase(TestCase):
    def setUp(self):
        image_file = open(os.path.join(os.path.dirname(__file__), 'test-image.png'), 'r')
        self.image = models.Image.objects.create(
            image=ImageFile(image_file, name='test-image.png'),
            height=640,
            width=480,
        )

    def tearDown(self):
        models.Image.objects.all().delete()
        models.Thumbnail.objects.all().delete()

    def test_thumbnail_view(self):
        response = self.client.get(reverse('image-thumbnail', args=(1000000, 'test1')))
        self.assertEqual(response.status_code, 404)
        response = self.client.get(reverse('image-thumbnail', args=(self.image.id, 'not-valid-transformation')))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(models.Thumbnail.objects.all().count(), 0)
        response = self.client.get(reverse('image-thumbnail', args=(self.image.id, 'test1')))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
                response.get('location'),
                'http://testserver/media/image/thumbnail/by-md5/a/3/a3395e1c1dc5ada82958c73f33c6641b/test-image.png'
        )
        self.assertEqual(models.Thumbnail.objects.all().count(), 1)
