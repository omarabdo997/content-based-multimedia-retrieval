from sqlalchemy.sql.expression import null
import utils
from model import (db_init, insert_image, insert_video as insert_video_model, Image, Video)
import shutil
import cv2
from numpy import array
from extract_kf import extract_images
import os


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
    
    def insert_video(self, video_url):
        images_urls = extract_images(video_url)
        input_video = {
            "url": video_url,
            "key_frames": [],
        }
        for image_url in images_urls:
            image = cv2.imread(image_url)
            if image is None:
                return "Please enter a valid image url!"
            avg_color = utils.avgColor(image)
            histogram = utils.calc_histogram(image).tolist()
            img = {
                "url": image_url,
                "avg_color": avg_color.tolist(),
                "histogram": histogram,
                "objects_freq": {},
                "objects_count": 0,
            }
            input_video["key_frames"].append(img)
        print(input_video)
        result = insert_video_model(self.session, input_video)
        return result["success"]

    def search_for_images(self, input_url, criteria):
        input_image = cv2.imread(input_url)
        if input_image is None:
            return "Please enter a valid image url!"

        images = self.session.query(Image).filter_by(video_id=None)
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
                if(similarity > 0.9):
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
    
    def search_for_videos(self, input_url, criteria):
        input_images = extract_images(input_url)
        input_images_processed = []
        videos = self.session.query(Video).all()
        videos_arr = []
        for input_url in input_images:
            input_image = cv2.imread(input_url)
            if input_image is None:
                return "Please enter a valid image url!"

            if criteria == "avg_color":
                input_avg_color = utils.avgColor(input_image)
                input_images_processed.append({
                    "avg_color": input_avg_color
                })

            elif criteria == "histogram":
                hist = utils.calc_histogram(input_image)
                input_images_processed.append({
                    "histogram": hist
                })
        for video in videos:
            images = video.images
            if (criteria == "avg_color"):
                similarity = utils.compareVideos(input_images_processed, images, "avg_color", 90)
            if (criteria == "histogram"):
                similarity = utils.compareVideos(input_images_processed, images, "histogram", 0.9)
            if(similarity > 0.8):
                    videos_arr.append({"url": video.url, "similarity": similarity})
        videos_arr = sorted(
            videos_arr, key=lambda i: i["similarity"], reverse=True)
        shutil.rmtree(os.path.dirname(input_images[0]))
        videos_urls = [i["url"] for i in videos_arr]
        print("video urls", videos_urls)
        return videos_urls    

#controller = Controller()

# print(controller.insert_image("./images/city.jpeg"))
# print(controller.session.query(Image).all())
# print(controller.search_for_images("./images/city2.jpeg", "avg_color"))
# print(controller.session.query(Video).all()[3].images)
#controller.search_for_videos("/home/omar/Videos/loading.mp4", "avg_color")