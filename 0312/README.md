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

* 모든 이미지에서 체크보드 코너를 검
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
<img width="1318" height="507" alt="스크린샷 2026-03-12 123400" src="https://github.com/user-attachments/assets/ef3daff2-42b3-48e5-bca0-06a514b4cc74" />
