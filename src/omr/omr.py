import numpy as np
import cv2
import os

from . import utils

from .grade_paper import ProcessPage

# from app.models.schemas.testresult import TestResult 

current_file = os.path.realpath(__file__)
cur_dir = os.path.dirname(current_file)


def recognize_test(image):
    # ret, image = cap.read()
    ratio = len(image[0]) / 500.0 #used for resizing the image
    original_image = image.copy() #make a copy of the original image

    #find contours on the smaller image because it's faster
    image = cv2.resize(image, (0,0), fx=1/ratio, fy=1/ratio)

    #gray and filter the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #bilateral filtering removes noise and preserves edges
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    #find the edges
    edged = cv2.Canny(gray, 250, 300)

    #find the contours
    contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]

    #sort the contours
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    #find the biggest contour
    biggestContour = utils.get_biggest_contour(contours)

    #used for the perspective transform
    points = []
    desired_points = [[0,0], [425, 0], [425, 550], [0, 550]] #8.5in by 11in. paper

    #convert to np.float32
    desired_points = np.float32(desired_points)

    #extract points from contour
    if biggestContour is not None:
        for i in range(0, 4):
            points.append(biggestContour[i][0])

    #find midpoint of all the contour points for sorting algorithm
    mx = sum(point[0] for point in points) / 4
    my = sum(point[1] for point in points) / 4

    #alogrithm for sorting points clockwise        
    def clockwise_sort(x):
        return (np.arctan2(x[0] - mx, x[1] - my) + 0.5 * np.pi) % (2*np.pi)


    #sort points
    points.sort(key=clockwise_sort, reverse=True)

    #convert points to np.float32
    points = np.float32(points)

    #resize points so we can take the persepctive transform from the
    #original image giving us the maximum resolution
    points *= ratio
    answers = 1
    if biggestContour is not None:
        #create persepctive matrix
        M = cv2.getPerspectiveTransform(points, desired_points)
        #warp persepctive
        paper = cv2.warpPerspective(original_image, M, (425, 550))
        answers, student_id, paper = ProcessPage(paper)
        if answers is not None:
            paper = cv2.resize(paper, (0, 0), fx=0.5, fy=0.5)

            y_offset=x_offset=0
            y1, y2 = y_offset, y_offset + paper.shape[0]
            x1, x2 = x_offset, x_offset + paper.shape[1]

            alpha_s = paper[:, :, 2] / 255.0
            alpha_l = 1.0 - alpha_s

            for c in range(0, 3):
                image[y1:y2, x1:x2, c] = (
                    alpha_s * paper[:, :, c] +
                    alpha_l * image[y1:y2, x1:x2, c]
                )
        codes = codes[0]
        return answers, student_id, image
    return answers, student_id, image

    #draw the contour
    # if biggestContour is not None:
    #     if answers != -1:
    #         cv2.drawContours(image, [biggestContour], -1, (0, 255, 0), 3)
    #         # print(answers)
    #         # if codes is not None:
    #         #     print(codes)
    #     else:
    #         cv2.drawContours(image, [biggestContour], -1, (0, 0, 255), 3)

    # cv2.imshow("Original Image", cv2.resize(image, (0, 0), fx=0.8, fy=0.8))
    # cv2.imshow("Image", paper)

    # cv2.waitKey(0)

# img = cv2.imread(cur_dir + "/test2.png")
# recognize_test(img)