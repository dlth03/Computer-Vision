import cv2 as cv             # OpenCV 라이브러리
import numpy as np           # 배열 처리를 위한 NumPy 라이브러리 불러오기
import sys                   # 프로그램 종료를 위해 사용

# 이미지 로드
img = cv.imread('soccer.jpg')    # soccer.jpg 이미지를 읽어서 img 변수에 저장

if img is None :            # 이미지가 없으면 프로그램 종료   
    sys.exit('파일이 존재하지 않습니다.')  

# 이미지를 그레이스케일로 변환
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  
gray_small=cv.resize(gray, dsize=(0,0), fx=0.5, fy=0.5)  # 가로, 세로를 0.5배로 줄임

# 원본 이미지와 그레이스케일 이미지를 가로로 연결
gray_small = np.hstack((img, cv.cvtColor(gray, cv.COLOR_GRAY2BGR)))

# 결과 화면 출력
cv.imshow('Image Display', gray_small) # 결과 이미지를 화면에 출력
cv.waitKey()   # 키보드 입력이 들어올 때까지 대기
cv.destroyAllWindows()  # 모든 OpenCV 창을 닫음

# 결과 이미지 저장
cv.imwrite('gray_small.jpg', gray_small)

# 이미지 정보 출력
print(type(img))                     # img 변수 타입 출력 (보통 <class 'numpy.ndarray'>)
print(img.shape)                    # img 이미지 배열의 크기 출력 (높이, 너비, 채널 수)