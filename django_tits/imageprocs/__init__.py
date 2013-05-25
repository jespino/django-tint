from django_tits import settings
from django.utils.importlib import import_module

__all__ = ('image_proc',)

module_name = ".".join(settings.TITS_IMAGE_PROCESSOR.split(".")[0:-1])
class_name = settings.TITS_IMAGE_PROCESSOR.split(".")[-1]
image_proc = getattr(import_module(module_name), class_name)()
