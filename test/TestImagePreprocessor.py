""" 
Script tests all the methods in the ImagePreprocessing
class
"""
import sys

import unittest
import numpy as np

sys.path.append("./src")
import logger as log
from Config import Config
from ImagePreprocessing import ImagePreprocessing


class TestImagePreprocessor(unittest.TestCase):
    """ 
    Class defining all the methods for testing ImagePreprocessing Class
    ---------------------
    Methods:
        setUp (staticmethod)
            Set up the class
        test_invert_image (staticmethod)
            Tests method invert_image from ImagePreprocessing
        test_binarize_image
            Tests method binarize_image from ImagePreprocessing
        test_noise_removal
            Tests method noise_removal from ImagePreprocessing
        test_change_font
            Tests method change_font from ImagePreprocessing
        test_rmv_border
            Tests method rmv_border from ImagePreprocessing
        test_add_border
            Tests method add_border from ImagePreprocessing
    """

    def setUp(self):
        """ 
        Set up the class
        """
        self.preprocessor = ImagePreprocessing(
            logger=log.get_logger(),
            img=f"{Config(logger=log.get_logger()).folder_test()}/test_image.jpg"
            )

    def test_invert_image(self):
        """ 
        Tests method invert_image from ImagePreprocessing
        """
        result = self.preprocessor.invert_image()
        self.assertIsInstance(
            result,
            np.ndarray,
            "Methods 'invert_image' return value is not a NumPy array")     

    def test_binarize_image(self):
        """ 
        Tests method binarize_image from ImagePreprocessing
        """
        result = self.preprocessor.binarize_image()
        self.assertIsInstance(
            result,
            np.ndarray,
            "Methods 'binarize_image' return value is not a NumPy array")

    def test_noise_removal(self):
        """ 
        Tests method noise_removal from ImagePreprocessing
        """
        result = self.preprocessor.noise_removal()
        self.assertIsInstance(
            result,
            np.ndarray,
            "Methods 'noise_removal' return value is not a NumPy array")

    def test_change_font(self):
        """ 
        Tests method change_font from ImagePreprocessing
        """
        result = self.preprocessor.change_font()
        self.assertIsInstance(
            result,
            np.ndarray,
            "Methods 'change_font' return value is not a NumPy array")

    def test_rmv_border(self):
        """ 
        Tests method rmv_border from ImagePreprocessing
        """
        result = self.preprocessor.rmv_border()
        self.assertIsInstance(
            result,
            np.ndarray,
            "Methods 'rmv_border' return value is not a NumPy array")

    def test_add_border(self):
        """ 
        Tests method add_border from ImagePreprocessing
        """
        result = self.preprocessor.add_border()
        self.assertIsInstance(
            result,
            np.ndarray,
            "Methods 'add_border' return value is not a NumPy array")

if __name__ == '__main__':
    unittest.main()
