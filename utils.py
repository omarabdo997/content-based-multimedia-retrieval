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


def compare_object_based(input_frame, stored_frame):
    common_objects = 0.0
    for object_name in input_frame.objects_freq.keys():
        if object_name in stored_frame.objects_freq:
            common_objects += min(stored_frame.objects_freq[object_name], 
                                  input_frame.objects_freq[object_name])
    return common_objects / stored_frame.total_count


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

def colourDistance ( img1,  img2):
    rmean = ( img1[0] + img2[0] )/2
    r = float(img1[0]) - float(img2[0])
    g = float(img1[1]) - float(img2[1])
    b = float(img1[2]) - float(img2[2])
    weightR = 2 + rmean/256
    weightG = 4.0
    weightB = 2 + (255-rmean)/256
    colorDis =  np.sqrt(weightR*r*r + weightG*g*g + weightB*b*b)
    maxColDist = 764.8339663572415;
    similarity = round(((maxColDist-colorDis)/maxColDist)*100)
    return similarity