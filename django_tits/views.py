from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect

from . import models
from .settings import TITS_TRANSFORMATIONS

def thumbnail(request, image_id, transformation):
    image = get_object_or_404(models.Image, id=image_id)
    if not transformation in TITS_TRANSFORMATIONS:
        return HttpResponseNotFound()

    return redirect(models.Thumbnail.objects.get_or_create_at_transformation(image.id, transformation))
