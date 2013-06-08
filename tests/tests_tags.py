from django.utils import unittest
from django.template import Template, Context
from django.core.files.images import ImageFile
from django.core.urlresolvers import reverse

from django_jinja.base import env

from django_tits import models

import os

class TemplateTagsTestCase(unittest.TestCase):
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

    def test_tits_django_templatetag(self):
        context = Context({ "image": self.image })
        result = Template("{% load tits %}{{ image|at_transformation:'test1' }}").render(context)
        self.assertEqual(result, reverse('image-thumbnail', args=(self.image.id, 'test1')))
        self.image.get_absolute_url('test1', True)
        result = Template("{% load tits %}{{ image|at_transformation:'test1' }}").render(context)
        self.assertEqual(result, '/media/image/thumbnail/by-md5/a/3/a3395e1c1dc5ada82958c73f33c6641b/test-image.png')

    def test_tits_django_jinja_global_function(self):
        context = Context({ "image": self.image })
        result = env.from_string("{{ image_at_transformation(image, 'test1') }}").render(context)
        self.assertEqual(result, reverse('image-thumbnail', args=(self.image.id, 'test1')))
        self.image.get_absolute_url('test1', True)
        result = env.from_string("{{ image_at_transformation(image, 'test1') }}").render(context)
        self.assertEqual(result, '/media/image/thumbnail/by-md5/a/3/a3395e1c1dc5ada82958c73f33c6641b/test-image.png')
