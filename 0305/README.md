# 0305-01.py

이 스크립트는 OpenCV와 NumPy를 사용하여 이미지를 처리하는 간단한 예제입니다. `soccer.jpg` 이미지를 로드하여 그레이스케일로 변환하고, 크기를 조정한 후 원본 이미지와 연결하여 표시하고 저장합니다.

## 기능
- 이미지 파일(`soccer.jpg`)을 로드합니다.
- 이미지를 그레이스케일로 변환합니다.
- 그레이스케일 이미지를 가로와 세로를 0.5배로 축소합니다.
- 원본 이미지와 그레이스케일 이미지를 가로로 연결합니다.
- 연결된 이미지를 화면에 표시합니다.
- 결과를 `gray_small.jpg` 파일로 저장합니다.
- 이미지의 타입과 크기 정보를 콘솔에 출력합니다.

## 요구사항
- Python 3.x
- OpenCV (`cv2`)
- NumPy (`numpy`)

필요한 라이브러리를 설치하려면 다음 명령어를 사용하세요:
```
pip install opencv-python numpy
```

## 사용법
1. `soccer.jpg` 이미지를 같은 디렉토리에 배치합니다.
2. 터미널에서 다음 명령어를 실행합니다:
   ```
   python 0305-01.py
   ```
3. 이미지가 표시되면 아무 키나 눌러 창을 닫습니다.
4. `gray_small.jpg` 파일이 생성됩니다.

## 출력 예시
```
<class 'numpy.ndarray'>
(높이, 너비, 3)
```

## 주의사항
- `soccer.jpg` 파일이 존재하지 않으면 프로그램이 종료됩니다.
- OpenCV 창이 표시되므로 GUI 환경에서 실행하는 것이 좋습니다.

## 핵심 코드 설명
0305-01.py의 핵심 코드를 단계별로 설명하겠습니다. 이 코드는 OpenCV를 사용하여 이미지를 로드하고 처리하는 기본 예제입니다.

### 1. 라이브러리 불러오기
```python
import cv2 as cv
import numpy as np
import sys
```
- `cv2`: OpenCV 라이브러리 (이미지 처리용).
- `numpy`: 배열 연산용.
- `sys`: 프로그램 종료용.

### 2. 이미지 로드 및 검증
```python
img = cv.imread('soccer.jpg')
if img is None:
    sys.exit('파일이 존재하지 않습니다.')
```
- `cv.imread()`로 'soccer.jpg' 이미지를 로드하여 NumPy 배열로 저장.
- 파일이 없으면 프로그램 종료.

### 3. 그레이스케일 변환
```python
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
```
- 원본 BGR 이미지를 그레이스케일로 변환 (색상 정보 제거).

### 4. 이미지 크기 조정
```python
gray_small = cv.resize(gray, dsize=(0,0), fx=0.5, fy=0.5)
```
- 그레이스케일 이미지를 가로/세로 0.5배로 축소.

### 5. 이미지 연결
```python
gray_small = np.hstack((img, cv.cvtColor(gray, cv.COLOR_GRAY2BGR)))
```
- 원본 이미지와 그레이스케일 이미지를 가로로 연결 (NumPy의 `hstack` 사용).
- 그레이스케일을 BGR로 변환하여 채널 수 맞춤.

### 6. 이미지 표시 및 저장
```python
cv.imshow('Image Display', gray_small)
cv.waitKey()
cv.destroyAllWindows()
cv.imwrite('gray_small.jpg', gray_small)
```
- 연결된 이미지를 창에 표시.
- 키 입력 대기 후 창 닫기.
- 결과를 'gray_small.jpg'로 저장.

### 7. 정보 출력
```python
print(type(img))
print(img.shape)
```
- 이미지의 타입 (NumPy 배열)과 크기 (높이, 너비, 채널 수) 출력.

이 코드는 OpenCV의 기본 이미지 처리 함수들을 보여주는 예제입니다. 실제 실행 시 'soccer.jpg' 파일이 필요합니다.