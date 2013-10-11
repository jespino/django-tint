from django.core.files.images import ImageFile
from django.core.urlresolvers import reverse
from django.test import TestCase

from tint import models

import os
import re


class ViewsTestCase(TestCase):
    def setUp(self):
        image_file = open(os.path.join(os.path.dirname(__file__), 'test-image.png'), 'rb')
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
        self.assertIsNotNone(re.search(
            'http://testserver/media/image/thumbnail/by-md5/[a-f0-9]/[a-f0-9]/[a-f0-9]{32}/test-image.png',
            response.get('location')
        ))
        self.assertEqual(models.Thumbnail.objects.all().count(), 1)
