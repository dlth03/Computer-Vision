# 0312-01.py

* 이미지에서 체크보드 코너를 검출하고 실제 좌표와 이미지 좌표의 대응 관계를 이용하여 카메라 파라미터 추정
* 체크보드 패턴이 촬영된 여러 장의 이미지를 이용하여 카메라의 내부 행렬과 왜곡 계수를 계산하여 왜곡 보정

---

# 기능

* 체크보드 이미지(calibration_images/left*.jpg)를 불러온다.
* cv2.findChessboardCorners()를 사용하여 체크보드 코너를 검출한다.
* 검출된 코너 좌표를 이용하여 카메라 캘리브레이션을 수행한다.
* cv2.calibrateCamera()를 사용하여 Camera Matrix와 Distortion Coefficients를 계산한다.
* cv2.undistort()를 사용하여 렌즈 왜곡을 보정한 이미지를 출력한다.
* 원본 이미지와 왜곡 보정 이미지를 비교하여 결과를 확인할 수 있다.

---

# 요구사항

* 모든 이미지에서 체크보드 코너를 검출
* 체크 보드의 실제 좌표와 이미지에서 찾은 코너 좌표를 구성
* cv2.calibrateCamera()를 사용하여 카메라 내부 행렬 k와 왜곡 계수를 구함
* cv2.undistort()를 사용하여 왜곡 보정한 결과를 시각화
---

# 핵심 코드 설명

## 1. 라이브러리 불러오기

```python
import cv2
import numpy as np
import glob
```

* cv2 : OpenCV 라이브러리
* numpy : 배열 및 수치 계산을 위한 라이브러리
* glob : 특정 패턴의 파일을 검색하기 위한 라이브러리

---

## 2. 체크보드 설정

```python
CHECKERBOARD = (9, 6)
square_size = 25.0
```

* CHECKERBOARD : 체크보드 내부 코너 개수 (가로 9, 세로 6)
* square_size : 체크보드 한 칸의 실제 크기 (25mm)

체크보드의 실제 좌표를 생성하여 3D 공간 좌표 기준을 설정한다.

---

## 3. 코너 정밀화 조건 설정

```python
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
```

코너 위치를 더 정확하게 찾기 위한 반복 조건이다.

* 최대 반복 횟수 : 30
* 오차 허용 범위 : 0.001

---

## 4. 실제 좌표 생성 (3D 좌표)

```python
objp = np.zeros((CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
objp *= square_size
```

체크보드는 평면이므로 z = 0으로 설정된다.
이 좌표는 체크보드의 실제 위치(3D 좌표)를 의미한다.

---

## 5. 좌표 저장 리스트

```python
objpoints = []
imgpoints = []
```

* objpoints : 실제 3D 좌표 저장
* imgpoints : 이미지에서 검출된 2D 좌표 저장

---

## 6. 캘리브레이션 이미지 불러오기

```python
images = glob.glob("calibration_images/left*.jpg")
```

calibration_images 폴더에서 left로 시작하는 모든 jpg 파일을 불러온다.

---

## 7. 체크보드 코너 검출

```python
ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)
```

이미지에서 체크보드 코너를 검출한다.

* ret : 코너 검출 성공 여부
* corners : 검출된 코너 좌표

---

## 8. 코너 정밀화

```python
corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
```

초기 코너 좌표를 기반으로 더 정확한 위치를 계산한다.

---

## 9. 코너 시각화

```python
cv2.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)
```

검출된 코너 위치를 이미지에 표시하여 체크보드 검출 결과를 확인할 수 있다.

---

## 10. 카메라 캘리브레이션

```python
ret, K, dist, rvecs, tvecs = cv2.calibrateCamera(
    objpoints,
    imgpoints,
    img_size,
    None,
    None
)
```

체크보드의 3D 실제 좌표와 이미지의 2D 좌표를 이용하여 카메라 파라미터를 계산한다.

---

## 11. Camera Matrix 출력

```python
print("Camera Matrix K:")
print(K)
```

카메라 내부 행렬 구조

```
K =
[ fx  0  px
  0  fy  py
  0   0   1 ]
```

* fx, fy : focal length
* px, py : principal point

---

## 12. Distortion Coefficients 출력

```python
print("\nDistortion Coefficients:")
print(dist)
```

렌즈 왜곡 계수

```
[k1 k2 p1 p2 k3]
```

* k1, k2, k3 : Radial distortion
* p1, p2 : Tangential distortion

---

## 13. 이미지 왜곡 보정

```python
dst = cv2.undistort(img, K, dist, None, newcameramtx)
```

계산된 카메라 파라미터를 이용하여 렌즈 왜곡을 보정한 이미지를 생성한다.

---

## 14. 결과 비교 출력

```python
cv2.imshow("Original", img)
cv2.imshow("Undistorted", dst)
```

* Original : 원본 이미지
* Undistorted : 왜곡 보정 이미지

두 이미지를 비교하여 캘리브레이션 결과를 확인할 수 있다.

---

# 폴더 구조

```
project_folder
│
├ calibration_images
│   ├ left01.jpg
│   ├ left02.jpg
│   ├ left03.jpg
│   ├ left04.jpg
│   ├ ...
│   └ left13.jpg
│
├ 01.Calibration.py
└ README.md
```

---

# 실행 방법

1. OpenCV 설치

```
pip install opencv-python
```

2. 프로그램 실행

```
python 01.Calibration.py
```

---

# 주의사항

* 체크보드 코너가 제대로 검출되지 않으면 캘리브레이션이 수행되지 않는다.
* 여러 각도에서 촬영된 체크보드 이미지를 사용할수록 더 정확한 카메라 파라미터를 얻을 수 있다.
<img width="390" height="90" alt="image" src="https://github.com/user-attachments/assets/202337fa-84a2-45c8-ab48-baad3679d41b" />

<img width="1318" height="507" alt="스크린샷 2026-03-12 123400" src="https://github.com/user-attachments/assets/ef3daff2-42b3-48e5-bca0-06a514b4cc74" />


# 0312-02.py

* 한 장의 이미지에 회전, 크기 조절, 평행 이동을 적용

---

# 기능

* 이미지 파일(`rose.png`)을 불러온다.
* 이미지 중심을 기준으로 회전 변환을 수행한다.
* 회전과 동시에 이미지 크기를 조절한다.
* 변환된 이미지를 x, y 방향으로 평행이동한다.
* 원본 이미지와 변환된 이미지를 화면에 출력하여 결과를 비교한다.

---

# 요구사항

* 이미지의 중심 기준으로 **+30도 회전**
* 회전과 동시에 **크기를 0.8로 조절**
* 그 결과를 **x축 방향으로 +80px, y축 방향으로 -40px 만큼 평행이동**

---

# 핵심 코드 설명

## 1. 라이브러리 불러오기

```python
import cv2
import numpy as np
```

* `cv2` : OpenCV 라이브러리
* `numpy` : 배열 및 수치 계산을 위한 라이브러리

---

## 2. 이미지 불러오기

```python
img = cv2.imread('rose.png')
```

`cv2.imread()`를 사용하여 `rose.png` 이미지를 불러온다.

이미지는 NumPy 배열 형태로 저장된다.

---

## 3. 이미지 크기 구하기

```python
h, w = img.shape[:2]
```

이미지 배열에서 높이(height)와 너비(width)를 가져온다.

* `h` : 이미지 높이
* `w` : 이미지 너비

---

## 4. 이미지 중심 좌표 계산

```python
center = (w // 2, h // 2)
```

이미지의 중심 좌표를 계산한다.

* `(w // 2, h // 2)`
* 정수 나눗셈(`//`)을 사용하여 중심 픽셀 좌표를 구한다.

이 중심 좌표를 기준으로 회전을 수행한다.

---

## 5. 회전 및 스케일 변환 행렬 생성

```python
M = cv2.getRotationMatrix2D(center, 30, 0.8)
```

`cv2.getRotationMatrix2D()`는 회전과 스케일 변환을 위한 **아핀 변환 행렬(Affine Transformation Matrix)**을 생성한다.

구성

```
cv2.getRotationMatrix2D(회전 중심, 회전 각도, 스케일)
```

* 회전 중심 : `center`
* 회전 각도 : **30도**
* 스케일 : **0.8**

즉 이미지 중심을 기준으로 **30도 회전하면서 크기를 80%로 축소**한다.

---

## 6. 평행이동 추가

```python
M[0, 2] += 80
M[1, 2] += -40
```

변환 행렬의 이동 성분을 수정하여 평행이동을 추가한다.

* `+80` : x축 방향으로 **80px 이동**
* `-40` : y축 방향으로 **40px 위로 이동**

---

## 7. 아핀 변환 적용

```python
result = cv2.warpAffine(img, M, (w, h))
```

`cv2.warpAffine()`를 사용하여 이미지에 변환 행렬을 적용한다.

구성

```
cv2.warpAffine(입력 이미지, 변환 행렬, 출력 이미지 크기)
```

* 입력 이미지 : `img`
* 변환 행렬 : `M`
* 출력 크기 : `(w, h)`

---

## 8. 결과 출력

```python
cv2.imshow("Original", img)
cv2.imshow("Rotated + Scaled + Translated", result)
```

* `Original` : 원본 이미지
* `Rotated + Scaled + Translated` : 변환된 이미지

두 이미지를 비교하여 변환 결과를 확인할 수 있다.

---

## 9. 프로그램 종료

```python
cv2.waitKey(0)
cv2.destroyAllWindows()
```

* `cv2.waitKey(0)` : 키 입력이 있을 때까지 창 유지
* `cv2.destroyAllWindows()` : 모든 OpenCV 창 닫기

---

# 폴더 구조

```
project_folder
│
├ rose.png
├ 0312-02.py
└ README.md
```

---

# 실행 방법

1. OpenCV 설치

```
pip install opencv-python
```

2. 프로그램 실행

```
python 0312-02.py
```

---

# 실행 결과

프로그램 실행 시 다음과 같은 두 개의 창이 출력된다.

* **Original** : 원본 이미지
* **Rotated + Scaled + Translated** : 회전, 크기 조절, 평행이동이 적용된 이미지

두 이미지를 비교하여 변환 결과를 확인할 수 있다.

<img width="2388" height="816" alt="스크린샷 2026-03-12 123830" src="https://github.com/user-attachments/assets/343d39d5-5872-45fb-a299-e762058c1f2f" />


# 0312-03.py

* 같은 장면을 왼쪽 카메라와 오른쪽 카메라에서 촬영한 두 장의 이미지를 이용해 깊이를 추정
* 두 이미지에서 같은 물체가 얼마나 옆으로 이동해 보이는지 계산하여 물체가 카메라에서 얼마나 떨어져 있는지(depth)를 구할 수 있음

---

# 기능

* 좌/우 스테레오 이미지를 불러온다.
* 이미지를 그레이스케일로 변환한다.
* `cv2.StereoBM_create()`를 사용하여 Disparity Map을 계산한다.
* Disparity 값을 이용하여 Depth Map을 계산한다.
* ROI 영역(Painting, Frog, Teddy)에 대해 평균 disparity와 평균 depth를 계산한다.
* 세 ROI 중 가장 가까운 영역과 가장 먼 영역을 분석한다.
* Disparity Map과 Depth Map을 컬러맵으로 시각화한다.
* ROI가 표시된 좌/우 이미지와 계산 결과 이미지를 저장한다.

---

# 요구사항

* 입력 이미지를 그레이스케일로 변환한 뒤 `cv2.StereoBM_create()`를 사용하여 disparity map 계산
* Disparity > 0인 픽셀만 사용하여 depth map 계산
* ROI Painting, Frog, Teddy 각각에 대해 평균 disparity와 평균 depth를 계산
* 세 ROI 중 어떤 영역이 가장 가까운지, 어떤 영역이 가장 먼지 해석

---

# 핵심 코드 설명

## 1. 라이브러리 불러오기

```python
import cv2
import numpy as np
from pathlib import Path
```

* `cv2` : OpenCV 라이브러리
* `numpy` : 수치 계산 및 배열 처리를 위한 라이브러리
* `Path` : 파일 경로 및 폴더 생성을 위한 라이브러리

---

## 2. 출력 폴더 생성

```python
output_dir = Path("./outputs")
output_dir.mkdir(parents=True, exist_ok=True)
```

결과 이미지를 저장하기 위한 `outputs` 폴더를 생성한다.

* 폴더가 이미 존재하면 그대로 사용한다.
* 존재하지 않으면 새로 생성한다.

---

## 3. 스테레오 이미지 불러오기

```python
left_color = cv2.imread("left.png")
right_color = cv2.imread("right.png")
```

좌측 이미지와 우측 이미지를 불러온다.

```python
if left_color is None or right_color is None:
    raise FileNotFoundError("좌/우 이미지를 찾지 못했습니다.")
```

이미지를 찾지 못할 경우 오류를 발생시킨다.

---

## 4. 카메라 파라미터 설정

```python
f = 700.0
B = 0.12
```

Depth 계산에 필요한 카메라 파라미터

* `f` : 카메라 focal length
* `B` : 두 카메라 사이 거리 (baseline)

---

## 5. ROI 설정

```python
rois = {
    "Painting": (55, 50, 130, 110),
    "Frog": (90, 265, 230, 95),
    "Teddy": (310, 35, 115, 90)
}
```

세 개의 관심 영역(ROI)을 정의한다.

각 ROI는 다음 형식으로 정의된다.

```
(x 좌표, y 좌표, 너비, 높이)
```

---

## 6. 그레이스케일 변환

```python
left_gray = cv2.cvtColor(left_color, cv2.COLOR_BGR2GRAY)
right_gray = cv2.cvtColor(right_color, cv2.COLOR_BGR2GRAY)
```

스테레오 매칭을 위해 컬러 이미지를 그레이스케일 이미지로 변환한다.

---

## 7. Disparity Map 계산

```python
stereo = cv2.StereoBM_create(numDisparities=128, blockSize=15)
```

StereoBM 알고리즘을 사용하여 disparity 계산 객체를 생성한다.

```python
disparity = stereo.compute(left_gray, right_gray).astype(np.float32)
disparity = disparity / 16.0
```

OpenCV는 disparity 값을 **16배 스케일**로 반환하므로 이를 보정한다.

```python
valid_mask = disparity > 0
```

유효한 disparity 픽셀만 선택한다.

---

## 8. Depth Map 계산

Depth는 다음 공식으로 계산된다.

```
Z = fB / d
```

* `Z` : Depth (거리)
* `f` : focal length
* `B` : baseline
* `d` : disparity

```python
depth_map = np.zeros_like(disparity, dtype=np.float32)
depth_map[valid_mask] = (f * B) / disparity[valid_mask]
```

Disparity가 **0보다 큰 픽셀만 사용하여 Depth를 계산**한다.

---

## 9. ROI 평균 Disparity / Depth 계산

```python
for name, (x, y, w, h) in rois.items():
```

각 ROI 영역을 반복하면서 계산한다.

```python
disp_roi = disparity[y:y+h, x:x+w]
depth_roi = depth_map[y:y+h, x:x+w]
```

ROI 영역을 잘라낸다.

```python
valid_roi = disp_roi > 0
```

유효한 disparity 픽셀만 사용한다.

```python
mean_disp = np.mean(disp_roi[valid_roi])
mean_depth = np.mean(depth_roi[valid_roi])
```

ROI 영역의 평균 disparity와 평균 depth를 계산한다.

---

## 10. 가장 가까운 / 먼 ROI 분석

```python
closest = min(results.items(), key=lambda x: x[1]['mean_depth'])
farthest = max(results.items(), key=lambda x: x[1]['mean_depth'])
```

Depth 값이

* **작을수록 가까운 물체**
* **클수록 먼 물체**

이 기준으로 가장 가까운 ROI와 가장 먼 ROI를 찾는다.

---

## 11. Disparity Map 시각화

```python
disparity_color = cv2.applyColorMap(disp_vis, cv2.COLORMAP_JET)
```

컬러맵을 적용하여 disparity를 시각화한다.

색상 의미

* 빨강 : 가까운 영역
* 파랑 : 먼 영역

---

## 12. Depth Map 시각화

```python
depth_color = cv2.applyColorMap(depth_vis, cv2.COLORMAP_JET)
```

Depth 값을 색상으로 변환하여 거리 차이를 시각적으로 확인할 수 있다.

---

## 13. ROI 표시

```python
cv2.rectangle(left_vis, (x, y), (x + w, y + h), (0, 255, 0), 2)
```

ROI 영역을 사각형으로 표시한다.

```python
cv2.putText(left_vis, name, (x, y - 8),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
```

각 ROI 이름을 이미지 위에 표시한다.

---

## 14. 결과 이미지 저장

```python
cv2.imwrite("outputs/disparity.png", disparity_color)
cv2.imwrite("outputs/depth.png", depth_color)
```

다음 이미지를 저장한다.

* `left_roi.png` : ROI가 표시된 좌 이미지
* `right_roi.png` : ROI가 표시된 우 이미지
* `disparity.png` : Disparity Map
* `depth.png` : Depth Map

---

# 폴더 구조

```
project_folder
│
├ left.png
├ right.png
├ 0312-03.py
│
├ outputs
│   ├ left_roi.png
│   ├ right_roi.png
│   ├ disparity.png
│   └ depth.png
│
└ README.md
```

---

# 실행 방법

1. OpenCV 설치

```
pip install opencv-python
```

2. 프로그램 실행

```
python 0312-03.py
```

---

# 주의사항

* 좌/우 이미지가 정확히 정렬된 스테레오 이미지여야 한다.
* disparity 값이 0 이하인 경우 depth 계산에 사용할 수 없다.
* ROI 영역에 유효한 disparity 픽셀이 없으면 평균 값이 계산되지 않을 수 있다.
* StereoBM 파라미터(`numDisparities`, `blockSize`)에 따라 결과가 달라질 수 있다.
<img width="1015" height="1023" alt="스크린샷 2026-03-12 164402" src="https://github.com/user-attachments/assets/3d728997-04c4-47ba-8459-32fbe5ab98ff" />
<img width="266" height="71" alt="스크린샷 2026-03-12 164154" src="https://github.com/user-attachments/assets/0f8dffe4-8c82-4bba-9b9a-9c9de486d8e9" />


