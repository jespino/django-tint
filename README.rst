django-tits
===========

Transparent Image Transformation System (based on django-images).

Default ImageProc Actions
~~~~~~~~~~~~~~~~~~~~~~~~~

Django-tits default Image Processor comes with some actions, here you have the
list:

crop
----

Crop the image to the width and height parameters, using the parameters align
and valign to know where to cut.

scale
-----

Simply scale the image to the width and height parameters (deforming it if not
have the same proportion).

fit
---

Scale and crop the image to width and height parameters with a proportional
result, croping out the what is not necesary. The parameters align and valing
allow you to define where to crop.

watermark
---------

Put a watermark on the image using the watermark_image file with the opacity
received as parameter. The watermark allwais will be scaled to the result image
size.

grayscale
---------

Convert the image to grayscale.

flip
----

Flip the image vertically.

mirror
------

Flip the image horizontally.

equialize
---------

Equalize the image histogram.

invert
------

Invert the colors of the image.

Configuration
~~~~~~~~~~~~~
Configuration example::

  TITS_TRANSFORMATIONS = {
    'example1': [
        {
            action: 'fit',
            width: '1024',
            height: '768',
            align: 'center',
            valign: 'middle',
            format: 'png',
        },
        {
            action: 'watermark',
            image: 'example.watermark.png',
            opacity: 0.5,
        },
    ],
    'example2': [
        {
            action: 'fit',
            width: '800',
            height: '600',
            align: 'center',
            valign: 'middle',
            format: 'png',
        },
        {
            action: 'watermark',
            image: 'example.watermark.png',
            opacity: 0.5,
        },
    ]
  }

