from django.core.files.images import ImageFile
from django.core.management import call_command
from django.core.urlresolvers import reverse

from django_tits import models
import unittest
import os

call_command('syncdb', interactive=False)


class ModelsTestCase(unittest.TestCase):
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

    def test_hashed_upload_to(self):
        self.assertEqual(
            models.hashed_upload_to("test/", self.image, 'test-image.png'),
            'test/4/e/4edc7685d17aa4d5c0c07a44e0e44f27/test-image.png'
        )

    def test_image_get_by_transformation(self):
        with self.assertRaises(models.Thumbnail.DoesNotExist):
            self.image.get_by_transformation('test1')
        self.image.get_absolute_url('test1', True),
        self.assertIsInstance(self.image.get_by_transformation('test1'), models.Thumbnail)

    def test_image_get_absolute_url(self):
        self.assertEqual(
            self.image.get_absolute_url(),
            '/media/image/original/by-md5/4/e/4edc7685d17aa4d5c0c07a44e0e44f27/test-image.png'
        )
        self.assertEqual(
            self.image.get_absolute_url('test1'),
            reverse('image-thumbnail', args=(self.image.id, 'test1'))
        )
        self.assertEqual(
            self.image.get_absolute_url('test1', True),
            '/media/image/thumbnail/by-md5/3/f/3fe2d799fd59ef5a9c6b057eb546bed5/test-image.png'

        )
        self.assertEqual(
            self.image.get_absolute_url('test1'),
            '/media/image/thumbnail/by-md5/3/f/3fe2d799fd59ef5a9c6b057eb546bed5/test-image.png'
        )
        models.Thumbnail.objects.all().delete()
        self.assertEqual(
            self.image.get_absolute_url('test1'),
            reverse('image-thumbnail', args=(self.image.id, 'test1'))
        )

    def test_image_upload_to(self):
        self.assertEqual(
            models.image_upload_to(self.image, 'test-image.png'),
            'image/original/by-md5/4/e/4edc7685d17aa4d5c0c07a44e0e44f27/test-image.png'
        )

    def test_thumbnail_upload_to(self):
        self.assertEqual(
            models.thumbnail_upload_to(self.image, 'test-image.png'),
            'image/thumbnail/by-md5/4/e/4edc7685d17aa4d5c0c07a44e0e44f27/test-image.png'
        )

    def test_thumbnail_manager_get_or_create_at_transformation(self):
        with self.assertRaises(ValueError):
            models.Thumbnail.objects.get_or_create_at_transformation(self.image.id, "invalid-transformation")

        with self.assertRaises(models.Image.DoesNotExist):
            models.Thumbnail.objects.get_or_create_at_transformation(-1, "test1")

        self.assertEqual(models.Thumbnail.objects.all().count(), 0)
        self.assertIsInstance(models.Thumbnail.objects.get_or_create_at_transformation(self.image.id, "test1"), models.Thumbnail)
        self.assertEqual(models.Thumbnail.objects.all().count(), 1)
        self.assertIsInstance(models.Thumbnail.objects.get_or_create_at_transformation(self.image.id, "test1"), models.Thumbnail)
        self.assertEqual(models.Thumbnail.objects.all().count(), 1)

    def test_thumbnail_get_absolute_url(self):
        self.image.get_absolute_url('test1', True),
        self.assertEqual(
            models.Thumbnail.objects.all()[0].get_absolute_url(),
            '/media/image/thumbnail/by-md5/3/f/3fe2d799fd59ef5a9c6b057eb546bed5/test-image.png'
        )

    def test_original_changed(self):
        self.assertEqual(models.Thumbnail.objects.all().count(), 0)
        models.Thumbnail.objects.get_or_create_at_transformation(self.image.id, "test1")
        self.assertEqual(models.Thumbnail.objects.all().count(), 1)
        self.image.save()
        self.assertEqual(models.Thumbnail.objects.all().count(), 0)
