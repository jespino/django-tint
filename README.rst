django-tits
===========

Transparent Image Transformation System (based on django-images).

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
            scale: False,
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
            scale: True,
            opacity: 0.5,
        },
    ]
  }
