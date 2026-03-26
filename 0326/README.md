# 01_sift_feature_detection.py

* 주어진 이미지(mot_color70.jpg)를 이용하여 SIFT(Scale-Invariant Feature Transform) 알고리즘을 사용하여 특징점을 검출하고 이를 시각화

---

# 기능

* 이미지를 불러온다.
* BGR 이미지를 RGB로 변환한다 (matplotlib 출력용).
* SIFT 알고리즘을 사용하여 특징점을 검출한다.
* 특징점의 descriptor(128차원 벡터)를 계산한다.
* 특징점의 위치, 크기, 방향을 시각화한다.
* 원본 이미지와 결과 이미지를 나란히 출력한다.
* 특징점 개수 및 descriptor 정보를 콘솔에 출력한다.

---

# 요구사항

* cv.SIFT_create()를 사용하여 SIFT 객체를 생성
* detectAndCompute()를 사용하여 특징점을 검출
* cv.drawKeypoints()를 사용하여 특징점을 이미지에 시각화
* matplotlib을 이용하여 원본 이미지와 특징점이 시각화된 이미지를 나란히 출력

---

# 핵심 코드 설명

## 1. 라이브러리 불러오기

```python
import cv2 as cv
import matplotlib.pyplot as plt
```

* `cv2` : OpenCV 라이브러리
* `matplotlib` : 이미지 시각화

---

## 2. 이미지 불러오기

```python
img = cv.imread('mot_color70.jpg')
```

이미지를 BGR 형식으로 불러온다.

```python
if img is None:
    print("이미지를 불러올 수 없습니다. 파일명을 확인하세요.")
    exit()
```

이미지가 없을 경우 프로그램 종료

---

## 3. BGR → RGB 변환

```python
img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
```

OpenCV는 BGR 형식이므로 matplotlib 출력 시 RGB로 변환한다.

---

## 4. SIFT 객체 생성

```python
sift = cv.SIFT_create(nfeatures=100)
```

* `nfeatures=100` : 최대 특징점 개수 제한

---

## 5. 특징점 검출 및 Descriptor 계산

```python
keypoints, descriptors = sift.detectAndCompute(img, None)
```

* `keypoints` : 특징점 위치 정보
* `descriptors` : 각 특징점의 특징 벡터 (128차원)

---

## 6. 특징점 시각화

```python
img_keypoints = cv.drawKeypoints(
    img,
    keypoints,
    None,
    color=(0, 255, 255),
    flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
)
```

* 특징점 위치 + 크기 + 방향까지 함께 표시
* 색상: 노란색

---

## 7. RGB 변환 (시각화용)

```python
img_keypoints_rgb = cv.cvtColor(img_keypoints, cv.COLOR_BGR2RGB)
```

---

## 8. 결과 시각화

```python
plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.imshow(img_rgb)
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(img_keypoints_rgb)
plt.title(f'SIFT Keypoints ({len(keypoints)})')
plt.axis('off')

plt.tight_layout()
plt.show()
```

* 원본 이미지 vs 특징점 결과 비교

---

## 9. 콘솔 출력

```python
print("검출된 특징점 개수:", len(keypoints))
```

특징점 개수 출력

```python
if descriptors is not None:
    print("descriptor shape:", descriptors.shape)
```

* descriptor shape: `(특징점 개수, 128)`

---

# 폴더 구조

```
project_folder
│
├ mot_color70.jpg
├ 01_sift_feature_detection.py
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
python 01_sift_feature_detection.py
```

---

# 결과 설명

* 원형 또는 화살표 형태 → 특징점
* 크기 → 특징점의 스케일
* 방향 → 특징점의 방향 정보

→ 이미지에서 중요한 부분(코너, 패턴, 텍스처)이 강조된다.

---

# 주의사항

* 입력 이미지 경로 및 파일명을 정확히 입력해야 한다.
* SIFT는 연산량이 비교적 크기 때문에 속도가 느릴 수 있다.
* `nfeatures` 값을 조정하면 특징점 개수를 변경할 수 있다.
* descriptor는 항상 128차원 벡터로 생성된다.

<img width="1400" height="663" alt="01_sift_feature_detection 결과" src="https://github.com/user-attachments/assets/b703f793-c705-4fd0-b594-102fa37f900b" />
<img width="260" height="49" alt="01_sift_feature_detection 콘솔" src="https://github.com/user-attachments/assets/c01b5357-c892-4963-8ecb-0b640c06ffad" />

---
# 02_sift_feature_matching.py

* 두 개의 이미지(mot_color70.jpg, mot_color83.jpg)를 입력받아 SIFT 특징점 기반으로 매칭을 수행하고 결과를 시각화

---

# 기능

* 두 이미지를 불러온다.
* BGR 이미지를 RGB로 변환한다 (matplotlib 출력용).
* SIFT 알고리즘을 이용하여 각 이미지의 특징점을 검출한다.
* descriptor를 이용하여 특징점 간 매칭을 수행한다.
* Lowe's Ratio Test를 적용하여 좋은 매칭만 선택한다.
* 상위 매칭 결과를 시각화한다.
* 특징점 개수 및 매칭 정보를 콘솔에 출력한다.

---

# 요구사항

* cv.imread()를 사용하여 두 개의 이미지를 불러옴
* cv.SIFT_create()를 사용하여 특징점을 추출
* cv.BFMatcher() 또는 cv.FlannBasedMatcher()를 사용하여 두 영상 간 특징점을 매칭
* cv.drawMatches()를 사용하여 매칭 결과를 시각화
* matplotlib을 이용하여 매칭 결과를 출력

---

# 핵심 코드 설명

## 1. 라이브러리 불러오기

```python
import cv2 as cv
import matplotlib.pyplot as plt
```

* `cv2` : OpenCV 라이브러리
* `matplotlib` : 이미지 시각화

---

## 2. 이미지 불러오기

```python
img1 = cv.imread('mot_color70.jpg')
img2 = cv.imread('mot_color83.jpg')
```

두 개의 이미지를 불러온다.

```python
if img1 is None or img2 is None:
    print("이미지를 불러올 수 없습니다.")
    exit()
```

이미지가 없을 경우 프로그램 종료

---

## 3. BGR → RGB 변환

```python
img1_rgb = cv.cvtColor(img1, cv.COLOR_BGR2RGB)
img2_rgb = cv.cvtColor(img2, cv.COLOR_BGR2RGB)
```

matplotlib 출력용 변환

---

## 4. SIFT 객체 생성

```python
sift = cv.SIFT_create(nfeatures=200)
```

* 특징점 최대 개수 제한

---

## 5. 특징점 검출 및 Descriptor 계산

```python
keypoints1, descriptors1 = sift.detectAndCompute(img1, None)
keypoints2, descriptors2 = sift.detectAndCompute(img2, None)
```

* 특징점 위치 + descriptor 계산

---

## 6. BFMatcher 생성

```python
bf = cv.BFMatcher(cv.NORM_L2)
```

* SIFT는 실수형 descriptor → `NORM_L2` 사용

---

## 7. KNN 매칭 수행

```python
matches = bf.knnMatch(descriptors1, descriptors2, k=2)
```

* 각 특징점에 대해 가장 가까운 2개 후보 선택

---

## 8. Lowe's Ratio Test

```python
good_matches = []

for m, n in matches:
    if m.distance < 0.6 * n.distance:
        good_matches.append(m)
```

* 잘못된 매칭 제거
* 정확한 매칭만 선택

---

## 9. 매칭 정렬 및 선택

```python
good_matches = sorted(good_matches, key=lambda x: x.distance)
good_matches = good_matches[:20]
```

* distance가 작은 순으로 정렬
* 상위 20개만 선택

---

## 10. 매칭 결과 시각화

```python
img_matches = cv.drawMatches(
    img1,
    keypoints1,
    img2,
    keypoints2,
    good_matches,
    None,
    flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
)
```

```python
img_matches_rgb = cv.cvtColor(img_matches, cv.COLOR_BGR2RGB)
```

---

## 11. 결과 출력

```python
plt.figure(figsize=(16, 8))
plt.imshow(img_matches_rgb)
plt.title(f'SIFT Feature Matching ({len(good_matches)} Good Matches)')
plt.axis('off')
plt.tight_layout()
plt.show()
```

---

## 12. 콘솔 출력

```python
print("첫 번째 이미지 특징점 개수:", len(keypoints1))
print("두 번째 이미지 특징점 개수:", len(keypoints2))
print("knn 매칭 개수:", len(matches))
print("좋은 매칭 개수:", len(good_matches))
```

```python
if descriptors1 is not None:
    print("descriptors1 shape:", descriptors1.shape)

if descriptors2 is not None:
    print("descriptors2 shape:", descriptors2.shape)
```

---

# 폴더 구조

```
project_folder
│
├ mot_color70.jpg
├ mot_color83.jpg
├ 02_sift_feature_matching.py
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
python 02_sift_feature_matching.py
```

---

# 결과 설명

* 선으로 연결된 점 → 매칭된 특징점
* 선이 많을수록 두 이미지가 유사함
* distance가 작을수록 더 정확한 매칭

---

# 주의사항

* 두 이미지가 비슷한 장면이어야 매칭이 잘 된다.
* Ratio Test의 기준값(0.6)에 따라 결과가 달라진다.
* 너무 많은 매칭이 나오면 상위 일부만 시각화하는 것이 좋다.
* SIFT는 연산량이 많아 속도가 느릴 수 있다.

<img width="1599" height="860" alt="02_sift_feature_matching 결과" src="https://github.com/user-attachments/assets/53e0f3f6-c5c5-4a06-9edc-82b8e3ee886c" />
<img width="293" height="126" alt="02_sift_feature_matching 콘솔" src="https://github.com/user-attachments/assets/668722c2-0bae-4757-87ee-61766fe0f2a7" />

---
# 03_image_alignment_homography.py

* SIFT 특징점을 사용하여 두 이미지 간 대응점을 찾고, 이를 바탕으로 호모그래피를 계산하여 하나의 이미지 위에 정렬
* 샘플파일로 img1.jpg, img2.jpg, img3.jpg 중 2개를 선택

---

# 기능

* 두 이미지를 불러온다.
* 이미지를 그레이스케일로 변환한다.
* SIFT를 이용하여 특징점을 검출하고 descriptor를 계산한다.
* BFMatcher + KNN 매칭을 수행한다.
* Lowe’s Ratio Test를 통해 좋은 매칭만 선택한다.
* RANSAC을 이용하여 호모그래피 행렬을 계산한다.
* warpPerspective를 이용하여 이미지 정합을 수행한다.
* 불필요한 영역을 crop하여 결과를 정리한다.
* 매칭 결과와 정합 결과를 시각화한다.
* 특징점, 매칭, 호모그래피 정보를 콘솔에 출력한다.

---

# 요구사항

* cv.imread()를 사용하여 두 개의 이미지를 불러옴
* cv.SIFT_create()를 사용하여 특징점을 검출
* cv.BFMatcher()와 knnMatch()를 사용하여 특징점을 매칭하고, 좋은 매칭점만 선별
* cv.findHomography()를 사용하여 호모그래피 행렬을 계산
* cv.warpPerspective()를 사용하여 한 이미지를 변환하여 다른 이미지와 정렬
* 변환된 이미지(Warped Image)와 특징점 매칭 결과(Matching Result)를 나란히 출력

---

# 핵심 코드 설명

## 1. 라이브러리 불러오기

```python
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
```

* `cv2` : OpenCV 라이브러리
* `numpy` : 좌표 및 행렬 계산
* `matplotlib` : 결과 시각화

---

## 2. 이미지 불러오기

```python
img1 = cv.imread('img2.jpg')  # 변환될 이미지
img2 = cv.imread('img1.jpg')  # 기준 이미지
```

```python
if img1 is None or img2 is None:
    print("이미지를 불러올 수 없습니다.")
    exit()
```

---

## 3. 그레이스케일 변환

```python
gray1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
gray2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
```

특징점 검출은 밝기 정보 기반으로 수행

---

## 4. SIFT 특징점 검출

```python
sift = cv.SIFT_create(nfeatures=300)
keypoints1, descriptors1 = sift.detectAndCompute(gray1, None)
keypoints2, descriptors2 = sift.detectAndCompute(gray2, None)
```

---

## 5. BFMatcher + KNN 매칭

```python
bf = cv.BFMatcher(cv.NORM_L2)
matches = bf.knnMatch(descriptors1, descriptors2, k=2)
```

---

## 6. Lowe's Ratio Test

```python
good_matches = []

for m, n in matches:
    if m.distance < 0.7 * n.distance:
        good_matches.append(m)
```

잘못된 매칭 제거

---

## 7. 대응점 추출

```python
src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
```

---

## 8. 호모그래피 계산 (RANSAC)

```python
H, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)
```

* 이상치(outlier) 제거
* 최소 4개 이상의 매칭 필요

---

## 9. 이미지 변환 (Warping)

```python
warped_img = cv.warpPerspective(img1, H, (w1 + w2, max(h1, h2)))
```

* img1을 img2 기준으로 변환

---

## 10. 이미지 합성 및 Crop

```python
result_img[0:h2, 0:w2] = img2
```

```python
coords = cv.findNonZero(gray_result)
x, y, w, h = cv.boundingRect(coords)
cropped_result = result_img[y:y+h, x:x+w]
```

불필요한 검은 영역 제거

---

## 11. 매칭 결과 시각화

```python
match_result = cv.drawMatches(...)
```

상위 30개 매칭만 표시

---

## 12. 결과 시각화

```python
plt.figure(figsize=(18, 8))

plt.subplot(1, 2, 1)
plt.imshow(match_result_rgb)
plt.title('Matching Result')

plt.subplot(1, 2, 2)
plt.imshow(cropped_result_rgb)
plt.title('Warped Image (Image Alignment)')
```

---

## 13. 콘솔 출력

```python
print("좋은 매칭 개수:", len(good_matches))
print("호모그래피 행렬 H:\n", H)
```

---

# 폴더 구조

```
project_folder
│
├ img1.jpg
├ img2.jpg
├ 03_image_alignment_homography.py
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
python 03_image_alignment_homography.py
```

---

# 결과 설명

* 왼쪽 → 특징점 매칭 결과
* 오른쪽 → 정합된 이미지 결과

→ 두 이미지가 하나의 장면처럼 이어진다.

---

# 주의사항

* 최소 4개 이상의 좋은 매칭이 필요하다.
* 이미지가 너무 다르면 정합이 실패할 수 있다.
* Ratio Test 기준(0.7)에 따라 결과가 달라진다.
* RANSAC threshold 값에 따라 정합 품질이 달라진다.
* 정합 후 경계 부분이 어색할 수 있다.

<img width="1803" height="862" alt="03_image_alignment_homography 결과" src="https://github.com/user-attachments/assets/81d2106d-ee66-478c-9b9d-cb93484b6ad3" />
<img width="539" height="287" alt="03_image_alignment_homography 콘솔" src="https://github.com/user-attachments/assets/5b163a4e-3b7d-423f-807a-6d726a7fabee" />

  
