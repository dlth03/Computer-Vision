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


# 0305-02.py
- 마우스 입력으로 이미지 위에 붓질
- 키보드 입력을 이용해 붓의 크기를 조절하는 기능 추가
## 기능
- 이미지 파일(`soccer.jpg`)을 로드합니다.
- 마우스를 이용해 이미지 위에 그림을 그릴 수 있습니다.
- 왼쪽 마우스 버튼 드래그 → 파란색으로 그림
- 오른쪽 마우스 버튼 드래그 → 빨간색으로 그림
- `+` 키를 누르면 붓 크기가 증가합니다. (최대 15)
- `-` 키를 누르면 붓 크기가 감소합니다. (최소 1)
- `q` 키를 누르면 현재 이미지를 `paint.jpg`로 저장하고 프로그램을 종료합니다.
- 이미지의 타입과 크기 정보를 콘솔에 출력합니다.

---

## 요구사항
- 초기 붓 크기는 5를 사용
- + 입력 시 붓 크기 1 증가, -입력 시 붓 크기 1 감소
- 붓 크기는 최소 1, 최대 15로 제한
- 좌클릭 = 파란색, 우클릭 = 빨간색, 드래그로 연속 그리기
- q키를 누르면 영상 창이 종료

---

## 핵심 코드 설명

### 1. 이미지 불러오기
```python
img = cv.imread('soccer.jpg')
```

OpenCV의 `cv.imread()` 함수를 사용하여 `soccer.jpg` 이미지를 불러와 `img` 변수에 저장한다.  
이미지 파일이 존재하지 않으면 `None`이 반환된다.

```python
if img is None:
    sys.exit('파일이 존재하지 않습니다.')
```

이미지가 정상적으로 로드되지 않은 경우 프로그램을 종료한다.

---

### 2. 붓 크기 설정
```python
brush_size = 5
```

이미지 위에 그림을 그릴 때 사용할 **붓의 기본 크기**를 설정한다.

---

### 3. 마우스 상태 변수
```python
drawing_left = False
drawing_right = False
```

마우스 버튼이 눌려 있는 상태인지 확인하기 위한 변수이다.

- `drawing_left` : 왼쪽 버튼 드래그 상태
- `drawing_right` : 오른쪽 버튼 드래그 상태

---

### 4. 마우스 이벤트 처리 함수
```python
def mouse_event(event, x, y, flags, param):
```

마우스 이벤트가 발생할 때 호출되는 함수이다.  
마우스 클릭, 이동, 버튼 해제 등의 이벤트를 처리한다.

---

### 5. 마우스 클릭 감지
```python
if event == cv.EVENT_LBUTTONDOWN:
    drawing_left = True
```

왼쪽 마우스 버튼을 누르면 `drawing_left` 값을 `True`로 변경하여  
**그림을 그릴 수 있는 상태**로 만든다.

```python
elif event == cv.EVENT_RBUTTONDOWN:
    drawing_right = True
```

오른쪽 버튼을 누르면 `drawing_right` 값을 `True`로 설정한다.

---

### 6. 마우스 이동 시 그림 그리기
```python
elif event == cv.EVENT_MOUSEMOVE:
    if drawing_left:
        cv.circle(img, (x, y), brush_size, (255, 0, 0), -1)
```

마우스를 움직이는 동안 왼쪽 버튼이 눌려 있으면  
현재 마우스 위치 `(x, y)`에 **파란색 원을 그려 그림을 그린다.**

```python
elif drawing_right:
    cv.circle(img, (x, y), brush_size, (0, 0, 255), -1)
```

오른쪽 버튼이 눌려 있으면 **빨간색으로 그림을 그린다.**

---

### 7. 마우스 이벤트 연결
```python
cv.namedWindow('Image Display')
cv.setMouseCallback('Image Display', mouse_event)
```

`cv.setMouseCallback()`을 사용하여  
이미지 창과 마우스 이벤트 처리 함수를 연결한다.

---

### 8. 화면 출력 및 키 입력 처리
```python
cv.imshow('Image Display', img)
key = cv.waitKey(1) & 0xFF
```

`cv.imshow()`를 사용하여 이미지를 화면에 출력하고  
`cv.waitKey()`로 키보드 입력을 받는다.

---

### 9. 붓 크기 조절
```python
if key == ord('+'):
    brush_size = min(15, brush_size + 1)
```

`+` 키를 누르면 붓 크기가 증가한다.

```python
elif key == ord('-'):
    brush_size = max(1, brush_size - 1)
```

`-` 키를 누르면 붓 크기가 감소한다.

---

### 10. 이미지 저장
```python
elif key == ord('q'):
    cv.imwrite('paint.jpg', img)
```

`q` 키를 누르면 현재 이미지를 `paint.jpg` 파일로 저장하고 프로그램을 종료한다.

---

### 11. 프로그램 종료
```python
cv.destroyAllWindows()
```

모든 OpenCV 창을 닫는다.

---

### 12. 이미지 정보 출력
```python
print(type(img))
print(img.shape)
```

이미지의 데이터 타입과 크기를 출력한다.

- `type(img)` : 이미지 데이터 타입  
- `img.shape` : `(높이, 너비, 채널)` 형태로 이미지 크기를 나타낸다.

---

## 주의사항

1. 프로그램 실행 전에 `soccer.jpg` 이미지 파일이 코드와 같은 폴더에 있어야 한다.

2. OpenCV 라이브러리가 설치되어 있어야 프로그램이 정상적으로 실행된다.

```bash
pip install opencv-python
```

3. `cv.imshow()`를 사용할 경우 `cv.waitKey()`를 사용해야 창이 바로 닫히지 않는다.

4. 프로그램 종료 시 `q` 키를 눌러야 이미지가 `paint.jpg` 파일로 저장된다.
![paint](https://github.com/user-attachments/assets/5d0dd4a7-b013-49bd-b96e-16ce2383c066)


# 0305-03.py
- 이미지를 불러오고 사용자가 마우스로 클릭하고 드래그하여 관심영역(ROI)을 선택
- 선택한 영역만 따로 저장하거나 표시

## 기능
- 이미지 파일(`soccer.jpg`)을 로드합니다.
- 마우스를 이용해 이미지에서 사각형 영역(ROI)을 선택할 수 있습니다.
- 마우스를 드래그하면 초록색 사각형으로 선택 영역이 표시됩니다.
- 마우스를 놓으면 선택된 영역이 ROI 창에 출력됩니다.
- `s` 키를 누르면 선택한 ROI 영역을 이미지 파일로 저장합니다.
- `r` 키를 누르면 선택 영역을 초기화합니다.
- `q` 키를 누르면 프로그램을 종료합니다.

---

## 요구사항
- 이미지를 불러오고 화면에 출력
- cv.setMouseCallback()`을 사용하여 마우스 이벤트 처리
- 사용자가 클릭한 시작점에서 드래그하여 사각형을 그리며 영역을 선택
- 마우스를 놓으면 해당 영역을 잘라내서 별도의 창에 출력
- r 키를 누르면 영역 선택을 리셋하고 처음부터 다시 선택
- s 키를 누르면 선택한 영역을 이미지 파일로 저장
  
---

## 핵심 코드 설명

### 1. 이미지 불러오기

```python
img = cv.imread('soccer.jpg')
```

OpenCV의 `cv.imread()` 함수를 사용하여 `soccer.jpg` 이미지를 불러와 `img` 변수에 저장한다.  
이미지 파일이 존재하지 않으면 `None`이 반환된다.

```python
if img is None:
    sys.exit('파일이 존재하지 않습니다.')
```

이미지가 정상적으로 로드되지 않은 경우 프로그램을 종료한다.

```python
img_copy = img.copy()
```

원본 이미지를 보존하기 위해 이미지 복사본을 생성한다.

---

### 2. ROI 선택을 위한 좌표 변수

```python
start_x, start_y = -1, -1
end_x, end_y = -1, -1
```

마우스 드래그의 시작 좌표와 종료 좌표를 저장하는 변수이다.

```python
drawing = False
roi = None
```

- drawing : 드래그 상태 여부  
- roi : 선택된 ROI 이미지를 저장하는 변수

---

### 3. 마우스 이벤트 처리 함수

```python
def mouse_event(event, x, y, flags, param):
```

마우스 클릭, 이동, 버튼 해제 등의 이벤트가 발생할 때 호출되는 함수이다.

---

### 4. 드래그 시작

```python
if event == cv.EVENT_LBUTTONDOWN:
    drawing = True
    start_x, start_y = x, y
```

왼쪽 마우스 버튼을 누르면 드래그가 시작되고 시작 좌표를 저장한다.

---

### 5. 드래그 중 사각형 표시

```python
elif event == cv.EVENT_MOUSEMOVE:
    if drawing:
        img = img_copy.copy()
        cv.rectangle(img, (start_x, start_y), (x, y), (0,255,0), 2)
```

마우스를 움직이는 동안 드래그 상태라면  
현재 마우스 위치까지 초록색 사각형을 그려 선택 영역을 표시한다.

---

### 6. 드래그 종료 및 ROI 추출

```python
elif event == cv.EVENT_LBUTTONUP:
    drawing = False
    end_x, end_y = x, y
```

마우스를 놓으면 드래그가 종료되고 종료 좌표를 저장한다.

```python
x1 = min(start_x, end_x)
x2 = max(start_x, end_x)
y1 = min(start_y, end_y)
y2 = max(start_y, end_y)
```

드래그 방향에 관계없이 올바른 영역을 선택하기 위해 좌표를 정렬한다.

```python
roi = img_copy[y1:y2, x1:x2]
```

NumPy 슬라이싱을 이용하여 선택된 영역을 ROI로 추출한다.

```python
cv.imshow("ROI", roi)
```

선택된 영역을 ROI 창에 따로 출력한다.

---

### 7. 마우스 이벤트 연결

```python
cv.namedWindow("Image")
cv.setMouseCallback("Image", mouse_event)
```

이미지 창을 생성하고 해당 창에 마우스 이벤트 함수를 연결한다.

---

### 8. 화면 출력 및 키 입력 처리

```python
cv.imshow("Image", img)
key = cv.waitKey(1) & 0xFF
```

이미지를 화면에 출력하고 키보드 입력을 받는다.

---

### 9. 화면 초기화

```python
if key == ord('r'):
    img = img_copy.copy()
    roi = None
```

`r` 키를 누르면 선택 영역을 초기화하고 이미지를 원본 상태로 되돌린다.

---

### 10. ROI 저장

```python
elif key == ord('s'):
    if roi is not None and roi.size != 0:
        cv.imwrite("0305-03/roi.jpg", roi)
```

`s` 키를 누르면 선택한 ROI 영역을 `0305-03/roi.jpg` 파일로 저장한다.

---

### 11. 프로그램 종료

```python
elif key == ord('q'):
    break
```

`q` 키를 누르면 프로그램이 종료된다.

```python
cv.destroyAllWindows()
```

모든 OpenCV 창을 닫는다.

---

## 주의사항

1. 프로그램 실행 전에 `soccer.jpg` 이미지 파일이 코드와 같은 폴더에 있어야 한다.

2. ROI 이미지는 다음 경로에 저장된다.

```
0305-03/roi.jpg
```

따라서 `0305-03` 폴더가 미리 생성되어 있어야 한다.

3. OpenCV 라이브러리가 설치되어 있어야 프로그램이 정상적으로 실행된다.

```
pip install opencv-python
```

4. 마우스로 드래그하여 영역을 선택해야 ROI 창이 나타난다.

5. ROI 영역을 선택하지 않은 상태에서 `s` 키를 눌러도 이미지가 저장되지 않는다.
<img width="1432" height="973" alt="final" src="https://github.com/user-attachments/assets/6a5f1b75-c242-4d89-9a29-30b7b6ae6b95" />
