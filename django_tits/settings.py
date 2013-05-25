from django.conf import settings

TITS_TRANSFORMATIONS = getattr(settings, 'TITS_TRANSFORMATIONS', {})
TITS_IMAGE_PROCESSOR = getattr(settings, 'TITS_IMAGE_PROCESSOR', 'django_tits.imageprocs.default.DefaultImageProc')
