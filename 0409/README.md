# 01_yolo_sort_tracking.py

* 이 실습에서는 SORT 알고리즘을 사용하여 비디오에서 다중 객체를 실시간으로 추적하는 프로그램을 구현합니다. 이를 통해 객체 추적의 기본 개념과 SORT 알고리즘의 적용 방법을 학습할 수 있습니다.

---

# 기능

* YOLOv3 모델을 사용하여 각 프레임에서 객체를 검출한다.
* 검출된 객체의 경계 상자를 입력으로 받아 SORT 추적기를 초기화한다.
* 칼만 필터로 객체의 다음 위치를 예측하고, 헝가리안 알고리즘으로 detection과 tracker를 매칭한다.
* 각 프레임마다 검출된 객체와 기존 추적 객체를 연관시켜 추적을 유지한다.
* 추적된 각 객체에 고유 ID와 track_id 기반 색상을 부여하여 bounding box와 함께 화면에 표시한다.
* 프레임 번호, 검출 수, 추적 수를 화면에 표시하고, 실시간 FPS는 터미널에 출력한다.
* ESC 키 또는 창의 X 버튼으로 프로그램을 종료할 수 있다.
* 결과 영상을 mp4 파일로 저장한다.

---

# 요구사항

* 객체 검출기 구현: YOLOv3와 같은 사전 훈련된 객체 검출 모델을 사용하여 각 프레임에서 객체를 검출합니다.
* SORT 추적기 초기화: 검출된 객체의 경계 상자를 입력으로 받아 SORT 추적기를 초기화합니다.
* 객체 추적: 각 프레임마다 검출된 객체와 기존 추적 객체를 연관시켜 추적을 유지합니다.
* 결과 시각화: 추적된 각 객체에 고유 ID를 부여하고, 해당 ID와 경계 상자를 비디오 프레임에 표시하여 실시간으로 출력합니다.

---

# 핵심 코드 설명

## 1. 라이브러리 불러오기
```python
import cv2
import numpy as np
from scipy.optimize import linear_sum_assignment
from filterpy.kalman import KalmanFilter
import os
import random
import time
```

* cv2 : OpenCV 라이브러리, 영상 처리 및 YOLOv3 모델 로드에 사용
* numpy : 배열 처리 및 수치 계산을 위한 라이브러리
* linear_sum_assignment : 헝가리안 알고리즘 구현, detection과 tracker 최적 매칭에 사용
* KalmanFilter : 칼만 필터 구현, 객체의 다음 위치 예측에 사용
* os : 파일 경로 확인 및 절대경로 생성에 사용
* random : 추적 객체 표시용 색상 생성에 사용
* time : 프레임 처리 시간 측정 및 실시간 FPS 계산에 사용

---

## 2. IoU 계산 함수
```python
def iou_batch(bb_test, bb_gt):
    ...
    iou = intersection / (union + 1e-6)
    return iou
```

두 bounding box 사이의 겹치는 비율(IoU)을 계산한다.

* 교집합 넓이를 합집합 넓이로 나누어 IoU를 계산한다.
* 0으로 나누는 것을 방지하기 위해 분모에 작은 값(1e-6)을 더한다.
* detection과 tracker 간의 유사도를 측정하는 핵심 지표로 사용된다.

---

## 3. Bounding Box 형식 변환 함수
```python
def convert_bbox_to_z(bbox):   # [x1, y1, x2, y2] -> [x, y, s, r]
    ...

def convert_x_to_bbox(x, score=None):   # [x, y, s, r] -> [x1, y1, x2, y2]
    ...
```

칼만 필터 입력/출력 형식과 bounding box 형식 간의 변환을 수행한다.

* convert_bbox_to_z : 좌상단/우하단 좌표를 중심 좌표(x, y), 면적(s), 종횡비(r)로 변환하여 칼만 필터에 입력한다.
* convert_x_to_bbox : 칼만 필터 상태값을 다시 좌상단/우하단 좌표 형식으로 변환하여 화면에 표시한다.

---

## 4. KalmanBoxTracker 클래스
```python
class KalmanBoxTracker(object):
    def __init__(self, bbox, class_id):  # 칼만 필터 초기화
    def update(self, bbox, class_id):    # 새 detection으로 상태 업데이트
    def predict(self):                   # 다음 프레임 위치 예측
    def get_state(self):                 # 현재 bbox 상태 반환
```

각 객체마다 하나씩 생성되는 개별 추적기 클래스이다.

* 상태 7차원(x, y, s, r, vx, vy, vs), 측정 4차원(x, y, s, r)의 칼만 필터를 사용한다.
* hit_streak : 연속으로 detection과 매칭된 횟수를 저장하여 정식 track 인정 여부를 판단한다.
* time_since_update : 마지막 업데이트 이후 경과 프레임 수를 저장하여 오래된 tracker를 삭제한다.
* class_id : 매 업데이트마다 최신 클래스 정보를 반영한다.

---

## 5. Detection-Tracker 매칭 함수
```python
def associate_detections_to_trackers(detections, trackers, iou_threshold=0.3):
    row_ind, col_ind = linear_sum_assignment(-iou_matrix)   # 헝가리안 알고리즘
    ...
    return matches, unmatched_detections, unmatched_trackers
```

현재 프레임의 detection과 기존 tracker를 IoU 기반으로 최적 매칭한다.

* IoU 행렬을 계산하고 헝가리안 알고리즘으로 전체 IoU 합이 최대가 되는 1:1 매칭을 찾는다.
* IoU threshold(0.3) 미만인 매칭은 제거하여 오매칭을 방지한다.
* 매칭된 쌍, 매칭되지 않은 detection(새 객체), 매칭되지 않은 tracker(사라진 객체)를 각각 반환한다.

---

## 6. Sort 클래스
```python
class Sort(object):
    def __init__(self, max_age=10, min_hits=3, iou_threshold=0.3):
    def update(self, dets):
```

전체 tracker들을 관리하는 SORT 알고리즘의 핵심 클래스이다.

* max_age : tracker가 detection과 매칭되지 않아도 유지되는 최대 프레임 수 (기본값 10, 실제 사용 15)
* min_hits : 정식 track으로 인정받기 위한 최소 연속 매칭 횟수 (기본값 3)
* 매 프레임마다 예측 → 매칭 → 업데이트 → 새 tracker 생성 → 오래된 tracker 삭제 순서로 동작한다.

---

## 7. YOLOv3 모델 로드 함수
```python
def load_yolo_model(cfg_path, weights_path):
    net = cv2.dnn.readNetFromDarknet(cfg_path, weights_path)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    ...
```

cfg 파일과 weights 파일로 YOLOv3 네트워크를 로드한다.

* CUDA가 지원되는 환경에서는 GPU 가속을 사용할 수 있으며, 환경에 따라 CPU에서 실행되도록 설정이 필요할 수 있다.
* 출력 레이어 이름을 추출하여 forward 시 사용한다.

---

## 8. 객체 검출 함수
```python
def detect_objects(frame, net, output_layers, conf_threshold=0.5, nms_threshold=0.4):
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True)
    ...
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
    return np.array(detections)   # [x1, y1, x2, y2, score, class_id]
```

한 프레임에서 YOLOv3로 객체를 검출한다.

* 입력 프레임을 416×416 크기의 blob으로 변환하고 픽셀 값을 0~1로 정규화한다.
* confidence threshold(0.5) 이상의 검출만 유지하고 NMS로 중복 박스를 제거한다.
* 반환 형식은 [x1, y1, x2, y2, score, class_id]이며 SORT 입력 형식과 동일하다.

---

## 9. 메인 함수
```python
def main():
    KalmanBoxTracker.count = 0   # ID 카운터 초기화
    ...
    while True:
        ret, frame = cap.read()
        detections = detect_objects(frame, ...)
        tracks = tracker.update(detections)
        ...
        if key == 27:   # ESC 종료
            break
        if cv2.getWindowProperty(...) < 1:   # X 버튼 종료
            break
```

전체 프로그램 흐름을 제어하는 메인 함수이다.

* 비디오 시작 시 KalmanBoxTracker.count를 0으로 초기화하여 ID가 항상 1부터 시작하도록 한다.
* 매 프레임마다 객체 검출 → SORT 추적 업데이트 → 결과 시각화 순서로 동작한다.
* track_id 기준으로 색상을 부여하여 같은 클래스라도 객체마다 다른 색상으로 표시한다.
* ESC 키 또는 창의 X 버튼으로 종료할 수 있으며, 종료 시 결과 영상을 mp4 파일로 저장한다.

---

# 폴더 구조
```
project_folder
│
├── 01_yolo_sort_tracking.py
├── slow_traffic_small.mp4
├── yolov3.cfg
├── yolov3.weights
├── output_tracking.mp4     (실행 후 생성)
│
└── README.md
```

---

# 실행 방법

1. 필요 라이브러리 설치
```
pip install opencv-python numpy scipy filterpy
```

2. YOLOv3 모델 파일 준비 (yolov3.cfg, yolov3.weights)

3. 프로그램 실행
```
python 01_yolo_sort_tracking.py
```

---

# 주의사항

* yolov3.cfg, yolov3.weights, slow_traffic_small.mp4 파일이 모두 같은 폴더에 있어야 한다.
* CUDA가 지원되지 않는 환경에서는 CPU로 전환하여 실행해야 하며 FPS가 낮게 나올 수 있다.
* max_age, min_hits, iou_threshold 값에 따라 추적 성능이 달라질 수 있다.
* 결과 영상은 프로그램 실행 폴더에 output_tracking.mp4로 저장된다.

  <img width="637" height="390" alt="01_yolo_sort_tracking 결과" src="https://github.com/user-attachments/assets/0ab0e5ac-3fc1-4e6e-9aeb-d3eb360ff693" />

<img width="665" height="732" alt="01_yolo_sort_tracking 로그" src="https://github.com/user-attachments/assets/4b328d41-5668-4be7-96ac-8cea91013d8f" />

---
# 02_mediapipe_face_landmark.py

* Mediapipe의 FaceMesh 모듈을 사용하여 얼굴의 468개 랜드마크를 추출하고, 이를 이미지에 시각화하는 프로그램을 구현합니다.
---

# 기능

* Mediapipe FaceMesh 모델을 사용하여 이미지에서 얼굴 랜드마크를 검출한다.
* 검출된 468개의 랜드마크를 이미지 위에 초록색 점으로 시각화한다.
* FACEMESH_TESSELATION을 사용하여 얼굴 전체에 삼각형 메시 연결선을 그린다.
* 얼굴 검출 여부를 "Face Detected" / "No Face Detected" 텍스트로 화면에 표시한다.
* 결과 이미지를 파일로 저장한다.
* ESC 키를 누르면 프로그램이 종료된다.

---

# 요구사항

* Mediapipe의 FaceMesh 모듈을 사용하여 얼굴 랜드마크 검출기를 초기화합니다.
* OpenCV를 사용하여 이미지를 불러오고 결과를 화면에 표시합니다.
* 검출된 얼굴 랜드마크를 이미지에 점으로 표시합니다.
* ESC 키를 누르면 프로그램이 종료되도록 설정합니다.


---

# 핵심 코드 설명

## 1. 라이브러리 불러오기
```python
import cv2
import mediapipe as mp
import os
```

* cv2 : OpenCV 라이브러리, 이미지 불러오기, 랜드마크 시각화, 결과 저장 및 화면 출력에 사용
* mediapipe : FaceMesh 모델을 통해 얼굴 468개 랜드마크를 검출하고 메시 연결선을 그리는 데 사용
* os : 현재 파일 경로 기준으로 입력/출력 이미지 절대경로를 생성하는 데 사용

---

## 2. Mediapipe FaceMesh 객체 초기화
```python
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
```

Mediapipe에서 FaceMesh 관련 기능을 불러온다.

* mp_face_mesh : 얼굴 랜드마크 검출 모델을 제공한다.
* mp_drawing : 이미지 위에 랜드마크와 연결선을 그리는 유틸리티를 제공한다.
* mp_drawing_styles : 기본 메시 스타일(색상, 두께 등)을 제공한다.

---

## 3. FaceMesh 객체 생성
```python
with mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=False,
    min_detection_confidence=0.5
) as face_mesh:
```

FaceMesh 검출기를 생성하고 설정값을 지정한다.

* static_image_mode=True : 정적 이미지를 처리하는 모드로, 비디오 스트림이 아닌 단일 이미지에 적합하다.
* max_num_faces=1 : 최대 1개의 얼굴만 검출한다.
* refine_landmarks=False : 기본 FaceMesh 랜드마크를 검출한다.
* min_detection_confidence=0.5 : 신뢰도 0.5 이상인 검출 결과만 사용한다.

---

## 4. 얼굴 랜드마크 검출
```python
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
results = face_mesh.process(rgb_image)
```

이미지를 RGB로 변환한 뒤 FaceMesh로 얼굴 랜드마크를 검출한다.

* OpenCV는 BGR 형식으로 이미지를 불러오므로, Mediapipe 입력에 맞게 RGB로 변환해야 한다.
* 검출 결과는 results.multi_face_landmarks에 저장되며, 얼굴이 없을 경우 None이 된다.

---

## 5. 얼굴 메시 및 랜드마크 시각화
```python
mp_drawing.draw_landmarks(
    image=image,
    landmark_list=face_landmarks,
    connections=mp_face_mesh.FACEMESH_TESSELATION,
    landmark_drawing_spec=None,
    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
)

for landmark in face_landmarks.landmark:
    x = int(landmark.x * w)
    y = int(landmark.y * h)
    cv2.circle(image, (x, y), 1, (0, 255, 0), -1)
```

검출된 랜드마크를 이미지 위에 시각화한다.

* FACEMESH_TESSELATION : 얼굴 전체를 삼각형 격자(메시) 형태로 연결하는 연결선 정보를 제공한다.
* 랜드마크 좌표는 0~1 사이의 정규화된 값이므로, 이미지 크기(w, h)를 곱해 실제 픽셀 좌표로 변환한다.
* cv2.circle로 각 랜드마크 위치에 초록색 점을 그린다.

---

## 6. 결과 저장 및 화면 출력
```python
cv2.imwrite(output_image, image)
cv2.imshow("Mediapipe Face Landmark Image", image)

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break
```

결과 이미지를 파일로 저장하고 화면에 출력한다.

* cv2.imwrite로 결과 이미지를 parkbogum_result.png 파일로 저장한다.
* ESC 키(keycode 27)를 누르면 프로그램이 종료된다.

---

# 폴더 구조
```
project_folder
│
├── 02_mediapipe_face_landmark.py
├── parkbogum.png
├── parkbogum_result.png     (실행 후 생성)
│
└── README.md
```

---

# 실행 방법

1. 필요 라이브러리 설치
```
pip install opencv-python mediapipe
```

2. 입력 이미지 준비 (parkbogum.png)

3. 프로그램 실행
```
python 02_mediapipe_face_landmark.py
```

---

# 주의사항

* parkbogum.png 파일이 파이썬 파일과 같은 폴더에 있어야 한다.
* Mediapipe는 RGB 형식의 이미지를 입력으로 받으므로, OpenCV로 불러온 BGR 이미지를 반드시 변환해야 한다.
* 랜드마크 좌표는 정규화된 값이므로, 이미지 크기에 맞게 변환이 필요하다.
* 결과 이미지는 프로그램 실행 폴더에 parkbogum_result.png로 저장된다.

<img width="474" height="474" alt="parkbogum" src="https://github.com/user-attachments/assets/7fe4afc6-94dd-4e54-8148-19b757b27c01" />
<img width="474" height="474" alt="parkbogum_result" src="https://github.com/user-attachments/assets/d1bbdb1b-ed81-4014-9888-7a434119589e" />
<img width="686" height="42" alt="02_mediapipe_face_landmark 로그" src="https://github.com/user-attachments/assets/169abe89-89b3-4517-a0d2-a1e66c72a6eb" />

