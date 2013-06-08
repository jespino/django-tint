import os

from io import BytesIO

from PIL import Image, ImageOps, ImageEnhance, ImageFile

class DefaultImageProc(object):
    def crop(self, image, params):
        (width, height) = image.size

        align = params.get('align', 'center')
        valign = params.get('valign', 'middle')

        if width >= params['width']:
            if align == 'center':
                left = (width/2)-(params['width']/2)
                right = (width/2)+(params['width']/2)
            elif align == 'left':
                left = 0
                right = params['width']
            elif align == 'right':
                left = width-params['width']
                right = width
            else:
                raise Exception('Invalid align')
        else:
            left = 0
            right = width

        if height >= params['height']:
            if valign == 'middle':
                top = (height/2)-(params['height']/2)
                bottom = (height/2)+(params['height']/2)
            elif valign == 'top':
                top = 0
                bottom = params['height']
            elif valign == 'bottom':
                top = height-params['height']
                bottom = height
            else:
                raise Exception('Invalid valign')
        else:
            top = 0
            bottom = height
        return image.crop((left, top, right, bottom))

    def fit(self, image, params):
        num_align = [0.0, 0.0]
        align = params.get('align', 'center')
        valign = params.get('valign', 'middle')

        if align == 'center':
            num_align[1] = 0.5
        elif align == 'left':
            num_align[1] = 0.0
        elif align == 'right':
            num_align[1] = 1.0
        else:
            raise Exception('Invalid align')

        if valign == 'middle':
            num_align[0] = 0.5
        elif valign == 'top':
            num_align[0] = 0.0
        elif valign == 'bottom':
            num_align[0] = 1.0
        else:
            raise Exception('Invalid valign')
        return ImageOps.fit(image, (params['width'], params['height']), Image.ANTIALIAS, 0, num_align)

    def grayscale(self, image, params):
        return ImageOps.grayscale(image)

    def invert(self, image, params):
        image = image.convert('RGB')
        return ImageOps.invert(image)

    def flip(self, image, params):
        return ImageOps.flip(image)

    def mirror(self, image, params):
        return ImageOps.mirror(image)

    def autocontrast(self, image, params):
        return ImageOps.autocontrast(image, params.get('cutoff', 0))

    def equalize(self, image, params):
        return ImageOps.equalize(image)

    def scale(self, image, params):
        return image.resize((params['width'], params['height']), Image.ANTIALIAS)

    def watermark(self, image, params):
        orig_watermark = Image.open(params['watermark_image']).convert('RGBA')
        orig_watermark = orig_watermark.resize(image.size, Image.ANTIALIAS)

        watermark = orig_watermark.copy()

        opacity = params.get('opacity', None)
        if opacity is not None:
            alpha = watermark.split()[3]
            alpha = ImageEnhance.Brightness(alpha).enhance(float(opacity))
            watermark.putalpha(alpha)
        return Image.composite(orig_watermark, image, watermark)

    def transform(self, image, *actions):
        image.open()
        im = Image.open(image)
        im_format, im_info = im.format, im.info
        for action in actions:
            im = getattr(self, action['action'])(im, action)
        im.format, im.info = im_format, im_info

        # save to memory
        buf = BytesIO()
        try:
            im.save(buf, im.format, **im.info)
        except IOError:
            if im.info.get('progression'):
                orig_MAXBLOCK = ImageFile.MAXBLOCK
                temp_MAXBLOCK = 1048576
                if orig_MAXBLOCK >= temp_MAXBLOCK:
                    raise
                ImageFile.MAXBLOCK = temp_MAXBLOCK
                try:
                    im.save(buf, im.format, **im.info)
                finally:
                    ImageFile.MAXBLOCK = orig_MAXBLOCK
            else:
                raise
        image.close()

        return buf
