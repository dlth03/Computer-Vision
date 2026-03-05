import cv2 as cv             # OpenCV 라이브러리를 cv라는 이름으로 불러오기
import numpy as np           # 배열 처리를 위한 NumPy 라이브러리 불러오기
import sys                   # 시스템 관련 기능 사용을 위해 sys 모듈 불러오기

# 이미지 로드
img = cv.imread('soccer.jpg')

if img is None :                
    sys.exit('파일이 존재하지 않습니다.')  

# 이미지를 그레이스케일로 변환
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  
gray_small=cv.resize(gray, dsize=(0,0), fx=0.5, fy=0.5)

# 원본 이미지와 그레이스케일 이미지를 가로로 연결
gray_small = np.hstack((img, cv.cvtColor(gray, cv.COLOR_GRAY2BGR)))

# 결과 화면 출력
cv.imshow('Image Display', gray_small) 
cv.waitKey()   
cv.destroyAllWindows()  # 모든 OpenCV 창을 닫음

# 결과 이미지 저장
cv.imwrite('gray_small.jpg', gray_small)

# 이미지 정보 출력
print(type(img))                     # img 변수 타입 출력 (보통 <class 'numpy.ndarray'>)
print(img.shape)                    # img 이미지 배열의 크기 출력 (높이, 너비, 채널 수)