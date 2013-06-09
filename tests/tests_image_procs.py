from PIL import Image, ImageOps, ImageEnhance, ImageFile
from tint.imageprocs.default import DefaultImageProc

import unittest
import os

class DefaultImageProcTestCase(unittest.TestCase):
    def assertImageEdges(self, image, edge_width, colors_top, colors_middle, colors_bottom):
        self.assertTrue(self.verify_edges(image, edge_width, colors_top, colors_middle, colors_bottom))

    def assertNotImageEdges(self, image, edge_width, colors_top, colors_middle, colors_bottom):
        self.assertFalse(self.verify_edges(image, edge_width, colors_top, colors_middle, colors_bottom))

    def verify_edges(self, image, edge_width, colors_top=None, colors_middle=None, colors_bottom=None):
        result = True
        width, height = image.size

        for x in range(edge_width):
            if colors_top:
                # TOP check
                result = result and image.getpixel((x, x)) == colors_top[0]
                result = result and image.getpixel((int(width/2), x)) == colors_top[1]
                result = result and image.getpixel((width-edge_width+x, edge_width-x)) == colors_top[2]

            if colors_middle:
                # MIDDLE check
                result = result and image.getpixel((x, int(height/2))) == colors_middle[0]
                result = result and image.getpixel(((width/2), int(height/2))) == colors_middle[1]
                result = result and image.getpixel((width-edge_width+x, int(height/2))) == colors_middle[2]

            if colors_bottom:
                # BOTTOM check
                result = result and image.getpixel((edge_width-x, height-edge_width+x)) == colors_bottom[0]
                result = result and image.getpixel((int(width/2), height-edge_width+x)) == colors_bottom[1]
                result = result and image.getpixel((width-edge_width+x, height-edge_width+x)) == colors_bottom[2]
        return result

    @classmethod
    def setUpClass(cls):
        cls.proc = DefaultImageProc()
        cls.black = (0, 0, 0, 255)
        cls.white = (255, 255, 255, 255)
        cls.red = (255, 0, 0, 255)
        cls.green = (0, 255, 0, 255)
        cls.blue = (0, 0, 255, 255)
        cls.yellow = (255, 255, 0, 255)
        cls.image = Image.open(os.path.join(os.path.dirname(__file__), 'test-image.png'))

    def test_crop(self):
        self.assertRaises(
                Exception,
                lambda: self.proc.crop(self.image.copy(), { "width": 320, "height": 240, "align": 'invalid', "valign": 'top' })
        )

        self.assertRaises(
            Exception,
            lambda: self.proc.crop(self.image.copy(), { "width": 320, "height": 240, "align": 'left', "valign": 'invalid' })
        )

        image_result = self.proc.crop(self.image.copy(), { "width": 1280, "height": 960 })
        self.assertEqual((640, 480), image_result.size)

        image_result = self.proc.crop(self.image.copy(), { "width": 320, "height": 240, "align": 'left', "valign": 'top' })
        self.assertImageEdges(
                image_result,
                10,
                [self.red, self.red, self.white],
                [self.red, self.white, self.white],
                [self.white, self.white, self.white]
        )

        image_result = self.proc.crop(self.image.copy(), { "width": 480, "height": 320, "align": 'center', "valign": 'top' })
        self.assertImageEdges(
                image_result,
                10,
                [self.red, self.white, self.green],
                [self.white, self.white, self.white],
                [self.white, self.white, self.white]
        )

        image_result = self.proc.crop(self.image.copy(), { "width": 320, "height": 240, "align": 'right', "valign": 'top' })
        self.assertImageEdges(
                image_result,
                10,
                [self.white, self.green, self.green],
                [self.white, self.white, self.green],
                [self.white, self.white, self.white]
        )
        image_result = self.proc.crop(self.image.copy(), { "width": 320, "height": 360, "align": 'left', "valign": 'middle' })
        self.assertImageEdges(
                image_result,
                10,
                [self.red, self.white, self.white],
                [self.white, self.white, self.white],
                [self.blue, self.white, self.white]
        )

        image_result = self.proc.crop(self.image.copy(), { "width": 320, "height": 240, "align": 'center', "valign": 'middle' })
        self.assertImageEdges(
                image_result,
                10,
                [self.white, self.white, self.white],
                [self.white, self.white, self.white],
                [self.white, self.white, self.white]
        )

        image_result = self.proc.crop(self.image.copy(), { "width": 320, "height": 360, "align": 'right', "valign": 'middle' })
        self.assertImageEdges(
                image_result,
                10,
                [self.white, self.white, self.green],
                [self.white, self.white, self.white],
                [self.white, self.white, self.yellow]
        )
        image_result = self.proc.crop(self.image.copy(), { "width": 320, "height": 240, "align": 'left', "valign": 'bottom' })
        self.assertImageEdges(
                image_result,
                10,
                [self.white, self.white, self.white],
                [self.blue, self.white, self.white],
                [self.blue, self.blue, self.white]
        )

        image_result = self.proc.crop(self.image.copy(), { "width": 480, "height": 320, "align": 'center', "valign": 'bottom' })
        self.assertImageEdges(
                image_result,
                10,
                [self.white, self.white, self.white],
                [self.white, self.white, self.white],
                [self.blue, self.white, self.yellow]
        )

        image_result = self.proc.crop(self.image.copy(), { "width": 320, "height": 240, "align": 'right', "valign": 'bottom' })
        self.assertImageEdges(
                image_result,
                10,
                [self.white, self.white, self.white],
                [self.white, self.white, self.yellow],
                [self.white, self.yellow, self.yellow]
        )

    def test_mirror(self):
        image_result = self.proc.mirror(self.image.copy(), {})
        self.assertImageEdges(
                image_result,
                10,
                [self.green, self.white, self.red],
                [self.white, self.white, self.white],
                [self.yellow, self.white, self.blue]
        )

    def test_flip(self):
        image_result = self.proc.flip(self.image.copy(), {})
        self.assertImageEdges(
                image_result,
                10,
                [self.blue, self.white, self.yellow],
                [self.white, self.white, self.white],
                [self.red, self.white, self.green]
        )

    def test_grayscale(self):
        image_result = self.proc.grayscale(self.image.copy(), {})
        # Asserting primary colors converted to grayscale
        self.assertImageEdges(
                image_result,
                10,
                [76, 255, 149],
                [255, 255, 255],
                [29, 255, 225]
        )

    def test_invert(self):
        image_result = self.proc.invert(self.image.copy(), {})
        self.assertImageEdges(
                image_result,
                10,
                [(0, 255, 255), self.black[0:-1], (255, 0, 255)],
                [self.black[0:-1], self.black[0:-1], self.black[0:-1]],
                [(255, 255, 0), self.black[0:-1], (0, 0, 255)]
        )

    def test_scale(self):
        image_result = self.proc.scale(self.image.copy(), { "height": 80, "width": 60})
        self.assertImageEdges(
                image_result,
                3,
                [self.red, self.white, self.green],
                [self.white, self.white, self.white],
                [self.blue, self.white, self.yellow]
        )
        self.assertNotImageEdges(
                image_result,
                10,
                [self.red, self.white, self.green],
                [self.white, self.white, self.white],
                [self.blue, self.white, self.yellow]
        )

        image_result = self.proc.scale(self.image.copy(), { "height": 640, "width": 120})
        self.assertEqual(image_result.getpixel((10, 20)), (255, 0, 0, 255))
        self.assertEqual(image_result.getpixel((10, 120)), (255, 255, 255, 255))
        self.assertEqual(image_result.getpixel((3, 120)), (255, 0, 0, 255))

    def test_watermark(self):
        watermark_path = os.path.join(os.path.dirname(__file__), 'watermark.png')
        image_result = self.proc.watermark(self.image.copy(), {"watermark_image": watermark_path, "opacity": 0.5})
        self.assertImageEdges(
                image_result,
                1,
                None,
                [self.white, (128, 128, 128, 255), self.white],
                None,
        )
        image_result = self.proc.watermark(self.image.copy(), {"watermark_image": watermark_path, "opacity": 0})
        self.assertImageEdges(
                image_result,
                1,
                None,
                [self.white, self.white, self.white],
                None,
        )
        image_result = self.proc.watermark(self.image.copy(), {"watermark_image": watermark_path, "opacity": 1})
        self.assertImageEdges(
                image_result,
                1,
                None,
                [self.white, self.black, self.white],
                None,
        )
