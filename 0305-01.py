import cv2 as cv             # OpenCV 라이브러리
import numpy as np           # 배열 처리를 위한 NumPy 라이브러리 불러오기
import sys                   # 프로그램 종료를 위해 사용

# 이미지 불러오기
img = cv.imread('soccer.jpg')   # 'soccer.jpg' 파일을 BGR 컬러 이미지로 읽어 img 변수에 저장

# 이미지가 존재하지 않을 경우 프로그램 종료
if img is None :  
    sys.exit('파일이 존재하지 않습니다.') 
    
# 그레이스케일 변환
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # BGR 컬러 이미지를 그레이스케일(흑백) 이미지로 변환하여 gray 변수에 저장
gray_small=cv.resize(gray, dsize=(0,0), fx=0.5, fy=0.5)

# 원본 이미지와 그레이스케일 이미지를 가로로 연결
gray_small = np.hstack((img, cv.cvtColor(gray, cv.COLOR_GRAY2BGR))) # 원본 컬러 이미지, 그레이스케일 이미지는 채널이 1개이므로, 3채널(BGR) 이미지로 다시 변환하여 연결 가능하게 함
# 두 이미지를 좌우로 붙여서 하나의 이미지로 만듦

# 결과 화면 출력
cv.imshow('Image Display', gray_small)  # 'Image Display' 창에 gray_small 이미지(원본 + 그레이스케일)를 표시
cv.waitKey()                          # 키 입력을 무한 대기, 아무 키나 누르면 다음으로 진행
cv.destroyAllWindows()                # 모든 OpenCV 창을 닫음

# 결과 이미지 저장
cv.imwrite('gray_small.jpg', gray_small)
print("이미지를 'gray_small.jpg'로 저장했습니다.")

# 이미지 정보 출력
print(type(img))                     # img 변수 타입 출력 (보통 <class 'numpy.ndarray'>)
print(img.shape)                    # img 이미지 배열의 크기 출력 (높이, 너비, 채널 수)