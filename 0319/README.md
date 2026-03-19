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


# 02.canny_hough_line_detection.py

* dabo 이미지에 캐니 에지 검출을 사용하여 에지 맵 생성
* 허프 변환을 사용하여 이미지에서 직선 검출
* 검출된 직선을 원본 이미지에서 빨간색으로 표시

---

# 기능

* 이미지를 불러온다.
* 이미지를 그레이스케일로 변환한다.
* Gaussian Blur를 적용하여 노이즈를 제거한다.
* Canny Edge Detection으로 에지를 검출한다.
* Hough Transform을 이용하여 직선을 검출한다.
* 검출된 직선을 원본 이미지 위에 그린다.
* 원본 이미지와 결과 이미지를 나란히 시각화한다.

---

# 요구사항

* cv.Canny()를 사용하여 에지 맵 생성
* cv.HoughtLinesP()를 사용하여 직선 검출
* cv.line()을 사용하여 검출된 직선을 원본 이미지에 그림
* Matplotlib를 사용하여 원본 이미지와 직선이 그려진 이미지를 나란히 시각화

---

# 핵심 코드 설명

## 1. 라이브러리 불러오기

```python
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
```

* `cv2` : OpenCV 라이브러리
* `numpy` : 수치 계산 (허프 변환 파라미터)
* `matplotlib` : 이미지 시각화

---

## 2. 이미지 로드 및 전처리

```python
img = cv.imread('dabo.jpg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
```

* 이미지를 불러온 후 그레이스케일로 변환한다.

---

## 3. Gaussian Blur (노이즈 제거)

```python
blurred = cv.GaussianBlur(gray, (5, 5), 0)
```

* 커널 크기: (5, 5)
* 노이즈 제거 및 에지 검출 안정화

---

## 4. Canny Edge Detection

```python
edges = cv.Canny(blurred, 100, 200)
```

* `100` : 낮은 임계값
* `200` : 높은 임계값

에지(윤곽선)를 검출하는 단계

---

## 5. Hough Transform (직선 검출)

```python
lines = cv.HoughLinesP(
    edges,
    rho=1,
    theta=np.pi/180,
    threshold=140,
    minLineLength=90,
    maxLineGap=10
)
```

### 주요 파라미터 설명

* `rho` : 거리 해상도 (픽셀 단위)
* `theta` : 각도 해상도 (라디안)
* `threshold` : 직선으로 판단할 최소 투표 수
* `minLineLength` : 최소 직선 길이
* `maxLineGap` : 선 사이 최대 허용 간격

→ 불필요한 짧은 선 제거 + 주요 직선만 검출

---

## 6. 직선 그리기

```python
img_copy = img.copy()
```

원본 이미지 복사

```python
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv.line(img_copy, (x1, y1), (x2, y2), (0, 0, 255), 2)
```

* 검출된 직선을 빨간색으로 표시
* 두께: 2

---

## 7. 결과 시각화

```python
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
```

* 원본 이미지 vs 직선 검출 결과 비교

---

# 폴더 구조

```
project_folder
│
├ dabo.jpg
├ 02.canny_hough_line_detection.py
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
python 02.canny_hough_line_detection.py
```

---

# 결과 설명

* 빨간 선 → 검출된 직선
* 주요 구조(건물, 도로, 경계선 등)가 강조됨

---

# 주의사항

* 입력 이미지 경로가 올바른지 확인해야 한다.
* Canny 임계값에 따라 에지 검출 결과가 달라진다.
* Hough Transform 파라미터에 따라 직선 검출 결과가 크게 달라진다.
* 노이즈가 많은 경우 Gaussian Blur를 더 강하게 적용할 수 있다.
* 너무 많은 선이 검출되면 `threshold`, `minLineLength` 값을 증가시켜야 한다.

<img width="512" height="282" alt="image" src="https://github.com/user-attachments/assets/0b0abc46-7486-4419-82c5-80da52e05f03" />

<img width="1200" height="660" alt="02 canny_hough_line_detection 결과" src="https://github.com/user-attachments/assets/a90f3e0e-897b-4254-af45-cc6212f06008" />


# 03.grabcut_segmentation.py

* coffee cup 이미지로 사용자가 지정한 사각형 영역을 바탕으로 GrabCut 알고리즘을 사용하여 객체 추출
* 객체 추출 결과를 마스크 형태로 시각화
* 원본 이미지에서 배경을 제거하고 객체만 남은 이미지 출력

---

# 기능

* 이미지를 불러온다.
* BGR 이미지를 RGB로 변환한다 (matplotlib 출력용).
* 초기 사각형 영역(ROI)을 설정한다.
* GrabCut 알고리즘을 수행하여 전경/배경을 분리한다.
* 마스크를 후처리하여 배경을 제거한다.
* 원본 이미지, 마스크, 결과 이미지를 시각화한다.

---

# 요구사항

* cv.grabCut()를 사용하여 대화식 분할을 수행
* 초기 사각형 영역은 (x, y, width, height) 형식으로 설정
* 마스크를 사용하여 원본 이미지에서 배경을 제거
* matplotlib를 사용하여 원본 이미지, 마스크 이미지, 배경 제거 이미지 세 개를 나란히 시각화

---

# 핵심 코드 설명

## 1. 라이브러리 불러오기

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt
```

* `cv2` : OpenCV 라이브러리
* `numpy` : 마스크 처리 및 배열 연산
* `matplotlib` : 결과 시각화

---

## 2. 이미지 불러오기

```python
img = cv2.imread('coffee cup.jpg')
```

이미지를 BGR 형식으로 불러온다.

```python
if img is None:
    print("이미지를 찾을 수 없습니다. 파일명을 확인해주세요.")
```

이미지가 없을 경우 오류 메시지 출력

---

## 3. BGR → RGB 변환

```python
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
```

OpenCV는 BGR 형식이므로 matplotlib 출력 시 RGB로 변환한다.

---

## 4. 초기 사각형 영역 설정

```python
h, w = img.shape[:2]
rect = (int(w*0.05), int(h*0.05), int(w*0.9), int(h*0.9))
```

* 이미지의 가장자리 5%를 제외한 영역을 전경 후보로 설정
* `(x, y, width, height)` 형식

---

## 5. GrabCut 초기화

```python
mask = np.zeros(img.shape[:2], np.uint8)
bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)
```

* `mask` : 픽셀 분류 결과 저장
* `bgdModel` : 배경 모델
* `fgdModel` : 전경 모델

---

## 6. GrabCut 실행

```python
cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
```

* `5` : 반복 횟수
* `GC_INIT_WITH_RECT` : 사각형 기반 초기화

---

## 7. 마스크 후처리

```python
mask2 = np.where((mask == 0) | (mask == 2), 0, 1).astype('uint8')
```

* 0, 2 → 배경
* 1, 3 → 전경

---

## 8. 배경 제거 이미지 생성

```python
result = img_rgb * mask2[:, :, np.newaxis]
```

마스크를 적용하여 전경만 남긴다.

---

## 9. 결과 시각화

```python
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.imshow(img_rgb)
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.imshow(mask2, cmap='gray')
plt.title('Mask Image')
plt.axis('off')

plt.subplot(1, 3, 3)
plt.imshow(result)
plt.title('Background Removed')
plt.axis('off')

plt.tight_layout()
plt.show()
```

* 원본 이미지
* 마스크 이미지
* 배경 제거 결과

---

# 폴더 구조

```
project_folder
│
├ coffee cup.jpg
├ 03.grabcut_segmentation.py
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
python 03.grabcut_segmentation.py
```

---

# 결과 설명

* 흰색 영역 → 전경
* 검은색 영역 → 배경

결과 이미지에서는 배경이 제거되고 **객체(커피컵)**만 남게 된다.

---

# 주의사항

* 입력 이미지 경로 및 파일명을 정확히 입력해야 한다.
* 초기 사각형(rect)에 따라 결과가 크게 달라진다.
* 복잡한 배경에서는 완벽하게 분리되지 않을 수 있다.
* 반복 횟수(iteration)를 늘리면 더 정확한 결과를 얻을 수 있다.

<img width="1498" height="563" alt="03 grabcut_segmentation 결과" src="https://github.com/user-attachments/assets/1463cb66-3806-4324-9cd7-917d64144b42" />
