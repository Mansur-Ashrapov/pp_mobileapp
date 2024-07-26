import cv2
import numpy as np

def get_biggest_contour(contours):
    # loop over our contours
    for contour in contours:
        # approximate the contour
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

        #return the biggest 4 sided approximated contour
        if len(approx) == 4:
            return approx
        
#alogrithm for sorting points clockwise
def clockwise_sort(x, mx, my):
    return (np.arctan2(x[0] - mx, x[1] - my) + 0.5 * np.pi) % (2*np.pi)
