# 01.sobel_edge_detection.py

* edgeDetectionImage 이미지를 그레이스케일로 변환
* Sobel 필터를 사용하여 x축과 y축 방향의 에지를 검출
* 검출된 에지 강도 이미지를 시각화

---

# 기능

* 이미지를 불러온다.
* BGR 이미지를 RGB로 변환한다 (matplotlib 출력용).
* 이미지를 그레이스케일로 변환한다.
* Sobel 필터를 이용하여 x, y 방향 에지를 검출한다.
* 에지 강도(magnitude)를 계산한다.
* 결과를 uint8 형식으로 변환하여 시각화한다.
* 원본 이미지와 에지 이미지를 나란히 출력한다.

---

# 요구사항

* cv.imread()를 사용하여 이미지를 불러옴
* cv.cvtColor()를 사용하여 그레이스케일로 변환
* cvSobel()을 사용하여 x축(cv.CV_64F, 1, 0)과 y축(cv.CV_64F, 0,1) 방향의 에지를 검출
* cv.magnitude()를 사용하여 에지 강도 계산
* Matplotlib를 사용하여 원본 이미지와 에지 강도 이미지를 나란히 시각화

---

# 핵심 코드 설명

## 1. 라이브러리 불러오기

```python
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
```

* `cv2` : OpenCV 라이브러리
* `numpy` : 수치 연산 (gradient magnitude 계산)
* `matplotlib` : 이미지 시각화

---

## 2. 이미지 불러오기

```python
image_path = 'edgeDetectionImage.jpg'
img = cv.imread(image_path)
```

이미지를 BGR 형식으로 불러온다.

```python
if img is None:
    raise ValueError("이미지를 불러올 수 없습니다. 경로를 확인하세요.")
```

이미지가 없을 경우 오류 처리

---

## 3. BGR → RGB 변환

```python
img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
```

OpenCV는 BGR 형식이므로 matplotlib 출력 시 색상 왜곡 방지를 위해 RGB로 변환한다.

---

## 4. 그레이스케일 변환

```python
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
```

에지 검출은 밝기 정보만 필요하기 때문에 흑백 이미지로 변환한다.

---

## 5. Sobel 필터 적용

```python
sobel_x = cv.Sobel(gray, cv.CV_64F, 1, 0, ksize=3)
sobel_y = cv.Sobel(gray, cv.CV_64F, 0, 1, ksize=3)
```

* `sobel_x` : x 방향 변화량 (세로 경계 검출)
* `sobel_y` : y 방향 변화량 (가로 경계 검출)

---

## 6. 에지 강도(Magnitude) 계산

에지의 전체 강도는 다음과 같이 계산된다.

```
Magnitude = √(Gx² + Gy²)
```

```python
magnitude = cv.magnitude(sobel_x, sobel_y)
```

---

## 7. uint8 변환

```python
magnitude_uint8 = cv.convertScaleAbs(magnitude)
```

* float 값을 0~255 범위의 uint8로 변환
* 시각화를 위해 필요

---

## 8. 결과 시각화

```python
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.title('Original Image')
plt.imshow(img_rgb)
plt.axis('off')

plt.subplot(1, 2, 2)
plt.title('Sobel Edge Magnitude')
plt.imshow(magnitude_uint8, cmap='gray')
plt.axis('off')

plt.tight_layout()
plt.show()
```

---

# 폴더 구조

```
project_folder
│
├ edgeDetectionImage.jpg
├ 01.sobel_edge_detection.py
└ README.md
```

---

# 실행 방법

1. OpenCV 및 matplotlib 설치

```
pip install opencv-python matplotlib
```

2. 프로그램 실행

```
python 01.sobel_edge_detection.py
```

---

# 결과 설명

* 밝은 부분 → 에지가 강한 영역
* 어두운 부분 → 에지가 약한 영역

즉,

* 물체의 경계선
* 윤곽선
* 밝기 변화가 큰 부분

이 강조되어 나타난다.

---

# 주의사항

* 입력 이미지 경로가 올바른지 확인해야 한다.
* Sobel 커널 크기(`ksize`)에 따라 결과가 달라질 수 있다.
* 노이즈가 많은 이미지에서는 에지가 과도하게 검출될 수 있다.
* 필요 시 Gaussian Blur 등을 적용하면 더 안정적인 결과를 얻을 수 있다.

  <img width="1001" height="559" alt="01 sobel_edge_detection 결과" src="https://github.com/user-attachments/assets/a3701cf1-74d7-4a09-afbb-185dc01c8fad" />

