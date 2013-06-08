from django import template

register = template.Library()


@register.filter
def at_transformation(image, transformation):
    return image.get_absolute_url(transformation=transformation)

try:
    from django_jinja.base import Library
    jinja_register = Library()

    @jinja_register.global_function
    def image_at_transformation(image, transformation):
        if image:
            return image.get_absolute_url(transformation=transformation)
        return None
except ImportError:
    pass
