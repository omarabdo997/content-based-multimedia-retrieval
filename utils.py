import matplotlib.pyplot as plt
import cv2
import numpy as np
from imageai.Detection import ObjectDetection
import os
from numpy import array
from json import loads
from extract_kf import extract_images


def calc_histogram(image):
    """
    calc_histogram
     calculate the histogram of one image
    :param image: the original image 
    :return: hist_base, array of 10 elements with the Noramolized values of image's histogram 
    """
    # hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    #bins' Number of histogrom 
    h_bins = 1
    s_bins = 10
    histSize = [h_bins, s_bins]
    
    #range of histogram hue 0 to 179, saturation 0 to 255
    hue_ranges = [0, 180]
    satr_ranges = [0, 256]
    ranges = hue_ranges + satr_ranges
    
    # Use the 0-th and 1-st channels
    channels = [0, 1]
    
    #calculate the histogram of image
    hist_base = cv2.calcHist([image], channels, None, histSize, ranges, accumulate=False)
    
    #alpha to beta is range of Normalize
    cv2.normalize(hist_base, hist_base, alpha=0, beta=100 , norm_type=cv2.NORM_MINMAX)
    return hist_base


def compare_Hist(hist_input , hist_img):
    """
    compare_Hist
     get a numerical value that express how well two histograms match with each other by Correlation method.
    :param hist_input: the histogram of input image 
    :param hist_img:  the histogram of image from Database
    :return: numerical value of comparing the 2 histograms
    """
    hist_input_1d = hist_input.squeeze()
    hist_img_1d = hist_img.squeeze()

    compare_value = cv2.compareHist(hist_input_1d , hist_img_1d , cv2.HISTCMP_CORREL)
    return compare_value 


def get_objects(path):
    execution_path = os.getcwd()
    detector = ObjectDetection()    
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath( os.path.join(execution_path , "images/resnet50_coco_best_v2.1.0.h5"))
    detector.loadModel()

    # construct output path
    separated_path = path.split(".")
    output_path = path[:-1 - len(separated_path[-1])] + "_detected." + separated_path[-1]
    
    detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , path), output_image_path=os.path.join(execution_path , output_path))

    objects_freq = {}
    for detected_object in detections:
        if detected_object["name"] in objects_freq:
            objects_freq[detected_object["name"]] += 1
        else:
            objects_freq[detected_object["name"]] = 1
    return objects_freq, len(detections)


def compare_object_based(input_frame, stored_frame):
    common_objects = 0.0
    for object_name in input_frame["objects_freq"].keys():
        if object_name in stored_frame.objects_freq:
            common_objects += min(loads(stored_frame.objects_freq)[object_name],
                                input_frame['objects_freq'][object_name])
    if stored_frame.objects_count == 0:
        return 0
    return common_objects / stored_frame.objects_count


def avgColor (img):
    height, width, _ = np.shape(img)
    avg_color_per_row = np.average(img, axis=0)
    avg_colors = np.average(avg_color_per_row, axis=0)
    int_averages = np.array(avg_colors, dtype=np.uint64)
    # for checking 
    average_image = np.zeros((height, width, 3), np.uint8)
    average_image[:] = int_averages
    # cv2.imshow("Avg Color", np.hstack([img, average_image]))
    # plt.show()
    return int_averages

def colourDistance ( avg_img1,  avg_img2):
    rmean = ( avg_img1[0] + avg_img2[0] )/2
    r = float(avg_img1[0]) - float(avg_img2[0])
    g = float(avg_img1[1]) - float(avg_img2[1])
    b = float(avg_img1[2]) - float(avg_img2[2])
    weightR = 2 + rmean/256
    weightG = 4.0
    weightB = 2 + (255-rmean)/256
    colorDis =  np.sqrt(weightR*r*r + weightG*g*g + weightB*b*b)
    maxColDist = 764.8339663572415
    similarity = round(((maxColDist-colorDis)/maxColDist)*100)
    return similarity

def compareVideos(video1_frames, video2_frames, comparisson, threshold):
    common_frames = 0
    for frame in video1_frames:
        for frame2 in video2_frames:
            if (comparisson == "avg_color"):
                similarity = colourDistance(frame[comparisson], frame2.avg_color)
                if similarity > threshold:
                    common_frames += 1
                    break
            if (comparisson == "histogram"):
                similarity = compare_Hist(
                    frame[comparisson], array(frame2.histogram, dtype="float32"))
                if similarity > threshold:
                    common_frames += 1
                    break
    return common_frames / len(video1_frames)
