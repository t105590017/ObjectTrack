import sys
import dlib
from cv2 import cv2

tracker = dlib.correlation_tracker()
cap = cv2.VideoCapture(0)
start_flag = True   # 為第一禎
selection = None   # 滑鼠畫出的方塊
track_window = None   # 追蹤區域
drag_start = None   # 滑鼠是否拖動

# 滑鼠點擊
def OnMouseClicked(event, x, y, flags, param):
    global selection, track_window, drag_start
    if event == cv2.EVENT_LBUTTONDOWN:
        drag_start = (x, y)
        track_window = None
    if drag_start:
        xMin = min(x, drag_start[0])
        yMin = min(y, drag_start[1])
        xMax = max(x, drag_start[0])
        yMax = max(y, drag_start[1])
        selection = (xMin, yMin, xMax, yMax)
    if event is cv2.EVENT_LBUTTONUP:
        drag_start = None
        track_window = selection
        selection = None

if __name__ == '__main__':
    cv2.namedWindow("image", cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback("image", OnMouseClicked)

    while(1):
        ret, frame = cap.read() 

        if start_flag is True:
            while True:
                img_first = frame.copy()
                if track_window:
                    cv2.rectangle(img_first, (track_window[0], track_window[1]), (track_window[2], track_window[3]), (0,0,255), 1)
                elif selection:
                    cv2.rectangle(img_first, (selection[0], selection[1]), (selection[2], selection[3]), (0,0,255), 1)
                cv2.imshow("image", img_first)
                if cv2.waitKey(5) == 13:
                    break
            start_flag = False
            tracker.start_track(frame, dlib.rectangle(track_window[0], track_window[1], track_window[2], track_window[3]))
        else:
            tracker.update(frame)

        box_predict = tracker.get_position()
        cv2.rectangle(frame,(int(box_predict.left()),int(box_predict.top())),(int(box_predict.right()),int(box_predict.bottom())),(0,255,255),1)
        cv2.imshow("image", frame)
        

        # MouseKeyDown
        key = cv2.waitKey(1)
        if key == 27:
            break
        if key == 32:
            start_flag = True

    cap.release()
    cv2.destroyAllWindows()