""" 
In this file everything about the prediction service
will happen, including OCR and Detection

File is written in pylint standard
"""

import time

import cv2
import tensorflow as tf
import matplotlib.pyplot as plt

import logger as log
from Config import Config
from ImagePreprocessing import ImagePreprocessing


class PredictionService(Config):
    """
    Class defining executing the prediction services like
    OCR and the detection model
    ---------------------
    Methods:
      detection
        Detects the two classes (table, total_price) on
        the given image
      extract_table
        Extracts the detected table from the image 
        for postprocessing. If visualize = True it
        shows the detected BBoxes on the image
      extract_text
        Uses OCR to extract text from total_price image
    """

    def __init__(self, logger):
        super().__init__(logger=logger)
        self.model = tf.saved_model.load(f"{self.folder_res()}/model/saved_model/")
        self.__logger = logger

    def detection(self, img):
        """ 
        Not implemented yet
        """
        orig_image = ImagePreprocessing.model_preprocess(img=img)
        detections = self.model(orig_image)

        return detections

    def extract_table(self, img, confidence: float = 0.75, visualize: bool = False) -> None:
        """ 
        Not implemented yet
        """
        _counter = 0
        _counter = 0

        start_time = time.time()
        detections = self.detection(img=img)
        end_time = time.time()

        self.__logger.debug(
            "Detection model made prediction in %s sec.",
            {end_time-start_time}
            )

        orig_image = cv2.imread(img)
        image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)

        boxes = detections['detection_boxes'][0].numpy()
        scores = detections['detection_scores'][0].numpy()
        classes = detections['detection_classes'][0].numpy().astype(int)

        for box, score, class_id in zip(boxes, scores, classes):
            if score > confidence:
                ymin, xmin, ymax, xmax = box
                ymin = int(ymin * image.shape[0])
                xmin = int(xmin * image.shape[1])
                ymax = int(ymax * image.shape[0])
                xmax = int(xmax * image.shape[1])

                # Should only be used for debugging
                if visualize:
                    # Draw bounding box
                    color = (0, 255, 0)
                    image = cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, thickness=2)

                    # Display class label and score
                    if class_id == 1:
                        label = f'Table {score:.2f}'
                    else:
                        label = f'total_price {score:.2f}'

                    font = cv2.FONT_HERSHEY_SIMPLEX

                    # Replace within the function
                    font_scale = 1
                    font_thickness = 2
                    text_origin = (xmin, ymin - 10)
                    image = cv2.putText(
                        image,
                        label,
                        text_origin,
                        font,
                        font_scale,
                        color,
                        font_thickness,
                        cv2.LINE_AA
                        )

                else:
                    img_cut = orig_image[ymin:ymax, xmin:xmax]
                    splitter = lambda img : str(img).split('/')[-1].split('.')[0]

                    if class_id == 1:
                        plt.imsave(f"{self.folder_src()}/temp/table_{splitter(img)}.png", img_cut)
                        plt.imsave(f"{self.folder_src()}/temp/table_{splitter(img)}.png", img_cut)
                    else:
                        img_cut = ImagePreprocessing(img=img_cut, logger=self.__logger).add_border()
                        plt.imsave(f"{self.folder_src()}/temp/price_{splitter(img)}.png", img_cut)
                        plt.imsave(f"{self.folder_src()}/temp/price_{splitter(img)}.png", img_cut)

                    _counter += 1
                    _counter += 1

        if visualize:
            fig, ax = plt.subplots(figsize=(20, 15))
            plt.imshow(image)
            plt.axis('off')
            plt.show()


    def extract_text(self, img: str, reader) -> float:
        """ 
        Not implemented yet
        """
        total: float = 0

        replace_dict = {
            "[": "",
            "]": "",
            "," : ".",
            " " : "",
            "_" : "",
            "-" : "",
            "/" : ""
        }

        start_time = time.time()

        extracted_text = reader.recognize(f"{self.folder_src()}/temp/{img}")[0]
        print(extracted_text)
        # extracted_text = reader.readtext(
        #     f"{self.folder_src()}/temp/{img}", detail=0, batch_size = 12
        #     )[0]

        for key, value in replace_dict.items():
            if key in extracted_text:
                extracted_text = extracted_text.replace(key, value)
        total = float(extracted_text)

        end_time = time.time()
        self.__logger.debug(
            f"OCR model extracted ({total}) and calculated total value in %s sec.",
            end_time-start_time
            )

        return total


if __name__ == "__main__":
    ps = PredictionService(logger=log.get_logger())
    ps.extract_table(img=r"C:\Git_Repos\PDF-To-Invoice\res\data\Receipt_2023-12-23_003514.jpg",
                     confidence=0.7,
                     visualize=True)
