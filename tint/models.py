import hashlib
import os.path

from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.urlresolvers import reverse
from django.dispatch import receiver

from .settings import TINT_TRANSFORMATIONS, TINT_KEEP_IMAGES, TINT_KEEP_THUMBNAILS

from .imageprocs import image_proc


def hashed_upload_to(prefix, instance, filename):
    hasher = hashlib.md5()
    instance.image.open('rb')
    for chunk in instance.image.chunks():
        hasher.update(chunk)
    hash = hasher.hexdigest()
    base, ext = os.path.splitext(filename)
    return '%(prefix)s%(first)s/%(second)s/%(hash)s/%(base)s%(ext)s' % {
        'prefix': prefix,
        'first': hash[0],
        'second': hash[1],
        'hash': hash,
        'base': base,
        'ext': ext,
    }

def image_upload_to(instance, filename, **kwargs):
    return hashed_upload_to('image/original/by-md5/', instance, filename)

class Image(models.Model):
    image = models.ImageField(upload_to=image_upload_to,
            height_field='height', width_field='width',
            max_length=255)
    height = models.PositiveIntegerField(default=0, editable=False)
    width = models.PositiveIntegerField(default=0, editable=False)

    def get_by_transformation(self, transformation):
        return self.thumbnail_set.get(transformation=transformation)

    def get_absolute_url(self, transformation=None, wait_creation=False):
        if not transformation:
            return self.image.url
        try:
            return self.get_by_transformation(transformation).image.url
        except Thumbnail.DoesNotExist:
            if wait_creation:
                thumbnail = Thumbnail.objects.get_or_create_at_transformation(self.id, transformation)
                return thumbnail.image.url
            return reverse('image-thumbnail', args=(self.id, transformation))


def thumbnail_upload_to(instance, filename, **kwargs):
    return hashed_upload_to('image/thumbnail/by-md5/', instance, filename)


class ThumbnailManager(models.Manager):
    def get_or_create_at_transformation(self, image_id, transformation):
        image = Image.objects.get(id=image_id)
        if not transformation in TINT_TRANSFORMATIONS:
            raise ValueError("Received unknown transformation: %s" % transformation)
        try:
            thumbnail = image.get_by_transformation(transformation)
        except Thumbnail.DoesNotExist:
            buf = image_proc.transform(image.image, *TINT_TRANSFORMATIONS[transformation])
            # and save to storage
            original_dir, original_file = os.path.split(image.image.name)
            thumb_file = InMemoryUploadedFile(buf, "image", original_file, None, buf.tell(), None)
            thumbnail, created = image.thumbnail_set.get_or_create(
                transformation=transformation,
                defaults={'image': thumb_file})
        return thumbnail

class Thumbnail(models.Model):
    original = models.ForeignKey(Image)
    image = models.ImageField(upload_to=thumbnail_upload_to,
            height_field='height', width_field='width',
            max_length=255)
    transformation = models.CharField(max_length=100)
    height = models.PositiveIntegerField(default=0, editable=False)
    width = models.PositiveIntegerField(default=0, editable=False)

    objects = ThumbnailManager()

    class Meta:
        unique_together = ('original', 'transformation')

    def get_absolute_url(self):
        return self.image.url

@receiver(models.signals.post_save)
def original_changed(sender, instance, created, **kwargs):
    if isinstance(instance, Image):
        instance.thumbnail_set.all().delete()

@receiver(models.signals.post_delete)
def remove_image(sender, instance, **kwargs):
    if isinstance(instance, Image):
        if not TINT_KEEP_IMAGES:
            instance.image.delete(save=False)

    if isinstance(instance, Thumbnail):
        if not TINT_KEEP_THUMBNAILS:
            instance.image.delete(save=False)
