import cv2 as cv
import sys

# 이미지 불러오기
img = cv.imread('soccer.jpg')

if img is None:
    sys.exit('파일이 존재하지 않습니다.')

img_copy = img.copy()

# 마우스 좌표 변수(초기값)
start_x, start_y = -1, -1
end_x, end_y = -1, -1

drawing = False
roi = None


def mouse_event(event, x, y, flags, param):
    global start_x, start_y, end_x, end_y, drawing, img, img_copy, roi

    # 사용자가클릭한시작점에서드래그하여사각형을그리며영역을선택
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        start_x, start_y = x, y

    elif event == cv.EVENT_MOUSEMOVE:
        if drawing:
            img = img_copy.copy()
            cv.rectangle(img, (start_x, start_y), (x, y), (0,255,0), 2)

    # 마우스를놓으면해당영역을잘라내서별도의창에출력
    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        end_x, end_y = x, y

        # 좌표 정렬 (중요)
        x1 = min(start_x, end_x)
        x2 = max(start_x, end_x)
        y1 = min(start_y, end_y)
        y2 = max(start_y, end_y)

        cv.rectangle(img, (x1, y1), (x2, y2), (0,255,0), 2)

        # ROI 추출
        roi = img_copy[y1:y2, x1:x2]

        # ROI 창에 출력
        if roi.size != 0:
            cv.imshow("ROI", roi)


cv.namedWindow("Image")
cv.setMouseCallback("Image", mouse_event)  # cv.setMouseCallback()을사용하여마우스이벤트를처리


while True:

    cv.imshow("Image", img)

    key = cv.waitKey(1) & 0xFF

    # r 키를누르면영역선택을리셋하고처음부터다시선택
    if key == ord('r'):
        img = img_copy.copy()
        roi = None

    # s 키를누르면선택한영역을이미지파일로저장
    elif key == ord('s'):
        if roi is not None and roi.size != 0:
            cv.imwrite("0305-03/roi.jpg", roi)
            print("ROI 이미지 저장 완료")

    # q 키 → 종료
    elif key == ord('q'):
        break


cv.destroyAllWindows()