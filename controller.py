import utils
from model import (db_init, insert_image, insert_video, Image, Video)

import cv2
from numpy import array


class Controller:
    def __init__(self):
        self.session = db_init()

    def insert_image(self, image_url):
        image = cv2.imread(image_url)
        if image is None:
            return "Please enter a valid image url!"
        avg_color = utils.avgColor(image)
        print(avg_color)
        histogram = utils.calc_histogram(image).tolist()
        objects_freq, objects_count = utils.get_objects(image_url)
        img = {
            "url": image_url,
            "avg_color": avg_color.tolist(),
            "histogram": histogram,
            "objects_freq": objects_freq,
            "objects_count": objects_count,
        }
        result = insert_image(self.session, img)
        return result["success"]

    def search_for_images(self, input_url, criteria):
        input_image = cv2.imread(input_url)
        if input_image is None:
            return "Please enter a valid image url!"

        images = self.session.query(Image).all()
        images_arr = []

        if criteria == "avg_color":
            input_avg_color = utils.avgColor(input_image)
            for image in images:
                similarity = utils.colourDistance(
                    input_avg_color.tolist(), image.avg_color)
                print("similarity", similarity)
                if (similarity > 90):
                    images_arr.append({"url": image.url, "similarity": similarity})

        elif criteria == "histogram":
            hist = utils.calc_histogram(input_image)
            for image in images:
                similarity = utils.compare_Hist(
                    hist, array(image.histogram, dtype="float32"))
                print("similarity", similarity)
                if(similarity > 0.8):
                    images_arr.append({"url": image.url, "similarity": similarity})

        elif criteria == "objects":
            objects_freq, objects_count = utils.get_objects(input_url)
            input_frame = {"objects_freq": objects_freq,
                           "objects_count": objects_count}
            for image in images:
                similarity = utils.compare_object_based(input_frame, image)
                if(similarity > 0.6):
                    images_arr.append({"url": image.url, "similarity": similarity})

        images_arr = sorted(
            images_arr, key=lambda i: i["similarity"], reverse=True)
        images_urls = [i["url"] for i in images_arr]
        return images_urls


# controller = Controller()

# print(controller.insert_image("./images/city.jpeg"))
# print(controller.session.query(Image).all())
# print(controller.search_for_images("./images/city2.jpeg", "avg_color"))