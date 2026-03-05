# 0305-01.py
- openCV를 사용하여 이미지를 불러오고 화면에 출력
- 원본 이미지와 그레이스케일로 변환된 이미지를 나란히 표시

## 기능
- 이미지 파일(`soccer.jpg`)을 로드합니다.
- 이미지를 그레이스케일로 변환합니다.
- 그레이스케일 이미지를 가로와 세로를 0.5배로 축소합니다.
- 원본 이미지와 그레이스케일 이미지를 가로로 연결합니다.
- 연결된 이미지를 화면에 표시합니다.
- 결과를 `gray_small.jpg` 파일로 저장합니다.
- 이미지의 타입과 크기 정보를 콘솔에 출력합니다.

## 요구사항
- cv.imread()를 사용하여 이미지 로드
- cv.cvtColor() 함수를 사용해 이미지를 그레이스케일로 변환
- np.hstack() 함수를 이용해 원본 이미지와 그레이스케일이미지를 가로로 연결하여 출력
- cv.imshow()와 cv.waitKey()를 사용해 결과를 화면에 표시하고, 아무키나 누르면 창이 닫히도록 할 것

## 핵심 코드 설명
### 1. 이미지 불러오기
```python
img = cv.imread('soccer.jpg')
```
OpenCV의 `cv.imread()` 함수를 사용하여 `soccer.jpg` 이미지를 불러와 `img` 변수에 저장한다.  
이미지 파일이 존재하지 않을 경우 `None`이 반환된다.

```python
if img is None:
    sys.exit('파일이 존재하지 않습니다.')
```
이미지가 정상적으로 로드되지 않았을 경우 `sys.exit()`를 사용하여 프로그램을 종료한다.

---

### 2. 그레이스케일 변환
```python
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
```
`cv.cvtColor()` 함수를 사용하여 컬러 이미지를 **그레이스케일 이미지**로 변환한다.  
그레이스케일 이미지는 색상 정보가 제거되고 밝기 정보만 남은 흑백 이미지이다.

---

### 3. 이미지 크기 조정
```python
gray_small = cv.resize(gray, dsize=(0,0), fx=0.5, fy=0.5)
```
`cv.resize()` 함수를 사용하여 이미지를 **가로와 세로 모두 0.5배로 축소**한다.  
`fx`는 가로 비율, `fy`는 세로 비율을 의미한다.

---

### 4. 이미지 가로 연결
```python
gray_small = np.hstack((img, cv.cvtColor(gray, cv.COLOR_GRAY2BGR)))
```
NumPy의 `hstack()` 함수를 사용하여 **원본 이미지와 그레이스케일 이미지를 가로로 연결**한다.  
그레이스케일 이미지는 채널이 1개이고 컬러 이미지는 채널이 3개(BGR)이기 때문에 그대로 연결할 수 없다.  
따라서 `cv.cvtColor(gray, cv.COLOR_GRAY2BGR)`을 사용하여 그레이스케일 이미지를 BGR 형식으로 변환한 후 연결한다.

---

### 5. 이미지 출력
```python
cv.imshow('Image Display', gray_small)
cv.waitKey()
```
`cv.imshow()`를 사용하여 결과 이미지를 화면에 출력한다.  
`cv.waitKey()`는 키보드 입력이 들어올 때까지 프로그램을 대기시켜 이미지 창이 바로 닫히지 않도록 한다.

---

### 6. 결과 이미지 저장
```python
cv.imwrite('gray_small.jpg', gray_small)
```
`cv.imwrite()` 함수를 사용하여 처리된 결과 이미지를 `gray_small.jpg` 파일로 저장한다.

---

### 7. 이미지 정보 출력
```python
print(type(img))
print(img.shape)
```
이미지의 데이터 타입과 크기를 출력한다.  

- `type(img)` : 이미지 데이터 타입  
- `img.shape` : `(높이, 너비, 채널)` 형태로 이미지 크기를 나타낸다.

  ## 주의사항

1. 프로그램을 실행하기 전에 `soccer.jpg` 이미지 파일이 코드와 같은 폴더에 있어야 한다.  
   이미지 파일이 존재하지 않을 경우 프로그램은 `파일이 존재하지 않습니다.`라는 메시지를 출력하고 종료된다.

2. OpenCV 라이브러리가 설치되어 있어야 프로그램이 정상적으로 실행된다.  
   설치되지 않은 경우 다음 명령어로 설치할 수 있다.

```bash
pip install opencv-python
```

3. NumPy 라이브러리도 함께 설치되어 있어야 한다.

```bash
pip install numpy
```

4. `cv.imshow()`로 이미지를 출력할 경우 `cv.waitKey()`를 사용해야 창이 바로 닫히지 않는다.

5. 결과 이미지는 `cv.imwrite()` 함수를 사용하여 `gray_small.jpg` 파일로 저장된다.
![gray_small](https://github.com/user-attachments/assets/7a51bc64-12a6-49ce-aff2-6348d31f205f)

