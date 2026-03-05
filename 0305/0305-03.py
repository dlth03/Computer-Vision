import cv2 as cv
import sys

# 이미지 불러오기
img = cv.imread('soccer.jpg')

if img is None:
    sys.exit('파일이 존재하지 않습니다.')

img_copy = img.copy() # 원본 이미지 복사

# 마우스 좌표 변수(초기값)
start_x, start_y = -1, -1 # 드래그 시작 좌표
end_x, end_y = -1, -1   # 드래그 종료 좌표

drawing = False # 드레그 상태 여부
roi = None # 선택된  ROI 영역 저장 변수


# 마우스 이벤트 처리 함수 
def mouse_event(event, x, y, flags, param):
    global start_x, start_y, end_x, end_y, drawing, img, img_copy, roi

    # 사용자가 클릭한 시작점에서 드래그하여 사각형 영역 선택
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        start_x, start_y = x, y
    # 드래그 상태
    elif event == cv.EVENT_MOUSEMOVE:
        if drawing:
            img = img_copy.copy()
            cv.rectangle(img, (start_x, start_y), (x, y), (0,255,0), 2) # 현재 마우스 위치까지 사각형 표시

    # 마우스를 놓으면 해당 영역을 잘라내 출력
    elif event == cv.EVENT_LBUTTONUP:
        drawing = False     # 드래그 종료
        end_x, end_y = x, y     # 종료 좌표 저장

        # 좌표 정렬
        x1 = min(start_x, end_x)
        x2 = max(start_x, end_x)
        y1 = min(start_y, end_y)
        y2 = max(start_y, end_y)

        # 선택된 영역 추출
        cv.rectangle(img, (x1, y1), (x2, y2), (0,255,0), 2)

        # ROI 추출
        roi = img_copy[y1:y2, x1:x2]

        # ROI 창에 출력
        if roi.size != 0:
            cv.imshow("ROI", roi)


cv.namedWindow("Image") # 이미지 창 생성
cv.setMouseCallback("Image", mouse_event)  # cv.setMouseCallback()을사용하여마우스이벤트를처리

# 프로그램을 계속 실행하기 위한 무한 루프
while True:

    # 현재 이미지를 화면에 출력
    cv.imshow("Image", img)

    key = cv.waitKey(1) & 0xFF  # 키보드 입력을 1ms 동안 대기

    # r 키를누르면 리셋
    if key == ord('r'):
        img = img_copy.copy()
        roi = None

    # s 키를누르면 선택한 영역을 파일로 저장
    elif key == ord('s'):
        if roi is not None and roi.size != 0:
            cv.imwrite("0305-03/roi.jpg", roi) # ROI 이미지 저장
            print("ROI 이미지 저장 완료")

    # q 키를 누르면 프로그램 종료
    elif key == ord('q'):
        break


cv.destroyAllWindows()