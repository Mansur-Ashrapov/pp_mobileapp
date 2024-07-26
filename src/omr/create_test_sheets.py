import cv2
import numpy as np
import qrcode
import os


current_file = os.path.realpath(__file__)
cur_dir = os.path.dirname(current_file)


def get_sheet_with_qr(data):
    #convert to grayscale
    
    #read the blank test sheet
    sheet = cv2.imread(cur_dir + "/test_sheet.png")

    sheet = cv2.cvtColor(sheet, cv2.COLOR_BGR2GRAY)

    #scaling constants
    x_offset = 330
    y_offset = 10


    #make QR code
    qr_img = qrcode.make(data)
    qr_img = np.float32(qr_img)

    #crop and resize QR code
    qr_img = qr_img[40:260, 40:250]
    qr_img = cv2.resize(qr_img, (0, 0), fx=0.7, fy=0.7)

    #calculate coordinates where the QR code should be placed
    y1, y2 = y_offset, y_offset + qr_img.shape[0]
    x1, x2 = x_offset, x_offset + qr_img.shape[1]

    #place the QR code on the sheet
    sheet[y1:y2, x1:x2] = qr_img * 255

    # cv2.imwrite("test" + ".png", sheet)
    return sheet

# get_sheet_with_qr(data='1 4')