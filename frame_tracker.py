# -*- coding:utf-8 -*-
import cv2
import iou

def list_compare(detect_list,track_list,thred = 0):
    new_dected = []
    r = []
    for detect in detect_list:
        a = (detect[0], detect[1], detect[0] + detect[2], detect[1] + detect[3])
        for track in track_list:
            b = (track[0],track[1],track[0]+track[2],track[1]+track[3])
            r += [iou.iou(a,b)]
            print('iou')
            print(r)
        if (r and max(r) <= thred) or (not r ) :
            new_dected.append(detect)
    return new_dected

def init_tracker(detected_img,list):
    tracker = cv2.TrackerKCF_create()
    tracker_list = []
    for detect in list:
        tracker.init(detected_img, tuple(detect))
    # 跟踪器列表
        tracker_list.append(tracker)
    return tracker_list


def update_tracker(img,tracker_list):
    detected_img=img.copy()
    j = 0
    result_list = []
    for tracker in tracker_list:
        # bbox  # (x,y.w,h)
        ok, bbox = tracker.update(detected_img)
        result_list.append(bbox)
        if ok:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(detected_img, p1, p2, (0, 0, 255))
            cv2.putText(detected_img, '%d' % (j), p1, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            print("Object[{}] 被跟踪 at [{}, {},{},{}] \r"
                  .format(j, int(bbox[0]), int(bbox[1]), int(bbox[2]),	int(bbox[3])), )
        j += 1
    return detected_img,result_list