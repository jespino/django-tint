from django.conf import settings

TITS_TRANSFORMATIONS = getattr(settings, 'TITS_TRANSFORMATIONS', {})
TITS_IMAGE_PROCESSOR = getattr(settings, 'TITS_IMAGE_PROCESSOR', 'django_tits.imageprocs.default.DefaultImageProc')
TITS_KEEP_THUMBNAILS = getattr(settings, 'TITS_KEEP_THUMBNAILS', True)
TITS_KEEP_IMAGES = getattr(settings, 'TITS_KEEP_IMAGES', True)
