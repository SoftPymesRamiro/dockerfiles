# -*- coding: utf-8 -*-
#!/usr/bin/env python
#########################################################
# Utils module
# All credits by SoftPymes Plus
# 
# Date: 21-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"


from base64 import b64encode, b64decode
from io import BytesIO
from PIL import Image


class ImagesConverter(object):
    '''
    ImagesConverter Allow convert images from (PNG and JPG formats)
    '''
    @staticmethod
    def img_convert(img):
        """
            Convert the upload imagen from encode (base64) format
            to save file.
            :param
        """
        result = None
        if img is not None or img != '':
            image_parts = img.split(',', 1)
            ext_img = image_parts[0].replace("data:image/", "").replace(";base64", "")
            img_str_parts = img[img.index(',')+1:]

            if img_str_parts != "null" and img_str_parts != "undefined":
                my_image = Image.open(BytesIO(b64decode(img_str_parts)))
                output = BytesIO()
                quality_val = 90
                my_image.format = my_image.format.upper()
                if my_image.format == "PNG":
                    my_image.save(output, format="png", quality=quality_val)
                    result = b64encode(output.getvalue())
                if my_image.format == "JPEG" or my_image.format == "JPG":
                    my_image.save(output, format="jpeg", quality=quality_val)
                    result = b64encode(output.getvalue())

        return result

    @staticmethod
    def img_convert_to_base64(img):
        """
        Decode the image in utf-8 codification
        """
        try:
            return "" if img is None else "{0}".format(img.decode("utf-8"))
        except UnicodeDecodeError:
            return "" if img is None else "{0}".format(b64encode(img).decode('utf-8'))
