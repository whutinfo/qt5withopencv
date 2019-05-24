import cv2
import numpy as np


def detectobj(diff,frame_lwpCV):
    point_list = []
    img = frame_lwpCV.copy()
    _,contours, hierarchy = cv2.findContours(diff.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  # 该函数计算一幅图像中目标的轮廓
    #cv2.drawContours(frame_lwpCV, contours, -1, (0, 255, 0), 3)
    i = 0

    for c in contours:  # shape : (10, 1, 2)

        countour_size = np.size(c, axis=0)  # 轮廓点个数
        # print(countour_size)

        if countour_size > 40:  # 根据轮廓点的多少判断是否是噪声
            x, y, w, h = cv2.boundingRect(c)
            # x_min1 = np.min(c[:, :, 0])
            # x_max1 = np.max(c[:, :, 0])
            # y_min1 = np.min(c[:, :, 1])
            # y_max1 = np.max(c[:, :, 1])
            #
            # w = x_max1 - x_min1
            # h = y_max1 - y_min1

            #cv2.rectangle(frame_lwpCV, (x_min1, y_min1), (x_max1, y_max1), (0, 255, 0), 2)  # 绿色识别框
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)  # 绿色识别框
            # 将所有符合的轮廓边框点加入识别框list
            #cv2.putText(frame_lwpCV, '%d' % (i),(x_min1, y_min1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(img, '%d' % (i), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            print("Object[{}] detected at [{}, {},{},{}] \r".format(i, x, y,w,h), )
            point_list.append((x,y,w,h))
            i += 1

    return point_list,img,contours



def contours2pos(contours,New_frame_lwpCV,cf,pts):
    # drawing coutour in frame and return posistions
    contour_checklist=np.array([])
    pos = []

    for c in contours:
        # cal contour area:
        # cv2.contourArea(c)
        # cv2.circle(New_frame_lwpCV, (int((x+xp)/2),int((y+yp)/2)), 7, (255, 255, 255), -1)

        #if cv2.contourArea(c)> 500:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(New_frame_lwpCV, (x, y), (x + w, y + h), (0, 0, 255), 2)
        contour_checklist = np.append(contour_checklist,cv2.contourArea(c))
        pos.append([x,y,x+w,y+h])
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # cv2.circle(New_frame_lwpCV, center, 5, (0, 0, 255), -1)
        pts.append(center)
        # contour_checklist += [cv2.contourArea(c)]
        print(contour_checklist)

    if pos:
        pos.pop(0)

    return contour_checklist,pos,pts


def drawline(frame_lwpCV):
    New_frame_lwpCV = frame_lwpCV.copy()
    contour_checklist, pos, pts = contours2pos(contours, New_frame_lwpCV, cf, pts)