from PIL import Image, ImageOps, ImageEnhance, ImageFile
from django_tits.imageprocs.default import DefaultImageProc

import unittest
import os

class DefaultImageProcTestCase(unittest.TestCase):
    def assertImageEdges(self, image, edge_width, colors_top, colors_middle, colors_bottom):
        width, height = image.size

        for x in range(edge_width):
            # TOP check
            self.assertEqual(image.getpixel((x, x)), colors_top[0])
            self.assertEqual(image.getpixel((int(width/2), x)), colors_top[1])
            self.assertEqual(image.getpixel((width-edge_width+x, edge_width-x)), colors_top[2])

            # MIDDLE check
            self.assertEqual(image.getpixel((x, int(height/2))), colors_middle[0])
            self.assertEqual(image.getpixel(((width/2), int(height/2))), colors_middle[1])
            self.assertEqual(image.getpixel((width-edge_width+x, int(height/2))), colors_middle[2])

            # BOTTOM check
            self.assertEqual(image.getpixel((edge_width-x, height-edge_width+x)), colors_bottom[0])
            self.assertEqual(image.getpixel((int(width/2), height-edge_width+x)), colors_bottom[1])
            self.assertEqual(image.getpixel((width-edge_width+x, height-edge_width+x)), colors_bottom[2])

    @classmethod
    def setUpClass(cls):
        cls.proc = DefaultImageProc()
        cls.black = (0, 0, 0, 255)
        cls.white = (255, 255, 255, 255)

    def test_crop(self):
        image = Image.open(os.path.join(os.path.dirname(__file__), 'test-image.png'))
        image_result = self.proc.crop(image.copy(), { "width": 320, "height": 240, "align": 'left', "valign": 'top' })
        self.assertImageEdges(
                image_result,
                10,
                [self.black, self.black, self.white],
                [self.black, self.white, self.white],
                [self.white, self.white, self.white]
        )

        image_result = self.proc.crop(image.copy(), { "width": 480, "height": 320, "align": 'center', "valign": 'top' })
        self.assertImageEdges(
                image_result,
                10,
                [self.black, self.white, self.black],
                [self.white, self.white, self.white],
                [self.white, self.white, self.white]
        )

        image_result = self.proc.crop(image.copy(), { "width": 320, "height": 240, "align": 'right', "valign": 'top' })
        self.assertImageEdges(
                image_result,
                10,
                [self.white, self.black, self.black],
                [self.white, self.white, self.black],
                [self.white, self.white, self.white]
        )
        image_result = self.proc.crop(image.copy(), { "width": 320, "height": 240, "align": 'left', "valign": 'middle' })
        self.assertImageEdges(
                image_result,
                10,
                [self.black, self.white, self.white],
                [self.white, self.white, self.white],
                [self.black, self.white, self.white]
        )

        image_result = self.proc.crop(image.copy(), { "width": 320, "height": 240, "align": 'center', "valign": 'middle' })
        self.assertImageEdges(
                image_result,
                10,
                [self.white, self.white, self.white],
                [self.white, self.white, self.white],
                [self.white, self.white, self.white]
        )

        image_result = self.proc.crop(image.copy(), { "width": 320, "height": 240, "align": 'right', "valign": 'middle' })
        self.assertImageEdges(
                image_result,
                10,
                [self.white, self.white, self.black],
                [self.white, self.white, self.white],
                [self.white, self.white, self.black]
        )
        image_result = self.proc.crop(image.copy(), { "width": 320, "height": 240, "align": 'left', "valign": 'bottom' })
        self.assertImageEdges(
                image_result,
                10,
                [self.white, self.white, self.white],
                [self.black, self.white, self.white],
                [self.black, self.black, self.white]
        )

        image_result = self.proc.crop(image.copy(), { "width": 480, "height": 320, "align": 'center', "valign": 'bottom' })
        self.assertImageEdges(
                image_result,
                10,
                [self.white, self.white, self.white],
                [self.white, self.white, self.white],
                [self.black, self.white, self.black]
        )

        image_result = self.proc.crop(image.copy(), { "width": 320, "height": 240, "align": 'right', "valign": 'bottom' })
        self.assertImageEdges(
                image_result,
                10,
                [self.white, self.white, self.white],
                [self.white, self.white, self.black],
                [self.white, self.black, self.black]
        )
