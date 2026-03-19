import cv2 as cv                    # OpenCV 라이브러리 불러오기
import numpy as np                  # 수치 연산 라이브러리 (magnitude 계산에 사용됨)
import matplotlib.pyplot as plt     # 시각화를 위한 matplotlib

# 이미지 불러오기
image_path = 'edgeDetectionImage.jpg'  # 사용할 이미지 경로
img = cv.imread(image_path)            # 이미지 읽기 (BGR 형식)

# 이미지가 정상적으로 로드되었는지 확인
if img is None:
    raise ValueError("이미지를 불러올 수 없습니다. 경로를 확인하세요.")

# OpenCV는 BGR → RGB 변환
img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)

# 그레이스케일 변환
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)      # 컬러 → 흑백 변환

# Sobel 필터로 x, y 방향 에지 검출
sobel_x = cv.Sobel(gray, cv.CV_64F, 1, 0, ksize=3)
# 세로 경계 검출(입력 이미지, 출력 데이터 타입, dx=1 → x 방향, dy=0 → y 방향 미적용, 커널 크기 (3x3)) 
sobel_y = cv.Sobel(gray, cv.CV_64F, 0, 1, ksize=3)
# 가로 경계 검출(입력 이미지, 출력 데이터 타입, dx=0 → x 방향 미적용, dy=1 → y 방향, 커널 크기 (3x3)) 

# 에지 강도(magnitude) 계산
magnitude = cv.magnitude(sobel_x, sobel_y)

# uint8로 변환 (시각화를 위해)
magnitude_uint8 = cv.convertScaleAbs(magnitude)     # float64 → uint8 변환 (0~255)

# 결과 시각화
plt.figure(figsize=(10, 5))

# 원본 이미지
plt.subplot(1, 2, 1)            # 1행 2열 중 첫 번째
plt.title('Original Image')     # 제목
plt.imshow(img_rgb)             # 이미지 출력
plt.axis('off')                 # 축 제거 

# 에지 결과 이미지
plt.subplot(1, 2, 2)                            # 1행 2열 중 두 번째
plt.title('Sobel Edge Magnitude')               # 제목
plt.imshow(magnitude_uint8, cmap='gray')        # 에지 이미지 흑백 출력
plt.axis('off')

plt.tight_layout()          # 레이아웃 자동 정렬
plt.show()                  # 화면 출력
