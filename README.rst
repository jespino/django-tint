Django Transparent Image Neat Transformer
-----------------------------------------

.. image:: http://kaleidos.net/static/img/badge.png
    :target: http://www.kaleidos.net/community/django-tint/

.. image:: https://travis-ci.org/jespino/django-tint.png?branch=master
    :target: https://travis-ci.org/jespino/django-tint

.. image:: https://coveralls.io/repos/jespino/django-tint/badge.png?branch=master
    :target: https://coveralls.io/r/jespino/django-tint?branch=master

.. image:: https://pypip.in/v/django-tint/badge.png
    :target: https://crate.io/packages/django-tint

.. image:: https://pypip.in/d/django-tint/badge.png
    :target: https://crate.io/packages/django-tint

Usage
~~~~~

You must define your transformation in your :code:`TINT_TRANSFORMATIONS` settings
variable.

You set your images on your models puting a :code:`ForeignKey` to
:code:`tint.models.Image`.

Then you put your images in your templates using the :code:`at_transformation` filter. Example::

  {% load tint %}

  <img src="{{ mymodel.my_image_field|at_transformation:"my-transformation-definition" }}" />

If you use django-jinja you only have to use the :code:`image_at_transformation` function. Example::

  <img src="{{ image_at_transformation(mymodel.my_image_field, "my-transformation-definition") }}" />


Default ImageProc Actions
~~~~~~~~~~~~~~~~~~~~~~~~~

Django-tint default Image Processor comes with some actions, here you have the
list:

+-----------------+-------------------------------+--------------------------+
| Action          | Description                   | Params                   |
+=================+===============================+==========================+
| crop            | Crop an image to a width and  | height, width, align,    |
|                 | height.                       | valign                   |
+-----------------+-------------------------------+--------------------------+
| scale           | Scale an image to a width and | height, width            |
|                 | height (deforming it).        |                          |
+-----------------+-------------------------------+--------------------------+
| fit             | Scale an image to a width and | height, width, align,    |
|                 | height and crop the overflow. | valign                   |
+-----------------+-------------------------------+--------------------------+
| watermark       | Paste a watermark on a image. | watermark_image, opacity |
+-----------------+-------------------------------+--------------------------+
| grayscale       | Convert the image to          |                          |
|                 | grayscale.                    |                          |
+-----------------+-------------------------------+--------------------------+
| flip            | Flip the image vertically.    |                          |
+-----------------+-------------------------------+--------------------------+
| mirror          | Flip the image horizontally.  |                          |
+-----------------+-------------------------------+--------------------------+
| equalize        | Equalize the image histogram. |                          |
+-----------------+-------------------------------+--------------------------+
| autocontrast    | Maximize (normalize) image    | cutoff                   |
|                 | contrast.                     |                          |
+-----------------+-------------------------------+--------------------------+
| invert          | Invert the image colors.      |                          |
+-----------------+-------------------------------+--------------------------+

Configuration
~~~~~~~~~~~~~

In Django-tint you can define your :code:`ImageProc` class (normally will be a subclass
of the :code:`DefaultImageProc`) to add your own image transformations. You can use it
configuring the :code:`TINT_IMAGE_PROCESSOR` settings variable. Example::

  TINT_IMAGE_PROCESSOR = 'myapp.my_image_processor_module.MyImageProcessorClass'

If the variable is not defined the :code:`DefaultImageProc` is used.

Then you can configure your transformations as a dictionary. The name of the
transformation is the key, and the value is a list of "actions". An action is a
dictionary with one key 'action' with the name of the action, and the other
keys the parameters to use in this action. Example::

  TINT_TRANSFORMATIONS = {
    'example1': [
        {
            "action": 'fit',
            "width": 1024,
            "height": 768,
            "align": 'center',
            "valign": 'middle',
        },
        {
            "action": 'watermark',
            "image": 'example.watermark.png',
            "opacity": 0.5,
        },
    ],
    'example2': [
        {
            "action": 'fit',
            "width": 800,
            "height": 600,
            "align": 'center',
            "valign": 'middle',
        },
        {
            "action": 'watermark',
            "image": 'example.watermark.png',
            "opacity": 0.5,
        },
    ]
  }

