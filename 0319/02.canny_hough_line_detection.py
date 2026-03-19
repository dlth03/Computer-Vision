import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# 1. 이미지 로드 및 전처리
img = cv.imread('dabo.jpg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# 가우시안 블러로 노이즈 제거
blurred = cv.GaussianBlur(gray, (5, 5), 0)

# 2. 캐니 에지 (threshold1=100, threshold2=200)
edges = cv.Canny(blurred, 100, 200)

# 3. 허프 변환 - 파라미터 조정으로 주요 직선만 검출
lines = cv.HoughLinesP(
    edges, 
    rho=1, 
    theta=np.pi/180, 
    threshold=140,      # 높일수록 확실한 직선만 검출
    minLineLength=90,  # 100픽셀 이하 짧은 선 제거
    maxLineGap=10       # 10픽셀 이상 끊기면 별개의 선으로 처리
)

# 4. 결과 그리기 (빨간색, 두께 2)
img_copy = img.copy()
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv.line(img_copy, (x1, y1), (x2, y2), (0, 0, 255), 2)

# 5. 시각화
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
plt.title('Original')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(cv.cvtColor(img_copy, cv.COLOR_BGR2RGB))
plt.title('Optimized Result')
plt.axis('off')

plt.tight_layout()
plt.show()