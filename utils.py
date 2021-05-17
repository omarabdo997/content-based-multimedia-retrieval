import matplotlib.pyplot as plt
import cv2
import numpy as np
from imageai.Detection import ObjectDetection
import osv

def calc_histogram(image):
    """
    calc_histogram
     calculate the histogram of one image
    :param image: the original image 
    :return: hist_base, array of 10 elements with the Noramolized values of image's histogram 
    """
    #bins' Number of histogrom 
    h_bins = 1
    s_bins = 10
    histSize = [h_bins, s_bins]
    
    #range of histogram
    h_ranges = [0, 180]
    s_ranges = [0, 256]
    ranges = h_ranges + s_ranges
    
    # Use the 0-th and 1-st channels
    channels = [0, 1]
    
    #calculate the histogram of image
    hist_base = cv2.calcHist([image], channels, None, histSize, ranges, accumulate=False)
    
    #alpha to beta is range of Normalize
    cv2.normalize(hist_base, hist_base, alpha=0, beta=100, norm_type=cv2.NORM_MINMAX)
    return hist_base


def compare_Hist(hist_input , hist_img):
    """
    compare_Hist
     get a numerical value that express how well two histograms match with each other by Correlation method.
    :param hist_input: the histogram of input image 
    :param hist_img:  the histogram of image from Database
    :return: "true", when the value of compression is larger then or equal 0.5
    :return: "false", when the value of compression is smaller then 0.5
    """
    compare_value = cv2.compareHist(hist_input, hist_img, cv2.HISTCMP_CORREL)
    # if compare_value >= 0.5:
    #     return "true" 
    # else:
    #     return "false"
    return compare_value 

# ###to test  calc_histogram && compare_Hist functions
# src_base = cv2.imread('test_images/Histogram_Comparison_Source_0.jpg')
# src_test1 = cv2.imread('test_images/Histogram_Comparison_Source_1.jpg')
# src_test2 = cv2.imread('test_images/Histogram_Comparison_Source_2.jpg')

# h1 = calc_histogram(src_base)
# h2 = calc_histogram(src_test1)
# print (compare_Hist(h1,h2))  


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
