.. image:: logo/logo.png

Default ImageProc Actions
~~~~~~~~~~~~~~~~~~~~~~~~~

Django-tits default Image Processor comes with some actions, here you have the
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

In Django-tits you can define your ImageProc class (normally will be a subclass
of the DefaultImageProc) to add your own image transformations. You can use it
configuring the TITS_IMAGE_PROCESSOR settings variable. Example::

  TITS_IMAGE_PROCESSOR = 'myapp.my_image_processor_module.MyImageProcessorClass'

If the variable is not defined the DefaultImageProc is used.

Then you can configure your transformations as a dictionary. The name of the
transformation is the key, and the value is a list of "actions". An action is a
dictionary with one key 'action' with the name of the action, and the other
keys the parameters to use in this action. Example::

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

