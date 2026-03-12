import cv2                   # OpenCV 라이브러리
import numpy as np           # 배열 처리를 위한 NumPy 라이브러리 불러오기

# 이미지 읽기
img = cv2.imread('rose.png')

# 이미지 크기 (높이, 너비)
h, w = img.shape[:2]

# 이미지 중심
center = (w // 2, h // 2)

# 회전 + 스케일 (30도, 0.8배)
M = cv2.getRotationMatrix2D(center, 30, 0.8)

# 평행이동 추가 (x +80, y -40)
M[0, 2] += 80
M[1, 2] += -40

# 변환 적용
result = cv2.warpAffine(img, M, (w, h))

# 결과 출력
cv2.imshow("Original", img)                              # 원본
cv2.imshow("Rotated + Scaled + Translated", result)      # 변환된 이미지

cv2.waitKey(0)          # 키 입력 대기
cv2.destroyAllWindows() # 창 닫기