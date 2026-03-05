import cv2 as cv   # OpenCV 라이브러리
import sys         # 프로그램 종료를 위해 사용

# 이미지 불러오기
img = cv.imread('soccer.jpg')   # soccer.jpg 이미지를 읽어서 img 변수에 저장

if img is None:
    sys.exit('파일이 존재하지 않습니다.')

# 초기 붓 크기
brush_size = 5

# 마우스 클릭 상태를 저장하는 변수
drawing_left = False   # 왼쪽 버튼 드래그 상태
drawing_right = False  # 오른쪽 버튼 드래그 상태

# 마우스 이벤트 처리 함수
def mouse_event(event, x, y, flags, param):
    global drawing_left, drawing_right, brush_size, img
    # 왼쪽 마우스 버튼을 눌렀을 때
    if event == cv.EVENT_LBUTTONDOWN:
        drawing_left = True
        
    # 오른쪽 마우스 버튼을 눌렀을 때
    elif event == cv.EVENT_RBUTTONDOWN:
        drawing_right = True

    # 왼쪽 마우스 버튼을 뗐을 때
    elif event == cv.EVENT_LBUTTONUP:
        drawing_left = False

    # 오른쪽 마우스 버튼을 뗐을 때
    elif event == cv.EVENT_RBUTTONUP:
        drawing_right = False

    # 마우스를 움직일 때
    elif event == cv.EVENT_MOUSEMOVE:
        if drawing_left:    # 왼쪽 버튼 드래그 중이면 파란색으로 그림
            cv.circle(img, (x, y), brush_size, (255, 0, 0), -1) 
        elif drawing_right: # 오른쪽 버튼 드래그 중이면 빨간색으로 그림
            cv.circle(img, (x, y), brush_size, (0, 0, 255), -1) 


cv.namedWindow('Image Display')     # 이미지 창 생성
cv.setMouseCallback('Image Display', mouse_event)   # 생성한 창에 마우스 이벤트 함수 연결

# 프로그램이 계속 실행되도록 무한 반복
while True:
    cv.imshow('Image Display', img) # 현재 이미지를 화면에 출력
    key = cv.waitKey(1) & 0xFF  # 키보드 입력을 1ms 동안 대기 후 key 변수에 저장
    # '+' 키를 누르면 붓 크기 증가 (최대 15)
    if key == ord('+'):
        brush_size = min(15, brush_size + 1)
    # '-' 키를 누르면 붓 크기 감소 (최소 1)
    elif key == ord('-'):
        brush_size = max(1, brush_size - 1)
    # 'q' 키를 누르면 프로그램 저장 후 종료
    elif key == ord('q'):
        cv.imwrite('paint.jpg', img)
        print("이미지가 저장되었습니다.")
        break

# 모든 OpenCV 창 닫기
cv.destroyAllWindows()

# 이미지 정보 출력
print(type(img))                # img 변수 타입 출력 (보통 <class 'numpy.ndarray'>)
print(img.shape)                # img 이미지 배열의 크기 출력 (높이, 너비, 채널 수)