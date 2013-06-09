from django.conf import settings

TINT_TRANSFORMATIONS = getattr(settings, 'TINT_TRANSFORMATIONS', {})
TINT_IMAGE_PROCESSOR = getattr(settings, 'TINT_IMAGE_PROCESSOR', 'tint.imageprocs.default.DefaultImageProc')
TINT_KEEP_THUMBNAILS = getattr(settings, 'TINT_KEEP_THUMBNAILS', True)
TINT_KEEP_IMAGES = getattr(settings, 'TINT_KEEP_IMAGES', True)
