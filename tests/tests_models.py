from django.core.files.images import ImageFile
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.test import TestCase

from tint import models
import os
import re

call_command('syncdb', interactive=False)


class ModelsTestCase(TestCase):
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

    def test_hashed_upload_to(self):
        self.assertIsNotNone(re.search(
            'test/[a-f0-9]/[a-f0-9]/[a-f0-9]{32}/test-image.png',
            models.hashed_upload_to("test/", self.image, 'test-image.png')
        ))

    def test_image_get_by_transformation(self):
        self.assertRaises(
            models.Thumbnail.DoesNotExist,
            lambda: self.image.get_by_transformation('test1')
        )
        self.image.get_absolute_url('test1', True),
        self.assertTrue(isinstance(self.image.get_by_transformation('test1'), models.Thumbnail))

    def test_image_get_absolute_url(self):
        self.assertIsNotNone(re.search(
            '/media/image/original/by-md5/[a-f0-9]/[a-f0-9]/[a-f0-9]{32}/test-image.png',
            self.image.get_absolute_url()
        ))
        self.assertEqual(
            self.image.get_absolute_url('test1'),
            reverse('image-thumbnail', args=(self.image.id, 'test1'))
        )
        self.assertIsNotNone(re.search(
            '/media/image/thumbnail/by-md5/[a-f0-9]/[a-f0-9]/[a-f0-9]{32}/test-image.png',
            self.image.get_absolute_url('test1', True)
        ))
        self.assertIsNotNone(re.search(
            '/media/image/thumbnail/by-md5/[a-f0-9]/[a-f0-9]/[a-f0-9]{32}/test-image.png',
            self.image.get_absolute_url('test1')
        ))
        models.Thumbnail.objects.all().delete()
        self.assertEqual(
            self.image.get_absolute_url('test1'),
            reverse('image-thumbnail', args=(self.image.id, 'test1'))
        )

    def test_image_upload_to(self):
        self.assertIsNotNone(re.search(
            'image/original/by-md5/[a-f0-9]/[a-f0-9]/[a-f0-9]{32}/test-image.png',
            models.image_upload_to(self.image, 'test-image.png')
        ))

    def test_thumbnail_upload_to(self):
        self.assertIsNotNone(re.search(
            'image/thumbnail/by-md5/[a-f0-9]/[a-f0-9]/[a-f0-9]{32}/test-image.png',
            models.thumbnail_upload_to(self.image, 'test-image.png')
        ))

    def test_thumbnail_manager_get_or_create_at_transformation(self):
        self.assertRaises(
            ValueError,
            lambda: models.Thumbnail.objects.get_or_create_at_transformation(self.image.id, "invalid-transformation")
        )

        self.assertRaises(
            models.Image.DoesNotExist,
            lambda: models.Thumbnail.objects.get_or_create_at_transformation(-1, "test1")
        )

        self.assertEqual(models.Thumbnail.objects.all().count(), 0)
        self.assertTrue(isinstance(
            models.Thumbnail.objects.get_or_create_at_transformation(self.image.id, "test1"),
            models.Thumbnail
        ))
        self.assertEqual(models.Thumbnail.objects.all().count(), 1)
        self.assertTrue(isinstance(
            models.Thumbnail.objects.get_or_create_at_transformation(self.image.id, "test1"),
            models.Thumbnail
        ))
        self.assertEqual(models.Thumbnail.objects.all().count(), 1)

    def test_thumbnail_get_absolute_url(self):
        self.image.get_absolute_url('test1', True),
        self.assertIsNotNone(re.search(
            '/media/image/thumbnail/by-md5/[a-f0-9]/[a-f0-9]/[a-f0-9]{32}/test-image.png',
            models.Thumbnail.objects.all()[0].get_absolute_url()
        ))

    def test_original_changed(self):
        self.assertEqual(models.Thumbnail.objects.all().count(), 0)
        models.Thumbnail.objects.get_or_create_at_transformation(self.image.id, "test1")
        self.assertEqual(models.Thumbnail.objects.all().count(), 1)
        self.image.save()
        self.assertEqual(models.Thumbnail.objects.all().count(), 0)
